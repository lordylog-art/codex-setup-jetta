#!/usr/bin/env node
"use strict";

const fs = require("fs");

const API_BASE = "https://api.app.connectchannels.com.br";
const APP_BASE = "https://app.connectchannels.com.br";
const DEFAULT_CDP = "http://127.0.0.1:9222";

function parseArgs(argv) {
  const args = { cdp: DEFAULT_CDP, chatbotId: null, read: false, save: null, audit: null, sessionCheck: false };
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--cdp") args.cdp = argv[++i];
    else if (arg === "--chatbot-id") args.chatbotId = argv[++i];
    else if (arg === "--read") args.read = true;
    else if (arg === "--save") args.save = argv[++i];
    else if (arg === "--audit") args.audit = argv[++i];
    else if (arg === "--session-check") args.sessionCheck = true;
    else if (arg === "--help" || arg === "-h") {
      printHelp();
      process.exit(0);
    } else {
      throw new Error(`Argumento desconhecido: ${arg}`);
    }
  }
  return args;
}

function printHelp() {
  console.log(`Uso:
  node scripts/connect_chatbot_tools.js --chatbot-id <id> --read
  node scripts/connect_chatbot_tools.js --audit payload.json
  node scripts/connect_chatbot_tools.js --chatbot-id <id> --save payload.json
  node scripts/connect_chatbot_tools.js --session-check

Nunca imprime token. Usa sessao Chrome CDP em ${DEFAULT_CDP}.
--session-check apenas confirma se a sessao existente tem accessToken; nao abre, clica ou navega.`);
}

async function fetchTextWithTimeout(url, init = {}, timeoutMs = 30000) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(url, { ...init, signal: controller.signal });
    return { response, text: await response.text() };
  } finally {
    clearTimeout(timeout);
  }
}

function cdpEvaluate(webSocketUrl, expression) {
  return new Promise((resolve, reject) => {
    const socket = new WebSocket(webSocketUrl);
    const timeout = setTimeout(() => {
      try { socket.close(); } catch {}
      reject(new Error("Timeout avaliando expressao via CDP."));
    }, 15000);
    socket.addEventListener("open", () => {
      socket.send(JSON.stringify({ id: 1, method: "Runtime.evaluate", params: { expression, returnByValue: true, awaitPromise: true } }));
    });
    socket.addEventListener("message", (event) => {
      const message = JSON.parse(String(event.data));
      if (message.id !== 1) return;
      clearTimeout(timeout);
      try { socket.close(); } catch {}
      if (message.error) reject(new Error(`CDP Runtime.evaluate falhou: ${message.error.message}`));
      else resolve(message.result);
    });
    socket.addEventListener("error", () => {
      clearTimeout(timeout);
      reject(new Error("Erro na conexao WebSocket CDP."));
    });
  });
}

async function getAccessTokenFromCdp(cdp) {
  let targetsResponse;
  try {
    targetsResponse = await fetchTextWithTimeout(`${cdp.replace(/\/$/, "")}/json`, { method: "GET" }, 10000);
  } catch (error) {
    throw new Error(`CDP nao respondeu em ${cdp}. Abra/reutilize a sessao controlavel apenas se precisar autenticar novamente.`);
  }
  if (!targetsResponse.response.ok) throw new Error(`Nao consegui listar abas CDP: ${targetsResponse.response.status}`);
  const targets = JSON.parse(targetsResponse.text);
  const target = targets.find((item) => item.type === "page" && String(item.url || "").startsWith(APP_BASE));
  if (!target || !target.webSocketDebuggerUrl) throw new Error("Nenhuma aba do Connect Channels encontrada no Chrome CDP. Reutilize a sessao controlavel ja logada ou faca login uma vez.");
  const result = await cdpEvaluate(target.webSocketDebuggerUrl, `(() => {
    const raw = localStorage.getItem("accessToken");
    if (!raw) return null;
    try { return JSON.parse(raw); } catch { return raw; }
  })()`);
  const token = result && result.result && result.result.value;
  if (!token) throw new Error("Sessao sem accessToken. Faca login no Chrome controlavel e tente novamente.");
  return {
    authorization: String(token).startsWith("Bearer ") ? String(token) : `Bearer ${token}`,
    targetUrl: target.url,
  };
}

async function getAuthHeaders(cdp) {
  const session = await getAccessTokenFromCdp(cdp);
  return {
    authorization: session.authorization,
    accept: "application/json, text/plain, */*",
    "content-type": "application/json",
    origin: APP_BASE,
    referer: `${APP_BASE}/`,
  };
}

async function apiGet(pathname, options) {
  const headers = await getAuthHeaders(options.cdp);
  const { response, text } = await fetchTextWithTimeout(`${API_BASE}${pathname}`, { method: "GET", headers }, 30000);
  if (!response.ok) throw new Error(`GET ${pathname} falhou: ${response.status} ${text.slice(0, 300)}`);
  return JSON.parse(text);
}

