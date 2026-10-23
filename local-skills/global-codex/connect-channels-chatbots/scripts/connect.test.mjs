import test from 'node:test';
import assert from 'node:assert/strict';
import { ConnectClient, validateSpec, auditReadback } from './connect.mjs';

const id = '11111111-1111-4111-8111-111111111111';
const group = '22222222-2222-4222-8222-222222222222';
const node = '33333333-3333-4333-8333-333333333333';
const versionId = '44444444-4444-4444-8444-444444444444';
const spec = () => ({
  kind: 'attendance',
  create: { name: 'Synthetic contract check', defaultDepartmentId: id, channelTypes: ['CLOUDAPI_WHATSAPP'], builderType: 'HELENA_ADVANCED' },
  version: {
    startGroupClientGeneratedId: group,
    groups: [{ name: 'Start', clientGeneratedId: group }], edges: [{ clientSourceGroupId: 'BEGIN-GROUP', clientTargetGroupId: group }],
    nodes: [{ type: 'CONTENT', clientGeneratedId: node, groupClientGeneratedId: group, message: { type: 'TEXT', text: 'Synthetic message', messageVariations: { variations: [{ text: 'Another message' }] } } }],
    config: { aggregation: { timeoutAfterMessageMs: null, enableFallbackNodeGroup: false }, vendorExtension: { preserve: true } },
  },
});
const response = data => ({ ok: true, status: 200, json: async () => data });

function nativeMenuReadback(){
  const child='55555555-5555-4555-8555-555555555555',childNode='66666666-6666-4666-8666-666666666666';
  return {metadata:{builderType:'HELENA_ADVANCED'},content:{startGroupId:versionId,groups:[{id:versionId,clientGeneratedId:group},{id:id,clientGeneratedId:child}],nodes:[{id:node,clientGeneratedId:node,groupId:versionId,groupClientGeneratedId:group,type:'MENU',order:0,nextNodeId:childNode,previousNodeId:null,menu:{options:[{clientGeneratedId:versionId,type:'NAVIGATION',text:'Continue',targetClientGroupId:child,targetGroupId:id}]}},{id:childNode,clientGeneratedId:childNode,groupId:id,groupClientGeneratedId:child,type:'CONTENT',order:0,previousNodeId:null,nextNodeId:null,message:{type:'TEXT',text:'Child'}}],edges:[{clientSourceGroupId:'BEGIN-GROUP',clientTargetGroupId:group},{clientSourceGroupId:group,clientSourceId:versionId,clientTargetGroupId:child}]}};
}

test('audits actual advanced bindings without declaring legacy adjacency a broken runtime',()=>{
  const result=auditReadback(nativeMenuReadback());
  assert.equal(result.valid,true);assert.equal(result.legacyAdjacencyDifferences,1);assert.equal(result.runtimeExecutionProven,false);
});

test('blocks a native MENU destination that differs from its client binding',()=>{
  const saved=nativeMenuReadback();saved.content.nodes[0].menu.options[0].targetGroupId=versionId;
  assert.throws(()=>auditReadback(saved),/MENU resolved destination/);
});

test('blocks a GOTO native destination that differs from its executable client target',()=>{
  const saved=nativeMenuReadback(),root=saved.content.nodes[0],target=saved.content.nodes[1];
  root.type='ACTION';delete root.menu;root.action={type:'GOTO_RETURN_POINT',targetClientNodeId:target.clientGeneratedId,targetNodeId:root.id};
  saved.content.edges[1].clientSourceId=group+'-EXIT';
  assert.throws(()=>auditReadback(saved),/GOTO resolved destination/);
});

test('rejects the observed hyphenated option save failure before any HTTP write', () => {
  const input=spec();
  input.version.nodes[0]={type:'MENU',clientGeneratedId:node,groupClientGeneratedId:group,message:{type:'TEXT',text:'Escolha'},menu:{options:[{clientGeneratedId:id,type:'NAVIGATION',text:'E-mail / acesso',targetClientGroupId:group}]}};
  assert.throws(()=>validateSpec(input),/hyphen/);
  input.version.nodes[0].menu.options[0].text='Email / acesso';
  assert.equal(validateSpec(input),input);
});

test('rejects interactive FILE questions supported only as open attachment collection', () => {
  const input=spec();
  input.version.nodes[0]={type:'QUESTION',clientGeneratedId:node,groupClientGeneratedId:group,question:{valueType:'FILE',interactiveType:'LIST',options:[]}};
  assert.throws(()=>validateSpec(input),/FILE.*interactive/);
  input.version.nodes[0].question.interactiveType=null;
  assert.equal(validateSpec(input),input);
});

test('rejects QUESTION parameters in CRM card fields while preserving session metadata parameters',()=>{
  const input=spec();
  input.version.nodes[0]={type:'ACTION',clientGeneratedId:node,groupClientGeneratedId:group,action:{type:'CARD',card:{operation:'CREATE',panelId:id,stepId:versionId,title:{text:'[solicitante]',params:[{type:'QUESTION',replacementName:'solicitante',questionNodeClientId:node}]}}}};
  assert.throws(()=>validateSpec(input),/CARD.*QUESTION/);
  input.version.nodes[0].action.card.title.params=[{type:'SESSION_METADATA',replacementName:'solicitante',metadataKey:'ti_solicitante'}];
  assert.equal(validateSpec(input),input);
});

