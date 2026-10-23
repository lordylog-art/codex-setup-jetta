import assert from 'node:assert/strict';
import { readFile, open } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { pathToFileURL } from 'node:url';
import { ConnectClient } from '../../connect-channels-chatbots/scripts/connect.mjs';

const ROOT = '/ai/v1/aiagent';
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const FIELDS = ['credentialId', 'name', 'promptConfig', 'aiCompanyId', 'companyId', 'partnerId', 'isPrivate'];
const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const hash = value => createHash('sha256').update(JSON.stringify(value)).digest('hex');
const json = async path => JSON.parse((await readFile(path, 'utf8')).replace(/^\uFEFF/, ''));
const agentPath = id => { assert(UUID.test(id), 'Agent ID must be a UUID'); return `${ROOT}/${id}`; };

export function redact(value, parent = '') {
  if (Array.isArray(value)) return value.map(item => redact(item, parent));
  if (!object(value)) return value;
  // Header and MCP authentication values can use arbitrary vendor-defined names.
  return Object.fromEntries(Object.entries(value).map(([key, item]) => [key,
    /apikey|encryptedapikey|access.?token|refresh.?token|password|secret|authorization|cookie|^token$/i.test(key)
      || /^(headers?|auth|authentication)$/i.test(key)
      || (/^(auth|authentication|headers?)$/i.test(parent)) ? '[redacted]' : redact(item, key)]));
}

function validateInput(value) {
  assert(!(typeof value === 'string' && /^\[redacted\]$/i.test(value)), 'Replace redacted placeholders using the original source before writing');
  if (value && typeof value === 'object') for (const [key, nested] of Object.entries(value)) {
    assert(!['__proto__', 'constructor', 'prototype'].includes(key), 'Unsafe object key');
    validateInput(nested);
  }
}

export function merge(base, patch) {
  validateInput(patch);
  if (!object(patch)) return structuredClone(patch);
  const result = object(base) ? structuredClone(base) : {};
  for (const [key, value] of Object.entries(patch)) {
    result[key] = object(value) ? merge(result[key], value) : structuredClone(value);
  }
  return result;
}

export function payload(agent) {
  return Object.fromEntries(FIELDS.filter(key => Object.hasOwn(agent, key)).map(key => [key, agent[key]]));
}

