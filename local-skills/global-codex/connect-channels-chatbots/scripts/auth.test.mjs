import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, writeFileSync, unlinkSync, rmdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { requestOtp, requestOtpToFile, authenticate } from './auth.mjs';
import { readSession, writeSession } from './session.mjs';

const response = data => ({ ok: true, status: 200, json: async () => data });
test('login uses recovered EMAIL and OTP contracts, not an invented code field', async () => {
  const calls = [];
  const replies = [{ id: 'partner' }, { id: 'challenge' }, { accessToken: 'synthetic-access', refreshToken: 'synthetic-refresh', tenantId: 'tenant' }];
  const fakeFetch = async (url, options) => { calls.push({ url, ...options }); return response(replies.shift()); };
  const state = await requestOtp('synthetic@example.test', fakeFetch);
  const session = await authenticate(state, '123456', fakeFetch);
  assert.deepEqual(JSON.parse(calls[1].body), { email: 'synthetic@example.test', type: 'EMAIL', partnerId: 'partner' });
  assert.deepEqual(JSON.parse(calls[2].body), { email: 'synthetic@example.test', password: '123456', grantType: 'OTP', partnerId: 'partner', internalDeviceId: state.internalDeviceId });
  assert.equal(session.tenantId, 'tenant');
  assert(calls.every(call => call.redirect === 'error'));
});

test('invalid OTP causes no authentication request', async () => {
  let calls = 0;
  await assert.rejects(authenticate({}, 'invalid', async () => { calls++; }), /six-digit/);
  assert.equal(calls, 0);
});

test('an occupied challenge path causes no email request', async () => {
  const folder = mkdtempSync(join(tmpdir(), 'connect-challenge-test-'));
  const path = join(folder, 'challenge.json');
  let calls = 0;
  writeFileSync(path, 'existing state');
  try {
    await assert.rejects(requestOtpToFile('synthetic@example.test', path, async () => { calls++; }), { code: 'EEXIST' });
    assert.equal(calls, 0);
    assert.equal(readFileSync(path, 'utf8'), 'existing state');
  } finally { unlinkSync(path); rmdirSync(folder); }
});

test('passes challenge.userId only when supplied by the recovered contract', async () => {
  let body;
  await authenticate({ email: 'synthetic@example.test', challenge: { id: 'challenge', userId: 'user' }, partnerId: 'partner', internalDeviceId: 'device' }, '123456', async (url, options) => { body = JSON.parse(options.body); return response({ accessToken: 'synthetic', refreshToken: 'synthetic', tenantId: 'tenant' }); });
  assert.equal(body.id, 'user');
});

test('real Windows DPAPI roundtrip stores no plaintext and replaces an existing session safely', () => {
  const folder = mkdtempSync(join(tmpdir(), 'connect-session-test-'));
  const path = join(folder, 'session.dpapi');
  try {
    const session = { accessToken: 'synthetic-secret', refreshToken: 'synthetic-refresh', tenantId: 'tenant' };
    writeSession(session, path);
    assert(!readFileSync(path, 'utf8').includes('synthetic-secret'));
    assert.deepEqual(readSession(path), session);
    writeSession({ ...session, accessToken: 'renewed-synthetic' }, path);
    assert.equal(readSession(path).accessToken, 'renewed-synthetic');
  } finally { unlinkSync(path); rmdirSync(folder); }
});

test('expired session refreshes once by HTTP and persists the replacement in an isolated DPAPI file', () => {
  const folder = mkdtempSync(join(tmpdir(), 'connect-refresh-test-'));
  const path = join(folder, 'session.dpapi');
  const code = `
    const assert = await import('node:assert/strict');
    const { ConnectClient } = await import(${JSON.stringify(new URL('./connect.mjs', import.meta.url).href)});
    const { writeSession, readSession } = await import(${JSON.stringify(new URL('./session.mjs', import.meta.url).href)});
    const token = 'header.' + Buffer.from(JSON.stringify({exp:1})).toString('base64url') + '.signature';
    writeSession({accessToken:token,refreshToken:'synthetic-refresh',tenantId:'tenant',partnerId:'partner',internalDeviceId:'device'});
    const calls = [];
    const client = new ConnectClient({fetchImpl:async (url, options)=>{
      calls.push({url,...options});
      return {ok:true,status:200,json:async()=>url.includes('/authenticate/refresh')?{accessToken:'renewed-synthetic',refreshToken:'next-synthetic',tenantId:'tenant'}:{id:'synthetic'}};
    }});
    await client.request('GET','/core/v1/agent/me');
    await client.request('GET','/core/v1/agent/me');
    assert.equal(calls.length,3);
    assert.equal(calls[0].headers.Authorization,undefined);
    assert.equal(calls[1].headers.Authorization,'Bearer renewed-synthetic');
    assert.equal(readSession().refreshToken,'next-synthetic');
    const current = {...readSession(),accessToken:'header.'+Buffer.from(JSON.stringify({exp:Math.floor(Date.now()/1000)+3600})).toString('base64url')+'.signature'};
    writeSession(current);
    const validCalls=[];
    await new ConnectClient({fetchImpl:async(url)=>{validCalls.push(url);return {ok:true,status:200,json:async()=>({})}}}).request('GET','/core/v1/agent/me');
    assert.equal(validCalls.length,1);
    assert.ok(!validCalls[0].includes('/refresh'));
    const deniedCalls=[];
    await assert.rejects(new ConnectClient({fetchImpl:async(url)=>{deniedCalls.push(url);return {ok:false,status:403}}}).request('GET','/core/v1/agent/me'),/HTTP 403/);
    assert.equal(deniedCalls.length,1);
    const recoveryCalls=[];
    const recovery=new ConnectClient({fetchImpl:async(url,options)=>{
      recoveryCalls.push({url,...options});
      if(recoveryCalls.length===1)return {ok:false,status:401};
      return {ok:true,status:200,json:async()=>url.includes('/refresh')?{accessToken:'recovered-synthetic',refreshToken:'recovered-refresh',tenantId:'tenant'}:{}};
    }});
    await recovery.request('POST','/chat/v1/chatbot',{name:'synthetic'});
    assert.deepEqual(recoveryCalls.map(call=>call.method),['POST','POST','POST']);
    assert.ok(recoveryCalls[1].url.includes('/refresh'));
    assert.equal(recoveryCalls[2].headers.Authorization,'Bearer recovered-synthetic');
    assert.equal(recoveryCalls[0].body,recoveryCalls[2].body);
    writeSession({...current,accessToken:token});
    const before=readSession();
    const drift=new ConnectClient({fetchImpl:async()=>({ok:true,status:200,json:async()=>({accessToken:'synthetic',refreshToken:'synthetic',tenantId:'different-tenant'})})});
    await assert.rejects(drift.request('GET','/core/v1/agent/me'),/company identity/);
    assert.deepEqual(readSession(),before);
    const rejected=new ConnectClient({fetchImpl:async()=>({ok:false,status:401})});
    await assert.rejects(rejected.request('GET','/core/v1/agent/me'),/Session refresh: HTTP 401/);
    assert.deepEqual(readSession(),before);
  `;
  try {
    const result = spawnSync(process.execPath, ['--input-type=module', '-e', code], { env: { ...process.env, CONNECT_ACCESS_TOKEN: '', CONNECT_SESSION_FILE: path }, encoding: 'utf8', timeout: 30000, windowsHide: true });
    assert.equal(result.status, 0, result.stderr);
  } finally { unlinkSync(path); rmdirSync(folder); }
});