test('retains vendor request identity on a rejected write without exposing vendor text or retrying',async()=>{
  let calls=0;
  const client=new ConnectClient({token:'private-session',fetchImpl:async()=>{calls++;return {ok:false,status:500,json:async()=>({id:{value:id},key:'ERROR_UNEXPECTED',text:'secret diagnostic https://storage.test?token=private-session'})};}});
  await assert.rejects(client.request('POST','/chat/v1/chatbot',{}),e=>{assert.equal(e.requestId,id);assert.equal(e.vendorCode,'ERROR_UNEXPECTED');assert.equal(e.status,500);assert(!e.message.includes('private-session'));return true;});
  assert.equal(calls,1);
});

test('preserves native options and rejects disconnected graph references', () => {
  const input = spec();
  assert.equal(validateSpec(input), input);
  assert.deepEqual(input.version.config.vendorExtension, { preserve: true });
  input.version.nodes[0].groupClientGeneratedId = id;
  assert.throws(() => validateSpec(input), /missing group/);
});

test('rejects duplicate node IDs before sending a request', () => {
  const input = spec();
  input.version.nodes.push(structuredClone(input.version.nodes[0]));
  assert.throws(() => validateSpec(input), /Duplicate node/);
});

test('rejects an absent initial edge and a dangling conditional target', () => {
  const noStart = spec();
  noStart.version.edges = [];
  assert.throws(() => validateSpec(noStart), /BEGIN-GROUP/);
  const dangling = spec();
  dangling.version.nodes[0].aggregation = { fallbackNodeGroupClientId: id };
  assert.throws(() => validateSpec(dangling), /Missing group reference/);
});

test('rejects fabricated handles and divergent executable destinations', () => {
  const input = spec();
  input.version.edges.push({ clientSourceGroupId: group, clientSourceId: node, clientTargetGroupId: group });
  assert.throws(() => validateSpec(input), /source handle/);
  input.version.nodes[0] = { type: 'CONDITION', clientGeneratedId: node, groupClientGeneratedId: group, conditions: [{ clientGeneratedId: id, target: { clientGroupId: group } }] };
  input.version.edges[1].clientSourceId = id;
  assert.equal(validateSpec(input), input);
  input.version.nodes[0].conditions[0].target.clientGroupId = undefined;
  assert.throws(() => validateSpec(input), /destination differs/);
});

test('uses the recovered three-stage save protocol without credentials on storage', async () => {
  const calls = [];
  const events = [];
  const metadata = { id, versionId, builderType: 'HELENA_ADVANCED', channelIds: [] };
  const replies = [metadata, { url: 'https://storage.example.test/draft?signature=secret', key: 'upload-key' }, {}, {}, metadata, { nodes: spec().version.nodes }];
  const client = new ConnectClient({ token: 'private-session', fetchImpl: async (url, options) => { calls.push({ url, ...options }); return response(replies.shift()); } });
  const saved = await client.save(id, spec().version, async event => events.push(event));
  assert.equal(saved.metadata.versionId, versionId);
  assert.deepEqual(calls.map(call => call.method), ['GET', 'GET', 'PUT', 'POST', 'GET', 'GET']);
  assert.equal(calls[2].headers.Authorization, undefined);
  assert.equal(calls[0].headers.Authorization, 'Bearer private-session');
  assert.deepEqual(JSON.parse(calls[2].body), spec().version);
  assert.deepEqual(JSON.parse(calls[3].body), { key: 'upload-key', url: 'https://storage.example.test/draft?signature=secret' });
  assert(calls.every(call => call.redirect === 'error'));
  assert(!JSON.stringify(events).includes('secret'));
  assert.equal(events.at(-1).stage, 'saved-content-review-required');
});

test('stops uncertain creation once, preserving the creating journal stage', async () => {
  let calls = 0;
  const events = [];
  const client = new ConnectClient({ token: 'session', fetchImpl: async () => { calls++; throw Error('connection lost'); } });
  await assert.rejects(client.create(spec(), async event => events.push(event)), /connection lost/);
  assert.equal(calls, 1);
  assert.equal(events.at(-1).stage, 'creating');
});

test('preserves the created chatbot ID if version upload fails; never retries it', async () => {
  let calls = 0;
  const events = [];
  const metadata = { id, builderType: 'HELENA_ADVANCED', channelIds: [] };
  const replies = [metadata, metadata, { url: 'https://storage.example.test/draft', key: 'k' }];
  const client = new ConnectClient({ token: 'session', fetchImpl: async () => { calls++; if (calls === 4) throw Error('upload interrupted'); return response(replies.shift()); } });
  await assert.rejects(client.create(spec(), async event => events.push(event)), /upload interrupted/);
  assert.equal(calls, 4);
  assert.equal(events.at(-1).stage, 'uploading');
  assert.equal(events.at(-1).chatbotId, id);
});

