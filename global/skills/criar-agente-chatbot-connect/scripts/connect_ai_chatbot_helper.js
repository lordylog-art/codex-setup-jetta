#!/usr/bin/env node
"use strict";

const http = require("http");

const API_BASE = "https://api.app.connectchannels.com.br";
const APP_BASE = "https://app.connectchannels.com.br";
const DEFAULT_CDP = "http://127.0.0.1:9222";

function arg(name, fallback = null) {
  const index = process.argv.indexOf(name);
  return index >= 0 ? process.argv[index + 1] : fallback;
}

function has(flag) {
  return process.argv.includes(flag);
}

function getJson(url) {
  return new Promise((resolve, reject) => {
    http.get(url, (response) => {
      let data = "";
      response.on("data", (chunk) => { data += chunk; });
      response.on("end", () => resolve(JSON.parse(data)));
    }).on("error", reject);
  });
}

async function selectConnectPage(cdp) {
  const pages = await getJson(`${cdp.replace(/\/$/, "")}/json`);
  const page = pages.find((item) => item.type === "page" && String(item.url || "").startsWith(APP_BASE));
  if (!page || !page.webSocketDebuggerUrl) throw new Error("Nenhuma aba Connect encontrada no CDP.");
  return page;
}

async function captureAuthorization(cdp = DEFAULT_CDP) {
  const page = await selectConnectPage(cdp);
  const socket = new WebSocket(page.webSocketDebuggerUrl);
  let id = 0;
  const pending = new Map();
  let authorization = null;

  socket.onmessage = (event) => {
    const message = JSON.parse(event.data);
    if (message.method === "Network.requestWillBeSent") {
      const headers = message.params.request.headers || {};
      const url = message.params.request.url || "";
      const header = headers.Authorization || headers.authorization;
      if (url.includes("api.app.connectchannels.com.br") && header) authorization = header;
    }
    if (message.id && pending.has(message.id)) {
      pending.get(message.id)(message);
      pending.delete(message.id);
    }
  };

  await new Promise((resolve, reject) => {
    socket.onopen = resolve;
    socket.onerror = reject;
  });

  function send(method, params = {}) {
    return new Promise((resolve) => {
      pending.set(++id, resolve);
      socket.send(JSON.stringify({ id, method, params }));
    });
  }

  await send("Network.enable");
  await send("Page.navigate", { url: `${APP_BASE}/chatbots/list/automation?codexCapture=${Date.now()}` });
  for (let i = 0; i < 20 && !authorization; i += 1) {
    await new Promise((resolve) => setTimeout(resolve, 500));
  }
  socket.close();
  if (!authorization) throw new Error("Nao foi possivel capturar Authorization de requisicao real.");
  return authorization;
}

async function api(pathname, authorization, init = {}) {
  const response = await fetch(`${API_BASE}${pathname}`, {
    ...init,
    headers: {
      Authorization: authorization,
      Accept: "application/json, text/plain, */*",
      "Content-Type": "application/json",
      Origin: APP_BASE,
      Referer: `${APP_BASE}/`,
      ...(init.headers || {}),
    },
  });
  const text = await response.text();
  let json;
  try { json = JSON.parse(text); } catch { json = { raw: text.slice(0, 500) }; }
  if (!response.ok) throw new Error(`${init.method || "GET"} ${pathname} -> ${response.status} ${JSON.stringify(json).slice(0, 500)}`);
  return json;
}

function auditTexts(texts) {
  const suspicious = [];
  for (const text of texts) {
    if (text.includes("�")) suspicious.push({ text, reason: "replacement-char" });
    const matches = text.match(/\b[\p{L}]*\?[\p{L}]*/gu) || [];
    for (const match of matches) {
      if (!match.endsWith("?")) suspicious.push({ text, reason: `question-inside-word:${match}` });
    }
  }
  return suspicious;
}

async function main() {
  const cdp = arg("--cdp", DEFAULT_CDP);
  if (has("--session-check")) {
    const authorization = await captureAuthorization(cdp);
    console.log(JSON.stringify({ authenticated: true, token: "[hidden]", authorizationLength: authorization.length }, null, 2));
    return;
  }

  const authorization = await captureAuthorization(cdp);

  if (has("--list-automations")) {
    const data = await api("/chat/v1/chatbot/automation?page=1&pageSize=100&orderBy=name&archived=false", authorization);
    console.log(JSON.stringify((data.items || []).map((item) => ({
      automationId: item.id,
      name: item.name,
      chatbotId: item.chatbotId,
      usage: item.usage,
      inUse: item.inUse,
      publishStatus: item.chatbot && item.chatbot.publishStatus,
    })), null, 2));
    return;
  }

  const chatbotId = arg("--chatbot-id");
  if (has("--read-chatbot") && chatbotId) {
    const bot = await api(`/chat/v1/chatbot/${chatbotId}`, authorization);
    const model = await api(`/chat/v1/chatbot/${chatbotId}/nodes?includeDetails=All`, authorization);
    const texts = (model.nodes || []).filter((node) => node.message && node.message.text).map((node) => node.message.text);
    const aiNodes = (model.nodes || []).filter((node) => node.type === "AI_AGENT" || node.type === "AI_TEAM");
    console.log(JSON.stringify({
      chatbot: {
        id: bot.id,
        name: bot.name,
        automation: bot.automation,
        builderType: bot.builderType,
        publishStatus: bot.publishStatus,
        deployedVersionId: bot.deployedVersionId,
      },
      model: {
        groups: (model.groups || []).map((group) => group.name),
        nodes: (model.nodes || []).length,
        edges: (model.edges || []).length,
        aiNodes: aiNodes.map((node) => ({
          type: node.type,
          aiAgentId: node.aiAgentConfig && node.aiAgentConfig.aiAgentId,
          aiAgentName: node.aiAgentConfig && node.aiAgentConfig.aiAgentName,
        })),
        suspiciousTexts: auditTexts(texts),
      },
    }, null, 2));
    return;
  }

  console.log("Uso: --session-check | --list-automations | --read-chatbot --chatbot-id <id>");
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
