import assert from 'node:assert/strict';
import { readFile, writeFile } from 'node:fs/promises';
import { randomUUID } from 'node:crypto';
import { pathToFileURL } from 'node:url';
import { writeSession, sessionFile } from './session.mjs';

const API = 'https://api.wts.chat';
const CONFIG = 'https://cdn.wts.chat/static/partners/app.connectchannels.com.br/config.json';
export async function requestOtp(email, fetchImpl = fetch) {
  assert(/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email), 'A login email is required');
  const configResponse = await fetchImpl(CONFIG, { redirect: 'error', signal: AbortSignal.timeout(30000) });
  assert(configResponse.ok, `Partner config: HTTP ${configResponse.status}`);
  const config = await configResponse.json();
  assert(config.id, 'Partner config has no ID');
  const state = { email, partnerId: config.id, internalDeviceId: randomUUID(), requestedAt: new Date().toISOString() };
  const response = await fetchImpl(`${API}/auth/v2/login/send-otp`, {
    method: 'POST', redirect: 'error', signal: AbortSignal.timeout(30000), headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, type: 'EMAIL', partnerId: state.partnerId }),
  });
  assert(response.ok, `OTP request: HTTP ${response.status}`);
  state.challenge = await response.json();
  assert(state.challenge.id, 'OTP challenge was not identified');
  return state;
}
export async function authenticate(state, otp, fetchImpl = fetch) {
  assert(/^\d{6}$/.test(otp), 'A six-digit OTP is required');
  const response = await fetchImpl(`${API}/auth/v2/login/authenticate`, {
    method: 'POST', redirect: 'error', signal: AbortSignal.timeout(30000), headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: state.challenge.userId, email: state.email, password: otp, grantType: 'OTP', partnerId: state.partnerId, internalDeviceId: state.internalDeviceId }),
  });
  assert(response.ok, `Authentication: HTTP ${response.status}`);
  const result = await response.json();
  assert(result.accessToken && result.refreshToken, 'Authentication did not return a complete session');
  return { accessToken: result.accessToken, refreshToken: result.refreshToken, tenantId: result.tenantId, partnerId: state.partnerId, internalDeviceId: state.internalDeviceId, base: API };
}
export async function requestOtpToFile(email, path, fetchImpl = fetch) {
  await writeFile(path, JSON.stringify({ stage: 'reserved', email, time: new Date().toISOString() }), { flag: 'wx' });
  const state = await requestOtp(email, fetchImpl);
  await writeFile(path, JSON.stringify(state, null, 2));
  return state;
}
async function main([command, first, second]) {
  if (command === 'request') {
    assert(second, 'Use request email challenge.json');
    const state = await requestOtpToFile(first, second);
    console.log(JSON.stringify({ requested: true, requestedAt: state.requestedAt, challengeFile: second }));
    return;
  }
  assert(command === 'authenticate' && first, 'Use authenticate challenge.json; supply OTP on stdin');
  const state = JSON.parse((await readFile(first, 'utf8')).replace(/^\uFEFF/, ''));
  let otp = '';
  for await (const chunk of process.stdin) otp += chunk;
  const session = await authenticate(state, otp.trim());
  writeSession(session, second || sessionFile);
  console.log(JSON.stringify({ authenticated: true, tenantSelected: !!session.tenantId, sessionProtected: true }));
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main(process.argv.slice(2)).catch(error => { console.error(error.message); process.exitCode = 1; });
}