test('does not edit a chatbot already linked to a live channel', async () => {
  let calls = 0;
  const client = new ConnectClient({ token: 'session', fetchImpl: async () => { calls++; return response({ id, builderType: 'HELENA_ADVANCED', channelIds: [group] }); } });
  await assert.rejects(client.save(id, spec().version, async () => {}), /separate draft/);
  assert.equal(calls, 1);
});

test('saves a new unpublished idle automation whose channelIds only represent its automation channel', async () => {
  const calls = [];
  const metadata = { id, versionId, builderType: 'HELENA_ADVANCED', automation: true, publishStatus: 'NOT_PUBLISHED', channelIds: [group] };
  const automation = { chatbotId: id, channelId: group, inUse: false };
  const replies = [metadata, { items: [automation] }, { url: 'https://storage.example.test/draft', key: 'k' }, {}, {}, metadata, { nodes: spec().version.nodes }];
  const client = new ConnectClient({ token: 'session', fetchImpl: async (url, options) => { calls.push({ url, ...options }); return response(replies.shift()); } });
  await client.save(id, spec().version, async () => {});
  assert.equal(calls.filter(call => call.method === 'PUT').length, 1);
  assert.equal(calls.find(call => call.method === 'PUT').headers.Authorization, undefined);
});

test('automation channel association does not permit editing published, mismatched or otherwise linked bots', async () => {
  for (const variation of [
    { publishStatus: 'READY', channelIds: [group], chatbotId: id },
    { publishStatus: 'NOT_PUBLISHED', channelIds: [group, node], chatbotId: id },
    { publishStatus: 'NOT_PUBLISHED', channelIds: [group], chatbotId: node },
  ]) {
    let calls = 0;
    const client = new ConnectClient({ token: 'session', fetchImpl: async () => response(++calls === 1
      ? { id, builderType: 'HELENA_ADVANCED', automation: true, publishStatus: variation.publishStatus, channelIds: variation.channelIds }
      : { items: [{ chatbotId: variation.chatbotId, channelId: group, inUse: false }] }) });
    await assert.rejects(client.save(id, spec().version, async () => {}), /separate draft|identity/);
    assert.equal(calls, 2);
  }
});

test('queries automation details separately before editing; blocks an in-use automation', async () => {
  const calls = [];
  const client = new ConnectClient({ token: 'session', fetchImpl: async url => { calls.push(url); return response(calls.length === 1 ? { id, builderType: 'HELENA_ADVANCED', automation: true } : { items: [{ chatbotId: id, inUse: true }] }); } });
  await assert.rejects(client.save(id, spec().version, async () => {}), /separate draft/);
  assert.equal(calls.length, 2);
  assert(calls[1].includes(`/automation?chatbotId=${id}`));
});

test('simple editor preserves upload confirmation fields and reads its version endpoint', async () => {
  const calls = [];
  const metadata = { id, versionId, builderType: 'HELENA_SIMPLE', channelIds: [] };
  const upload = { url: 'https://storage.example.test/simple', key: 'k', vendorConfirmationField: 'preserved' };
  const input = {
    id, versionId, key: 'synthetic-key', name: 'Simple hierarchy', config: {},
    nodes: [{ type: 'MENU', clientGeneratedId: node, order: 0, key: 'cb-11111111-mn-33333333', menu: { interactiveType: 'LIST', options: [{ clientGeneratedId: group, type: 'NAVIGATION', text: 'Continue', targetClientGroupId: group }] }, children: [{ clientGeneratedId: group, nodes: [{ type: 'CONTENT', clientGeneratedId: versionId, order: 0, key: 'cb-11111111-msg-44444444', message: { type: 'TEXT', text: 'Child content' } }] }] }],
  };
  const replies = [metadata, upload, {}, {}, metadata, input];
  const client = new ConnectClient({ token: 'session', fetchImpl: async (url, options) => { calls.push({ url, ...options }); return response(replies.shift()); } });
  await client.save(id, input, async () => {});
  assert.deepEqual(JSON.parse(calls[3].body), upload);
  assert.deepEqual(JSON.parse(calls[2].body), input);
  assert(calls.at(-1).url.endsWith(`/version/${versionId}?includeDetails=All&deployedVersion=false`));
});

test('refuses wrong chatbot identity, unexpected API origins and unsafe upload URL', async () => {
  assert.throws(() => new ConnectClient({ token: 'session', base: 'https://attacker.example' }), /Unsupported/);
  let calls = 0;
  const client = new ConnectClient({ token: 'session', fetchImpl: async () => { calls++; return response(calls === 1 ? { id: group } : {}); } });
  await assert.rejects(client.save(id, spec().version, async () => {}), /Wrong chatbot/);
  const unsafe = new ConnectClient({ token: 'session', fetchImpl: async url => response(url.includes('/version/url') ? { url: 'http://localhost/upload', key: 'k' } : { id, builderType: 'HELENA_ADVANCED' }) });
  await assert.rejects(unsafe.save(id, spec().version, async () => {}), /Invalid upload/);
});
