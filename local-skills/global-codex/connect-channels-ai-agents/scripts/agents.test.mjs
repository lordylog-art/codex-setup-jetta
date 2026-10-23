import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, readFile, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { AgentClient, main, merge, redact, validate } from './agents.mjs';
import { ConnectClient } from '../../connect-channels-chatbots/scripts/connect.mjs';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const id = '11111111-1111-1111-1111-111111111111';
const agent = () => ({ name: 'Customer service', credentialId: id, aiCompanyId: id, companyId: null, partnerId: null, isPrivate: false, promptConfig: { agentName: 'Service', goal: 'Help customers', profile: 'Support expert', shouldSignConversation: false, isTeam: false, showHumanTransferMessage: false, informAboutTransfer: false, version: '0.8', communicationForm: 'NEUTRAL', temperature: 'LOW', messageInterval: 5, fallbackDepartmentId: id, enableHumanTransfer: false, reasoningModelConfig: { modelIntegrationId: 'vendor-model' }, restrictions: [], skills: [], knowledgeIds: [] } });
async function temp(t) {
  const path = await mkdtemp(join(tmpdir(), 'connect-ai-'));
  t.after(() => rm(path, { recursive: true, force: true }));
  return path;
}

test('plan is local and needs no session; variable models and no knowledge are valid', async t => {
  const file = join(await temp(t), 'input.json');
  await writeFile(file, JSON.stringify(agent()));
  const result = await main(['plan', file], () => { throw new Error('Must not authenticate'); });
  assert.equal(result.valid, true);
  assert.equal(result.runtimeExecutionProven, false);
  assert.equal(result.payload.promptConfig.reasoningModelConfig.modelIntegrationId, 'vendor-model');
});

test('merge preserves unknowns and secrets; arrays replace only when explicit', () => {
  const current = { promptConfig: { future: { mode: 'new' }, skills: [{ config: { mcp: { authentication: { token: 'secret' } } } }], restrictions: ['one'] } };
  const output = merge(current, { promptConfig: { future: { second: true } } });
  assert.deepEqual(output.promptConfig.skills, current.promptConfig.skills);
  assert.deepEqual(output.promptConfig.future, { mode: 'new', second: true });
  assert.deepEqual(merge(output, { promptConfig: { restrictions: [] } }).promptConfig.restrictions, []);
  assert(!JSON.stringify(redact(output)).includes('secret'));
  assert.throws(() => merge(output, { password: '[redacted]' }), /redacted/);
  assert.throws(() => merge(output, JSON.parse('{"__proto__":{}}')), /Unsafe/);
});

test('redaction retains maxTokens but excludes keys and arbitrary auth headers', () => {
  const result = redact({ maxTokens: 1000, encryptedApiKey: 'secret', token: 'secret', headers: [{ name: 'x-key', value: 'secret' }], config: { mcp: { auth: { value: 'secret' } } } });
  assert.equal(result.maxTokens, 1000);
  assert(!JSON.stringify(result).includes('secret'));
});

test('validation enforces known enum and human transfer constraints, accepts supervisor', () => {
  const value = agent();
  value.promptConfig.isTeam = true;
  value.promptConfig.subAgents = [id];
  value.promptConfig.subAgentSummary = [{ id, agentSummary: { short: 'Summary', long: 'Description' } }];
  validate(value);
  assert.throws(() => validate({ ...value, promptConfig: { ...value.promptConfig, maxTokens: 149 } }), /maxTokens/);
  assert.throws(() => validate({ ...value, promptConfig: { ...value.promptConfig, enableHumanTransfer: true } }), /defaultDepartmentId/);
});

test('catalog collects all pages and credentials array', async () => {
  const paths = [];
  const client = new AgentClient({ request: async (method, path) => {
    paths.push(path);
    if (path.includes('aicredential')) return [{ id, apiKey: 'hidden' }];
    const page = Number(new URL(path, 'https://example.test').searchParams.get('page'));
    return { items: [{ id: `${page}` }], totalItems: 3, countPages: 3, isLastPage: page === 3, nextPageToken: page < 3 ? `page-${page}` : null };
  } });
  assert.equal((await client.catalog('agents')).length, 3);
  assert(paths[1].includes('nextPageToken=page-1'));
  assert.equal((await client.catalog('credentials')).length, 1);
});

test('repeated pages fail without silently returning an incomplete catalog', async () => {
  const client = new AgentClient({ request: async () => ({ items: [{ id }], isLastPage: false, totalItems: 3 }) });
  await assert.rejects(client.catalog('agents'), /Pagination repeated/);
});