async function saveDraftPayload(chatbotId, payload, options) {
  const headers = await getAuthHeaders(options.cdp);
  const base = `${API_BASE}/chat/v1/chatbot/${chatbotId}/version/url`;
  const { response: getRes, text: getText } = await fetchTextWithTimeout(base, { method: "GET", headers }, 30000);
  if (!getRes.ok) throw new Error(`GET version/url falhou: ${getRes.status} ${getText.slice(0, 200)}`);
  const signed = JSON.parse(getText);
  const body = JSON.stringify(payload);
  const { response: putRes, text: putText } = await fetchTextWithTimeout(signed.url, { method: "PUT", headers: { "content-type": "application/json" }, body }, 30000);
  if (!putRes.ok) throw new Error(`PUT S3 falhou: ${putRes.status} ${putText.slice(0, 200)}`);
  const { response: postRes, text: postText } = await fetchTextWithTimeout(base, { method: "POST", headers, body: JSON.stringify({ key: signed.key, url: signed.url }) }, 30000);
  if (!postRes.ok) throw new Error(`POST version/url falhou: ${postRes.status} ${postText.slice(0, 300)}`);
  return JSON.parse(postText);
}

function auditPayload(payload) {
  const counts = {};
  for (const node of payload.nodes || []) {
    const key = node.type === "ACTION" ? `ACTION.${node.action && node.action.type}` : node.type;
    counts[key] = (counts[key] || 0) + 1;
  }
  const edges = payload.edges || [];
  const nodes = payload.nodes || [];
  const groups = payload.groups || [];
  const badEnd = [];
  const terminalActionTypes = new Set(["COMPLETE_SESSION", "TRANSFER_CHATBOT"]);
  for (const group of groups) {
    const groupNodes = nodes.filter((node) => node.groupClientGeneratedId === group.clientGeneratedId);
    const hasOwnExit = groupNodes.some((node) => node.type === "MENU" || node.type === "CONDITION" || (node.action && terminalActionTypes.has(node.action.type)));
    const hasExitEdge = edges.some((edge) => edge.clientSourceId === `${group.clientGeneratedId}-EXIT`);
    if (hasOwnExit && hasExitEdge) badEnd.push(group.name || group.clientGeneratedId);
  }
  const menus = nodes.filter((node) => node.type === "MENU");
  const menuMissing = menus.flatMap((node) => (node.menu && node.menu.options || [])
    .filter((option) => !edges.some((edge) => edge.clientSourceGroupId === node.groupClientGeneratedId && edge.clientSourceId === option.clientGeneratedId))
    .map((option) => option.text || option.clientGeneratedId));
  const conditions = nodes.filter((node) => node.type === "CONDITION");
  const condMissing = conditions.flatMap((node) => (node.conditions || [])
    .filter((condition) => !edges.some((edge) => edge.clientSourceGroupId === node.groupClientGeneratedId && edge.clientSourceId === condition.clientGeneratedId))
    .map((condition) => condition.name || condition.clientGeneratedId));
  return {
    groups: groups.length,
    nodes: nodes.length,
    edges: edges.length,
    counts,
    badEnd,
    menuMissing,
    condMissing,
    hasWebhook: !!counts["ACTION.WEBHOOK"],
    hasTemplate: !!counts.TEMPLATE,
  };
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.sessionCheck) {
    const session = await getAccessTokenFromCdp(args.cdp);
    console.log(JSON.stringify({
      authenticated: true,
      cdp: args.cdp,
      source: "Chrome CDP localStorage accessToken",
      targetUrl: session.targetUrl,
      token: "[hidden]",
    }, null, 2));
    return;
  }
  if (args.audit) {
    const payload = JSON.parse(fs.readFileSync(args.audit, "utf8"));
    console.log(JSON.stringify(auditPayload(payload), null, 2));
    return;
  }
  if (args.read) {
    if (!args.chatbotId) throw new Error("--chatbot-id e obrigatorio para --read.");
    const payload = await apiGet(`/chat/v1/chatbot/${args.chatbotId}/nodes?includeDetails=All`, { cdp: args.cdp });
    console.log(JSON.stringify({ chatbotId: args.chatbotId, audit: auditPayload(payload) }, null, 2));
    return;
  }
  if (args.save) {
    if (!args.chatbotId) throw new Error("--chatbot-id e obrigatorio para --save.");
    const payload = JSON.parse(fs.readFileSync(args.save, "utf8"));
    const audit = auditPayload(payload);
    if (audit.badEnd.length || audit.menuMissing.length || audit.condMissing.length) {
      throw new Error(`Auditoria falhou antes de salvar: ${JSON.stringify(audit)}`);
    }
    const result = await saveDraftPayload(args.chatbotId, payload, { cdp: args.cdp });
    console.log(JSON.stringify({ saved: true, chatbotId: args.chatbotId, audit, result }, null, 2));
    return;
  }
  printHelp();
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
