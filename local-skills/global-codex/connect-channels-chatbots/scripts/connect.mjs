import assert from 'node:assert/strict';
import { readFile, writeFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
import { readSession, writeSession, sessionFile } from './session.mjs';

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const BASES = ['https://api.wts.chat', 'https://chatbot.wts.chat', 'https://api.app.connectchannels.com.br'];
const NODE_TYPES = ['EMPTY', 'CONTENT', 'QUESTION', 'MENU', 'ACTION', 'CONDITION', 'TEMPLATE', 'AI_AGENT', 'AI_TEAM'];
const ACTION_TYPES = ['WEBHOOK', 'TRANSFER_SESSION', 'COMPLETE_SESSION', 'NAVIGATION_RETURN', 'SET_CONTACT_TAG', 'CARD', 'DELAY', 'GOTO_RETURN_POINT', 'SEQUENCE_OPERATION', 'AGGREGATE_MESSAGES', 'TRANSFER_CHATBOT', 'SET_METADATA'];
const CHANNEL_TYPES = ['DIALOG360_WHATSAPP', 'CLOUDAPI_WHATSAPP', 'ZAPI_WHATSAPP', 'EVOLUTIONAPI_WHATSAPP', 'INSTAGRAM', 'MESSENGER', 'WEBCHAT'];
const botPath = id => { assert(UUID.test(id), 'Invalid chatbot ID'); return `/chat/v1/chatbot/${id}`; };
const json = async path => JSON.parse((await readFile(path, 'utf8')).replace(/^\uFEFF/, ''));

function handles(node) {
  const pairs = [];
  const add = (value, target) => { if (value?.clientGeneratedId) pairs.push([value.clientGeneratedId, target]); };
  const aggregation = value => { if (value?.enableFallbackNodeGroup) add(value, value.fallbackNodeGroupClientId); };
  const action = node.action;
  if (node.type === 'ACTION') {
    if (action.type === 'WEBHOOK') for (const target of [action.webhook?.failTarget, action.webhook?.successTarget, ...(action.webhook?.customTargets ?? [])]) add(target, target?.clientGroupId);
    if (action.type === 'CARD') add(action.card, action.card?.fallbackNodeGroupClientId);
    if (action.type === 'AGGREGATE_MESSAGES') aggregation(action.aggregation);
  }
  if (node.type === 'MENU' || node.type === 'QUESTION') {
    const value = node.menu ?? node.question;
    for (const option of value?.options ?? []) add(option, option.targetClientGroupId);
    aggregation(value?.aggregation);
    add(value?.dynamicMessage, value?.dynamicMessage?.fallbackNodeGroupClientId);
  }
  if (node.type === 'CONDITION') for (const condition of node.conditions ?? []) add(condition, condition.target?.clientGroupId);
  if (node.type === 'TEMPLATE') aggregation(node.template?.aggregation);
  if (node.type === 'AI_AGENT' || node.type === 'AI_TEAM') {
    for (const target of node.aiAgentConfig?.customTargets?.targets ?? []) add(target, target.clientGroupId);
    aggregation(node.aiAgentConfig?.aggregation);
  }
  return pairs;
}

export function validateVersion(version, builderType) {
  assert(version && Array.isArray(version.nodes) && version.nodes.length, 'Version needs nodes');
  const advanced = builderType === 'HELENA_ADVANCED';
  const groups = new Set();
  const ids = new Set();
  if (advanced) {
    assert(Array.isArray(version.groups) && version.groups.length, 'Advanced version needs groups');
    for (const group of version.groups) {
      assert(UUID.test(group.clientGeneratedId), 'Group needs a clientGeneratedId UUID');
      assert(!groups.has(group.clientGeneratedId), 'Duplicate group ID');
      groups.add(group.clientGeneratedId);
    }
    assert(groups.has(version.startGroupClientGeneratedId), 'Start group does not exist');
    assert(Array.isArray(version.edges), 'Advanced version needs edges');
    assert(version.edges.some(edge => edge.clientSourceGroupId === 'BEGIN-GROUP' && !edge.clientSourceId && edge.clientTargetGroupId === version.startGroupClientGeneratedId), 'Start group needs the BEGIN-GROUP edge');
    for (const edge of version.edges) {
      assert(groups.has(edge.clientTargetGroupId), 'Edge points to missing group');
      assert(edge.clientSourceGroupId === 'BEGIN-GROUP' || groups.has(edge.clientSourceGroupId), 'Edge starts in missing group');
    }
    for (const trigger of version.triggers?.channelTriggers ?? []) assert(UUID.test(trigger.channelId), 'Trigger needs a real channel ID');
  }
  function visit(nodes) {
    for (const node of nodes) {
      assert(NODE_TYPES.includes(node.type), `Unsupported node type: ${node.type}`);
      assert(UUID.test(node.clientGeneratedId), 'Node needs a clientGeneratedId UUID');
      assert(!ids.has(node.clientGeneratedId), 'Duplicate node ID');
      ids.add(node.clientGeneratedId);
      if (advanced) assert(groups.has(node.groupClientGeneratedId), 'Node belongs to missing group');
      if (node.type === 'ACTION') assert(ACTION_TYPES.includes(node.action?.type), 'Unsupported action type');
      if(node.action?.type==='CARD'){
        const card=node.action.card;
        for(const field of [card?.title,card?.description,card?.dueDate,...(card?.customFieldsValues??[])]){
          const params=Array.isArray(field?.params)?field.params:field?.params?.items??[];
          assert(!params.some(p=>p.type==='QUESTION'),'CARD fields do not accept QUESTION parameters; store the answer in SESSION_METADATA first');
        }
      }
      if (['MENU','QUESTION'].includes(node.type)) {
        const value=node.menu??node.question;
        // shortcut: E-mail option labels reproduced HTTP 500, revisit after fresh vendor proof.
        for(const option of value?.options??[]) assert(!/\bE-mail\b/i.test(option.text??''),'Option label E-mail reproduced vendor HTTP 500; use Email (observed hyphen compatibility case)');
        if(value?.valueType==='FILE') assert(!value.interactiveType,'FILE questions cannot be interactive');
      }
      if (node.type === 'CONTENT') {
        assert(['TEXT', 'AUDIO', 'IMAGE', 'VIDEO', 'DOCUMENT'].includes(node.message?.type), 'Invalid message type');
        if (node.message.type === 'TEXT') assert(node.message.text?.trim(), 'Text message is empty');
        else assert(node.message.fileId || (advanced && node.message.fileIds?.length), 'Media requires uploaded file IDs');
      }
      if (['AI_AGENT', 'AI_TEAM'].includes(node.type)) assert(UUID.test(node.aiAgentConfig?.aiAgentId), 'AI node needs an existing agent/team ID');
      for (const group of node.children ?? []) visit(group.nodes ?? []);
    }
  }
  visit(version.nodes);
  if (advanced) {
    function references(value) {
      if (!value || typeof value !== 'object') return;
      for (const [key, target] of Object.entries(value)) {
        if (target && ['targetClientGroupId', 'clientGroupId', 'fallbackNodeGroupClientId'].includes(key)) assert(groups.has(target), `Missing group reference: ${key}`);
        if (target && ['targetClientNodeId', 'questionNodeClientId', 'templateNodeClientId'].includes(key)) assert(ids.has(target), `Missing node reference: ${key}`);
        references(target);
      }
    }
    references(version.nodes);
    references(version.config);
    for (const edge of version.edges) {
      if (edge.clientSourceGroupId === 'BEGIN-GROUP') {
        if (edge.clientSourceId) assert(version.config?.aggregation?.fallbackNodeGroupClientId === edge.clientTargetGroupId, 'Begin fallback destination differs');
        continue;
      }
      const sourceNodes = version.nodes.filter(node => node.groupClientGeneratedId === edge.clientSourceGroupId);
      if (!edge.clientSourceId || edge.clientSourceId === `${edge.clientSourceGroupId}-EXIT`) {
        const targetNodes = version.nodes.filter(node => node.groupClientGeneratedId === edge.clientTargetGroupId);
        assert(sourceNodes.some(node => node.action?.type === 'GOTO_RETURN_POINT' && targetNodes.some(target => target.clientGeneratedId === node.action.targetClientNodeId)), 'Group exit needs matching navigation action');
        continue;
      }
      const targets = sourceNodes.flatMap(handles).filter(([handle]) => handle === edge.clientSourceId);
      assert(targets.length === 1, 'Edge source handle is missing or ambiguous');
      assert(targets[0][1] === edge.clientTargetGroupId, 'Edge destination differs from the executable node target');
    }
  }
  return version;
}

export function validateSpec(spec) {
  assert(['attendance', 'automation'].includes(spec.kind), 'kind must be attendance or automation');
  const create = spec.kind === 'automation' ? spec.create?.chatbot : spec.create;
  assert(create?.name?.trim(), 'Chatbot name is required');
  assert(UUID.test(create.defaultDepartmentId), 'Select a real default department');
  assert(['HELENA_SIMPLE', 'HELENA_ADVANCED'].includes(create.builderType), 'Select a builder type');
  assert(create.channelTypes?.length && create.channelTypes.every(type => CHANNEL_TYPES.includes(type)), 'Select supported channel types');
  if (spec.kind === 'automation') {
    assert(UUID.test(spec.create.channelId), 'Automation needs a real channel ID');
    assert(typeof spec.create.usage === 'string' && spec.create.usage.split(',').every(value => ['API', 'MANUAL', 'CAMPAIGN', 'SEQUENCE'].includes(value)), 'Invalid automation usage');
    assert(['COMPANY', 'DEPARTMENT'].includes(spec.create.scope), 'Automation scope is required');
    if (spec.create.scope === 'DEPARTMENT') assert(spec.create.scopeIds?.length && spec.create.scopeIds.every(value => UUID.test(value)), 'Automation needs real scope department IDs');
  }
  validateVersion(spec.version, create.builderType);
  // Unknown native fields are preserved: the vendor, not this helper, owns the full schema.
  return spec;
}

export function auditReadback(saved) {
  assert(saved.metadata?.builderType==='HELENA_ADVANCED','Readback audit requires HELENA_ADVANCED');
  const v=saved.content,groups=new Map(v.groups.map(g=>[g.clientGeneratedId,g])),nodes=new Map(v.nodes.map(n=>[n.clientGeneratedId,n]));
  const start=[...groups.values()].find(g=>g.id===v.startGroupId);
  validateVersion({...v,startGroupClientGeneratedId:v.startGroupClientGeneratedId??start?.clientGeneratedId},'HELENA_ADVANCED');
  let legacyAdjacencyDifferences=0;
  for(const g of groups.values()){
    const ordered=v.nodes.filter(n=>n.groupClientGeneratedId===g.clientGeneratedId).sort((a,b)=>a.order-b.order);
    assert(ordered.length,'Persisted group is empty');
    ordered.forEach((n,i)=>{
      assert.equal(n.order,i,'Persisted group order is not contiguous');
      assert.equal(n.groupId,g.id,'Persisted node belongs to a different native group');
      if(n.nextNodeId!==(ordered[i+1]?.id??null)||n.previousNodeId!==(ordered[i-1]?.id??null))legacyAdjacencyDifferences++;
    });
  }
  for(const n of v.nodes){
    for(const o of n.menu?.options??[]){
      if(o.type==='NAVIGATION'){
        assert.equal(o.targetGroupId,groups.get(o.targetClientGroupId)?.id,'MENU resolved destination differs from client destination');
        assert(v.edges.some(e=>e.clientSourceGroupId===n.groupClientGeneratedId&&e.clientSourceId===o.clientGeneratedId&&e.clientTargetGroupId===o.targetClientGroupId),'MENU navigation has no matching edge');
      }
    }
    if(n.action?.type==='GOTO_RETURN_POINT')assert.equal(n.action.targetNodeId,nodes.get(n.action.targetClientNodeId)?.id,'GOTO resolved destination differs from client destination');
  }
  // Legacy adjacency is diagnostic: real TI conversations traversed correctly despite these differences.
  return {valid:true,groups:groups.size,nodes:nodes.size,edges:v.edges.length,legacyAdjacencyDifferences,runtimeExecutionProven:false};
}

export class ConnectClient {
  constructor({ token = process.env.CONNECT_ACCESS_TOKEN, base = process.env.CONNECT_API_BASE_URL || BASES[0], fetchImpl = fetch } = {}) {
    this.session = token ? null : readSession();
    token ||= this.session?.accessToken;
    assert(token && !/[\r\n]/.test(token), 'Set CONNECT_ACCESS_TOKEN to a user session token');
    assert(BASES.includes(base), 'Unsupported CONNECT_API_BASE_URL');
    this.token = token;
    this.base = base;
    this.fetch = fetchImpl;
  }
  async refreshIfNeeded(force = false) {
    if (!this.session || this.refreshed) return;
    let expires;
    try { expires = JSON.parse(Buffer.from(this.token.split('.')[1], 'base64url')).exp; } catch { if (!force) return; }
    if (!force && (!expires || expires * 1000 > Date.now() + 1800000)) return;
    const response = await this.fetch(`${BASES[0]}/auth/v2/login/authenticate/refresh`, {
      method: 'POST', redirect: 'error', signal: AbortSignal.timeout(30000), headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refreshToken: this.session.refreshToken, tenantId: this.session.tenantId, partnerId: this.session.partnerId, internalDeviceId: this.session.internalDeviceId }),
    });
    assert(response.ok, `Session refresh: HTTP ${response.status}${response.status === 401 ? '; authenticate again' : '; preserve the session and diagnose the error'}`);
    const result = await response.json();
    assert(result.accessToken && result.refreshToken, 'Session refresh did not return complete tokens');
    assert(result.tenantId === this.session.tenantId, 'Session refresh changed the company identity');
    const renewed = { ...this.session, accessToken: result.accessToken, refreshToken: result.refreshToken, tenantId: result.tenantId };
    writeSession(renewed, sessionFile);
    this.session = renewed;
    this.token = result.accessToken;
    this.refreshed = true;
  }
  async request(method, path, body) {
    await this.refreshIfNeeded();
    assert(path.startsWith('/') && !path.startsWith('//') && !/[\r\n]/.test(path), 'Invalid API path');
    const send = () => this.fetch(this.base + path, {
      method, redirect: 'error', signal: AbortSignal.timeout(30000),
      headers: { Authorization: `Bearer ${this.token}`, 'Content-Type': 'application/json' },
      ...(body === undefined ? {} : { body: JSON.stringify(body) }),
    });
    let response = await send();
    if (response.status === 401 && this.session && !this.refreshed) {
      await this.refreshIfNeeded(true);
      response = await send();
    }
    if(!response.ok){
      let detail;try{detail=await response.json();}catch{}
      const requestId=detail?.id?.value??detail?.id;
      const vendorCode=detail?.key;
      const safeId=UUID.test(requestId??'')?requestId:undefined;
      const safeCode=/^[A-Z0-9_]{1,80}$/.test(vendorCode??'')?vendorCode:undefined;
      const error=new Error(`${method} ${path.split('?')[0]}: HTTP ${response.status}${safeCode?`; ${safeCode}`:''}${safeId?`; request ${safeId}`:''}`);
      Object.assign(error,{status:response.status,requestId:safeId,vendorCode:safeCode});
      throw error;
    }
    if (response.status === 204) return null;
    return response.json();
  }
  async read(id) {
    const path = botPath(id);
    const metadata = await this.request('GET', `${path}?deployedVersion=false`);
    const contentPath = metadata.builderType === 'HELENA_SIMPLE'
      ? `${path}/version/${metadata.versionId}?includeDetails=All&deployedVersion=false`
      : `${path}/nodes?includeDetails=All`;
    const content = await this.request('GET', contentPath);
    return { metadata, content };
  }
  async save(id, version, journal) {
    const path = botPath(id);
    const metadata = await this.request('GET', `${path}?deployedVersion=false`);
    assert(metadata.id === id, 'Wrong chatbot returned');
    if (metadata.automation) {
      const result = await this.request('GET', `/chat/v1/chatbot/automation?chatbotId=${id}&page=1&pageSize=2&archived=false`);
      assert(result.items?.length === 1, 'Automation identity is missing or ambiguous');
      metadata.automationDetails = result.items[0];
      assert(metadata.automationDetails.chatbotId === id, 'Wrong automation identity returned');
    }
    // New automation metadata includes its sending channel even before publication or use.
    const draftAssociation = metadata.automation && metadata.publishStatus === 'NOT_PUBLISHED'
      && metadata.automationDetails.inUse === false
      && (metadata.channelIds ?? []).every(channelId => channelId === metadata.automationDetails.channelId);
    assert(!metadata.archived && (!metadata.channelIds?.length || draftAssociation) && !metadata.automationDetails?.inUse, 'Create a separate draft before editing a linked or archived chatbot');
    validateVersion(version, metadata.builderType);
    await journal({ stage: 'requesting-upload', chatbotId: id });
    const upload = await this.request('GET', `${path}/version/url`);
    const url = new URL(upload.url);
    assert(url.protocol === 'https:' && !url.username && !url.password && !/^localhost$|\.local$|^[\d.]+$|:/.test(url.hostname), 'Invalid upload destination');
    await journal({ stage: 'uploading', chatbotId: id });
    const response = await this.fetch(url.href, {
      method: 'PUT', redirect: 'error', signal: AbortSignal.timeout(30000),
      headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(version),
    });
    assert(response.ok, `Version upload: HTTP ${response.status}`);
    await journal({ stage: 'registering-version', chatbotId: id });
    const confirmation = metadata.builderType === 'HELENA_SIMPLE' ? upload : { key: upload.key, url: upload.url };
    await this.request('POST', `${path}/version/url`, confirmation);
    const saved = await this.read(id);
    await journal({ stage: 'saved-content-review-required', chatbotId: id, versionId: saved.metadata.versionId });
    return saved;
  }
  async create(spec, journal) {
    validateSpec(spec);
    await journal({ stage: 'creating' });
    const result = await this.request('POST', `/chat/v1/chatbot${spec.kind === 'automation' ? '/automation' : ''}`, spec.create);
    const chatbot = spec.kind === 'automation' ? result.chatbot : result;
    assert(UUID.test(chatbot?.id), 'Creation response did not identify the chatbot; reconcile before retrying');
    await journal({ stage: 'created', chatbotId: chatbot.id });
    return this.save(chatbot.id, spec.version, journal);
  }
}