test('unknown create outcome is journaled, never retried, and reconcile includes archived exact names', async t => {
  const file = join(await temp(t), 'journal.json');
  let writes = 0;
  const reads = [];
  const client = new AgentClient({ request: async (method, path) => {
    if (method === 'POST') { writes++; throw new Error('response includes secret'); }
    reads.push(path);
    return { items: [{ id, name: path.includes('archived=true') ? 'Customer service' : 'Customer service extended' }], isLastPage: true };
  } });
  await assert.rejects(client.write('POST', agent(), file), /Write outcome unknown/);
  const journal = JSON.parse(await readFile(file, 'utf8'));
  assert.equal(journal.status, 'outcome-unknown');
  assert(!Object.hasOwn(journal, 'payload'));
  const result = await client.reconcile(journal);
  assert.equal(result.candidates.length, 1);
  assert.equal(result.retryAuthorized, false);
  assert.equal(writes, 1);
  assert.equal(reads.length, 2);
});

test('exclusive journal blocks duplicate writes', async t => {
  const file = join(await temp(t), 'journal.json');
  await writeFile(file, 'existing');
  let calls = 0;
  const client = new AgentClient({ request: async () => { calls++; } });
  await assert.rejects(client.write('POST', agent(), file), { code: 'EEXIST' });
  assert.equal(calls, 0);
  assert.equal(await readFile(file, 'utf8'), 'existing');
});

test('successful write records ID before readback failure', async t => {
  const file = join(await temp(t), 'journal.json');
  const client = new AgentClient({ request: async method => {
    if (method === 'POST') return { id };
    const journal = JSON.parse(await readFile(file, 'utf8'));
    assert.deepEqual(journal.targetIds, [id]);
    assert.equal(journal.status, 'persisted-content-review-required');
    throw new Error('read unavailable');
  } });
  const result = await client.write('POST', agent(), file);
  assert.equal(result.readback, 'unavailable');
  assert.equal(result.status, 'persisted-content-review-required');
});

test('update sends only native outer DTO but entire merged promptConfig with unknown secret fields', async t => {
  const file = join(await temp(t), 'journal.json');
  const current = { ...agent(), id, active: true, unrelatedMetadata: 5 };
  current.promptConfig.future = { key: 'kept', token: 'secret' };
  current.promptConfig.skills = [{ name: 'retained' }];
  let body;
  const client = new AgentClient({ request: async (method, path, input) => {
    if (method === 'PUT') { body = input; return { id }; }
    return current;
  } });
  const result = await client.write('PUT', { promptConfig: { goal: 'new' } }, file, id);
  assert.equal(body.promptConfig.future.token, 'secret');
  assert.equal(body.promptConfig.skills.length, 1);
  assert.equal(body.credentialId, id);
  assert(!Object.hasOwn(body, 'active'));
  assert(!Object.hasOwn(body, 'unrelatedMetadata'));
  assert.equal(result.readbackMatches, false);
  assert(!JSON.stringify(result).includes('secret'));
  assert(!JSON.stringify(result).includes('goal'));
});

test('401 handling remains delegated to the existing transport', async () => {
  let calls = 0;
  const transport = new ConnectClient({ token: 'synthetic-token', fetchImpl: async () => {
    calls++;
    return { ok: false, status: 401, json: async () => ({ apiKey: 'secret' }) };
  } });
  const client = new AgentClient(transport);
  await assert.rejects(client.read(id), error => error.status === 401 && !error.message.includes('secret'));
  assert.equal(calls, 1);
  const source = await readFile(new URL('./agents.mjs', import.meta.url), 'utf8');
  assert(!source.includes('authenticate/refresh'));
});

test('real shared transport does not retry a write on HTTP 503 or leak response errors', async t => {
  const file = join(await temp(t), 'journal.json');
  let calls = 0;
  const transport = new ConnectClient({ token: 'synthetic-token', fetchImpl: async () => {
    calls++;
    return { ok: false, status: 503, json: async () => ({ message: 'secret raw vendor response' }) };
  } });
  await assert.rejects(new AgentClient(transport).write('POST', agent(), file), error => !error.message.includes('secret') && error.message.includes('503'));
  assert.equal(calls, 1);
  assert.equal(JSON.parse(await readFile(file, 'utf8')).status, 'outcome-unknown');
});

test('known skill limits are checked without inventing mandatory knowledge or capabilities', () => {
  const value = agent();
  value.promptConfig.skills = [{ type: 'DATE_TOOLS' }, { type: 'DATE_TOOLS' }];
  assert.throws(() => validate(value), /duplicate exclusive/);
  value.promptConfig.skills = Array.from({ length: 51 }, () => ({ type: 'CALL_API' }));
  assert.throws(() => validate(value), /maximum 50/);
});