export function validate(agent, existing) {
  assert(object(agent) && object(agent.promptConfig), 'Native agent and promptConfig are required');
  assert(typeof agent.name === 'string' && agent.name.trim(), 'Agent name is required');
  for (const key of ['credentialId', 'aiCompanyId']) assert(UUID.test(agent[key]), `Select a real ${key}`);
  const p = agent.promptConfig;
  for (const key of ['goal', 'profile']) assert(typeof p[key] === 'string' && p[key].trim(), `Invalid required ${key}`);
  assert(typeof agent.isPrivate === 'boolean', 'Invalid isPrivate boolean');
  for (const key of ['shouldSignConversation', 'isTeam', 'showHumanTransferMessage', 'informAboutTransfer']) assert(typeof p[key] === 'boolean', `Invalid ${key} boolean`);
  if (p.shouldNotifyAboutHandoff != null) assert(typeof p.shouldNotifyAboutHandoff === 'boolean', 'Invalid shouldNotifyAboutHandoff boolean');
  assert(typeof p.agentName === 'string' && p.agentName.trim(), 'promptConfig.agentName is required');
  assert(['0.5', '0.6', '0.7', '0.8'].includes(p.version), 'Unsupported agent version');
  if (Number(p.version) >= 0.7 && p.shouldSignConversation) assert(typeof p.nickName === 'string' && p.nickName.trim(), 'Invalid signed agent nickname');
  assert(['SUPPORTIVE', 'NEUTRAL', 'FORMAL'].includes(p.communicationForm), 'Invalid communicationForm');
  assert(p.responseLength == null || ['SHORT', 'LONG'].includes(p.responseLength), 'Invalid responseLength');
  assert(['NO_CREATIVITY', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH'].includes(p.temperature), 'Invalid temperature');
  assert(Number.isInteger(p.messageInterval) && ((p.messageInterval >= 0 && p.messageInterval <= 10) || [15, 20, 25, 30, 35, 40].includes(p.messageInterval)), 'Invalid messageInterval');
  assert(p.maxTokens == null || (Number.isInteger(p.maxTokens) && p.maxTokens >= 150 && p.maxTokens <= 2e9), 'maxTokens must be an integer from 150 to 2000000000');
  assert(UUID.test(p.fallbackDepartmentId), 'Select a real fallbackDepartmentId');
  assert(typeof p.enableHumanTransfer === 'boolean', 'enableHumanTransfer must be boolean');
  if (p.enableHumanTransfer) assert(UUID.test(p.defaultDepartmentId), 'Human transfer needs defaultDepartmentId');
  if (p.enableHumanTransfer && p.showHumanTransferMessage) assert(typeof p.humanTransferMessage === 'string' && p.humanTransferMessage.trim(), 'Human transfer message is required');
  assert(typeof p.reasoningModelConfig?.modelIntegrationId === 'string' && p.reasoningModelConfig.modelIntegrationId.trim(), 'Select a reasoning model from the provider catalog');
  for (const key of ['reasoningModelConfig', 'formattingModelConfig']) {
    if (p[key]?.credentialId != null) assert(UUID.test(p[key].credentialId), 'Model credentialId must be UUID');
  }
  for (const key of ['restrictions', 'requiredSteps', 'skills', 'knowledgeIds', 'subAgents', 'subAgentSummary']) if (p[key] != null) assert(Array.isArray(p[key]), `${key} must be an array`);
  const unchanged = key => existing && JSON.stringify(p[key]) === JSON.stringify(existing.promptConfig?.[key]);
  if (!unchanged('skills')) {
    assert((p.skills?.length ?? 0) <= 50, 'Invalid skill count: maximum 50');
    for (const type of ['DATE_TOOLS', 'FOLLOW_UP']) assert((p.skills ?? []).filter(skill => skill.type === type).length <= 1, 'Invalid duplicate exclusive skill type');
    for (const skill of p.skills ?? []) assert(object(skill) && typeof skill.name === 'string' && skill.name.trim() && typeof skill.description === 'string' && typeof skill.type === 'string' && skill.type.trim() && typeof skill.active === 'boolean' && typeof skill.supressMessage === 'boolean' && object(skill.config), 'Invalid native skill shape');
  }
  if (!unchanged('requiredSteps')) for (const step of p.requiredSteps ?? []) assert(object(step) && Number.isInteger(step.order) && step.order >= 0 && typeof step.step === 'string' && step.step.trim(), 'Invalid required step');
  if (p.restrictions) assert(p.restrictions.every(rule => typeof rule === 'string'), 'Invalid restrictions');
  if (!unchanged('knowledgeIds')) assert((p.knowledgeIds?.length ?? 0) <= 50, 'Invalid knowledge count: maximum 50');
  if (p.knowledgeIds) assert(p.knowledgeIds.every(id => UUID.test(id)), 'knowledgeIds must be UUIDs');
  if (p.subAgents) assert(p.subAgents.every(id => UUID.test(id)), 'subAgents must be UUIDs');
  if (p.isTeam) assert(p.subAgents?.length, 'Supervisor needs selected subAgents');
  return payload(agent);
}

async function newJson(path, value) {
  const handle = await open(path, 'wx', 0o600);
  try { await handle.writeFile(JSON.stringify(value, null, 2)); } finally { await handle.close(); }
}

export class AgentClient {
  constructor(client = new ConnectClient()) { this.client = client; }
  request(method, path, body) { return this.client.request(method, path, body); }
  async pages(path, params = {}) {
    const items = [];
    let page = 1, nextPageToken;
    const seen = new Set(), ids = new Map();
    let totalItems, countPages;
    const collect = batch => {
      for (const item of batch) {
        if (item?.id != null) {
          assert(!ids.has(item.id) || hash(ids.get(item.id)) === hash(item), 'Pagination returned conflicting duplicate IDs');
          if (ids.has(item.id)) continue;
          ids.set(item.id, item);
        }
        items.push(item);
      }
    };
    while (true) {
      const query = new URLSearchParams({ ...params, page: String(page), pageSize: '100', ...(nextPageToken ? { nextPageToken } : {}) });
      const data = await this.request('GET', `${path}?${query}`);
      if (Array.isArray(data)) { collect(data); return items; }
      assert(Array.isArray(data?.items), 'Unexpected catalog shape');
      if (data.totalItems != null) {
        assert(Number.isInteger(data.totalItems) && data.totalItems >= 0 && (totalItems === undefined || totalItems === data.totalItems), 'Pagination totalItems is invalid or changed');
        totalItems = data.totalItems;
      }
      if (data.countPages != null) {
        assert(Number.isInteger(data.countPages) && data.countPages >= 0 && (countPages === undefined || countPages === data.countPages), 'Pagination countPages is invalid or changed');
        countPages = data.countPages;
      }
      if (data.page != null) assert(data.page === page, 'Pagination returned wrong page');
      if (data.isLastPage != null) assert(typeof data.isLastPage === 'boolean', 'Pagination invalid isLastPage');
      const fingerprint = hash(data.items);
      assert(!seen.has(fingerprint) || !data.items.length, 'Pagination repeated a page; catalog is incomplete');
      seen.add(fingerprint);
      collect(data.items);
      const flags = [data.isLastPage, countPages === undefined ? undefined : page >= countPages, totalItems === undefined ? undefined : items.length >= totalItems].filter(flag => flag !== undefined);
      assert(!(flags.includes(true) && flags.includes(false)), 'Pagination metadata contradicts completeness');
      if (flags.includes(true)) {
        assert(totalItems === undefined || items.length === totalItems, 'Pagination unique item total differs');
        return items;
      }
      assert(data.items.length || data.nextPageToken, 'Pagination ended without completion metadata');
      nextPageToken = data.nextPageToken;
      page++;
    }
  }
  catalog(kind) {
    const paths = { agents: ROOT, companies: '/ai/v1/aicompany', credentials: '/ai/v1/aicredential', knowledge: '/ai/v1/aiKnowledge' };
    assert(paths[kind], 'Use catalog agents|companies|credentials|knowledge');
    return this.pages(paths[kind], kind === 'agents' ? { archived: 'false', orderByDesc: 'createdat' } : {});
  }
  async read(id) {
    const result = await this.request('GET', agentPath(id));
    assert(result?.id === id, 'Wrong agent returned');
    return result;
  }
  async write(method, input, journalPath, id) {
    assert(journalPath, 'A new journal path is required');
    if (id) agentPath(id);
    const existing = id ? await this.read(id) : undefined;
    const body = validate(merge(existing ?? {}, input), existing);
    const journal = { method, status: 'planned', inputHash: hash(body), name: body.name, targetIds: id ? [id] : [], createdAt: new Date().toISOString() };
    // Keep one exclusive handle: an existing journal can never authorize another write.
    const handle = await open(journalPath, 'wx', 0o600);
    const save = async () => { await handle.truncate(0); await handle.write(JSON.stringify(journal, null, 2), 0, 'utf8'); await handle.sync(); };
    try {
      await save();
      journal.status = 'write-attempted';
      await save();
      let result;
      try { result = await this.request(method, id ? agentPath(id) : ROOT, body); }
      catch (error) {
        journal.status = 'outcome-unknown';
        if (Number.isInteger(error.status)) journal.httpStatus = error.status;
        await save();
        const failure = new Error(`Write outcome unknown; reconcile journal before deciding any next action${journal.httpStatus ? ` (HTTP ${journal.httpStatus})` : ''}`);
        if (journal.httpStatus) failure.status = journal.httpStatus;
        throw failure;
      }
      if (UUID.test(result?.id)) journal.targetIds = [result.id];
      journal.status = 'persisted-content-review-required';
      await save();
      if (!journal.targetIds.length) return { ...journal, readback: 'ID missing; reconcile by exact name' };
      try {
        const saved = await this.read(journal.targetIds[0]);
        journal.observedHash = hash(payload(saved));
        journal.readbackMatches = journal.inputHash === journal.observedHash;
        await save();
      } catch { journal.readback = 'unavailable'; await save(); }
      return journal;
    } finally { await handle.close(); }
  }
  async reconcile(journal) {
    assert(object(journal) && ['POST', 'PUT'].includes(journal.method), 'Invalid journal');
    const ids = journal.targetIds ?? [];
    if (ids.length) {
      const agents = [];
      for (const id of ids) agents.push(await this.read(id));
      return { status: 'persisted-content-review-required', retryAuthorized: false, agents: redact(agents), inputHash: journal.inputHash };
    }
    assert(typeof journal.name === 'string' && journal.name, 'Exact journal name is required');
    const active = await this.pages(ROOT, { archived: 'false' });
    const archived = await this.pages(ROOT, { archived: 'true' });
    const candidates = [...active, ...archived].filter(agent => agent.name === journal.name);
    return { status: candidates.length ? 'persisted-content-review-required' : 'outcome-unknown', retryAuthorized: false, candidates: redact(candidates) };
  }
}

export async function main([command, first, second, third], makeClient = () => new AgentClient()) {
  if (command === 'plan') {
    const input = validate(merge({}, await json(first)));
    return { valid: true, inputHash: hash(input), payload: redact(input), publicationMayStartOnSave: true, runtimeExecutionProven: false };
  }
  if (command === 'create') return makeClient().write('POST', await json(first), second);
  if (command === 'update') return makeClient().write('PUT', await json(second), third, first);
  if (command === 'reconcile') return makeClient().reconcile(await json(first));
  let result, output;
  if (command === 'catalog') { result = await makeClient().catalog(first); output = second; }
  else if (command === 'read') { result = await makeClient().read(first); output = second; }
  else if (command === 'knowledge-read') { assert(UUID.test(first), 'Knowledge ID must be UUID'); result = await makeClient().request('GET', `/ai/v1/aiKnowledge/${first}`); output = second; }
  else if (command === 'knowledge-contents') { assert(UUID.test(first), 'Knowledge ID must be UUID'); result = await makeClient().pages(`/ai/v1/aiKnowledge/${first}/content`); output = second; }
  else if (command === 'sandbox') {
    assert(second, 'Sandbox requires a new output file; execution can incur provider costs');
    const request = await json(first);
    validateInput(request);
    assert(object(request) && object(request.agentConfig), 'Invalid sandbox agentConfig');
    validate(request.agentConfig);
    assert(Array.isArray(request.messages) && request.messages.every(message => typeof message.role === 'string' && typeof message.content === 'string'), 'Invalid sandbox messages');
    assert(typeof request.userMessage === 'string' && request.userMessage.trim(), 'Invalid sandbox userMessage');
    const handle = await open(second, 'wx', 0o600);
    try {
      await handle.writeFile(JSON.stringify({ status: 'execution-attempted', mayIncurProviderCosts: true }));
      await handle.sync();
      result = await makeClient().request('POST', `${ROOT}/sandbox`, request);
      await handle.truncate(0);
      await handle.write(JSON.stringify(redact(result), null, 2), 0, 'utf8');
      return { output: second, status: 'execution-response-received', runtimeExecutionProven: false };
    } catch (error) {
      const failure = new Error('Sandbox outcome unknown; preserve output marker and do not retry automatically');
      if (Number.isInteger(error.status)) failure.status = error.status;
      throw failure;
    }
    finally { await handle.close(); }
  } else throw new Error('Use catalog|read|plan|create|update|reconcile|knowledge-read|knowledge-contents|sandbox');
  result = redact(result);
  if (output) { await newJson(output, result); return { output, written: true }; }
  return result;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main(process.argv.slice(2)).then(result => console.log(JSON.stringify(result, null, 2))).catch(error => {
    // Transport and parser errors may contain source data; never print them verbatim.
    console.error(`Operation failed${error.code === 'EEXIST' ? ': output or journal already exists' : ''}${Number.isInteger(error.status) ? ` (HTTP ${error.status})` : ''}; preserve files and diagnose without automatic retries`);
    process.exitCode = 1;
  });
}