async function main(args) {
  const [command, first, second, third] = args;
  if(command==='audit')return console.log(JSON.stringify(auditReadback(await json(first))));
  if (command === 'plan') {
    const spec = validateSpec(await json(first));
    console.log(JSON.stringify({ valid: true, kind: spec.kind, name: (spec.create.chatbot ?? spec.create).name, nodes: spec.version.nodes.length, externalCalls: 0 }));
    return;
  }
  const client = new ConnectClient();
  if (command === 'read') return console.log(JSON.stringify(await client.read(first)));
  if (command === 'list') return console.log(JSON.stringify(await client.request('GET', '/chat/v1/chatbot/index?page=1&pageSize=200&includeDetails=All&archived=false')));
  if (command === 'publish') {
    assert(UUID.test(second), 'Version ID is required');
    const result = await client.request('POST', `${botPath(first)}/version/${second}/deploy`, {});
    return console.log(JSON.stringify({ id: result?.id ?? first, publishStatus: result?.publishStatus, verificationRequired: true }));
  }
  assert(['create', 'save'].includes(command), 'Use plan spec.json | audit snapshot.json | list | read id | create spec.json journal.json | save id version.json journal.json | publish id versionId');
  const journalPath = command === 'create' ? second : third;
  assert(journalPath, 'An unused journal path is required');
  const input = await json(command === 'create' ? first : second);
  if (command === 'create') validateSpec(input);
  await writeFile(journalPath, JSON.stringify({ stage: 'reserved' }), { flag: 'wx' });
  const journal = event => writeFile(journalPath, JSON.stringify({ ...event, time: new Date().toISOString() }, null, 2));
  try {
    const saved = command === 'create' ? await client.create(input, journal) : await client.save(first, input, journal);
    await writeFile(`${journalPath}.snapshot.json`, JSON.stringify(saved, null, 2));
    console.log(JSON.stringify({ chatbotId: saved.metadata.id, versionId: saved.metadata.versionId, snapshot: `${journalPath}.snapshot.json`, contentReviewRequired: true }));
  } catch (error) {
    console.error(`Stopped. Reconcile ${journalPath} before retrying; no writes are retried automatically.`);
    throw error;
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main(process.argv.slice(2)).catch(error => { console.error(error.message); process.exitCode = 1; });
}