test('sandbox output exclusivity prevents execution when the output exists', async t => {
  const folder = await temp(t);
  const input = join(folder, 'request.json'), output = join(folder, 'output.json');
  await writeFile(input, JSON.stringify({ agentConfig: agent(), messages: [], userMessage: 'Hello' }));
  await writeFile(output, 'existing');
  await assert.rejects(main(['sandbox', input, output], () => { throw new Error('Must not execute'); }), { code: 'EEXIST' });
});

test('array replacement rejects nested redaction markers regardless of capitalization', async t => {
  for (const marker of ['[redacted]', '[REDACTED]']) {
    assert.throws(() => merge({}, { skills: [{ config: { headers: [{ key: 'x-api-key', value: marker }] } }] }), /redacted/);
    assert.throws(() => merge({}, { skills: [{ config: { mcp: { auth: { key: 'token', value: marker } } } }] }), /redacted/);
  }
  assert.throws(() => merge({}, JSON.parse('{"skills":[{"config":{"constructor":{"token":"value"}}}]}')), /Unsafe/);
  const file = join(await temp(t), 'journal.json');
  let calls = 0;
  const client = new AgentClient({ request: async () => { calls++; } });
  const input = agent();
  input.promptConfig.skills = [{ config: { headers: [{ value: '[REDACTED]' }] } }];
  await assert.rejects(client.write('POST', input, file), /redacted/);
  assert.equal(calls, 0);
});

test('pagination rejects contradictory completion metadata', async () => {
  for (const data of [
    { items: [1], totalItems: 500, countPages: 5, isLastPage: true },
    { items: [{ id }], totalItems: 1, countPages: 2, isLastPage: false },
    { items: [{ id }], totalItems: 2, countPages: 1, isLastPage: false },
  ]) {
    const client = new AgentClient({ request: async () => data });
    await assert.rejects(client.catalog('agents'), /contradicts/);
  }
});

test('pagination deduplicates identical IDs and rejects conflicting duplicate content', async () => {
  const item = { id, name: 'one' }, other = { id: 'other', name: 'two' };
  let calls = 0;
  const client = new AgentClient({ request: async () => {
    calls++;
    return calls === 1 ? { items: [item], totalItems: 2, countPages: 2, isLastPage: false } : { items: [item, other], totalItems: 2, countPages: 2, isLastPage: true };
  } });
  assert.deepEqual(await client.catalog('agents'), [item, other]);
  const duplicate = new AgentClient({ request: async () => [item, item] });
  assert.deepEqual(await duplicate.catalog('credentials'), [item]);
  const conflict = new AgentClient({ request: async () => [item, { ...item, name: 'changed' }] });
  await assert.rejects(conflict.catalog('credentials'), /conflicting duplicate/);
});

test('CLI invalid JSON never echoes source secret even when SyntaxError begins Unexpected', async t => {
  const file = join(await temp(t), 'invalid.json');
  await writeFile(file, '{"apiKey": SYNTHETIC_SECRET }');
  const result = spawnSync(process.execPath, [fileURLToPath(new URL('./agents.mjs', import.meta.url)), 'plan', file], { encoding: 'utf8' });
  assert.equal(result.status, 1);
  assert(!result.stdout.includes('SYNTHETIC_SECRET'));
  assert(!result.stderr.includes('SYNTHETIC_SECRET'));
  assert.equal(result.stderr.trim(), 'Operation failed; preserve files and diagnose without automatic retries');
});

test('missing profile or goal, malformed boolean, nickname, skill and steps fail locally', () => {
  for (const key of ['goal', 'profile']) for (const value of [undefined, '', '   ']) {
    const input = agent();
    input.promptConfig[key] = value;
    assert.throws(() => validate(input), /required/);
  }
  const input = agent();
  input.promptConfig.shouldSignConversation = 'true';
  assert.throws(() => validate(input), /boolean/);
  input.promptConfig.shouldSignConversation = true;
  assert.throws(() => validate(input), /nickname/);
  input.promptConfig.nickName = 'Service';
  input.promptConfig.skills = [{ name: 'No config' }];
  assert.throws(() => validate(input), /skill shape/);
  input.promptConfig.skills = [{ name: 'Calendar', description: '', type: 'DATE_TOOLS', active: true, supressMessage: false, config: {}, futureNativeField: true }];
  input.promptConfig.requiredSteps = [{ order: 0, step: '   ' }];
  assert.throws(() => validate(input), /required step/);
  input.promptConfig.requiredSteps = [{ order: 0, step: 'Greet' }];
  assert.equal(validate(input).promptConfig.skills[0].futureNativeField, true);
});
