import { chromium } from "@playwright/test";
import { mkdir, readdir, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

const SCRIPT_PATH = fileURLToPath(import.meta.url);
const SKILL_ROOT = path.resolve(path.dirname(SCRIPT_PATH), "..");
const PROJECT_ROOT = path.resolve(SKILL_ROOT, "../../..");
const DEFAULT_REFERENCES_ROOT = path.join(SKILL_ROOT, "references");
const DEFAULT_STORAGE_STATE = path.join(PROJECT_ROOT, ".codex-temp", "playwright-auth.json");
const LOCAL_HOSTS = new Set(["localhost", "127.0.0.1", "[::1]"]);
const DEFAULT_MAX_PAGES = 180;

export function assertLocalBaseUrl(value) {
  let url;
  try {
    url = new URL(value);
  } catch {
    throw new Error("URL base local inválida.");
  }

  if (!LOCAL_HOSTS.has(url.hostname)) {
    throw new Error("A captura aceita somente localhost, 127.0.0.1 ou ::1.");
  }
  if (url.protocol !== "http:" && url.protocol !== "https:") {
    throw new Error("A URL local deve usar HTTP ou HTTPS.");
  }
  if (url.username || url.password) {
    throw new Error("A URL local não pode conter credenciais.");
  }
  if (url.search || url.hash) {
    throw new Error("A URL local não pode conter query ou fragmento.");
  }
  if (url.pathname !== "/" && url.pathname !== "") {
    throw new Error("A URL base local não pode conter caminho.");
  }

  return url;
}

export function isInspectableRoute(value) {
  if (typeof value !== "string" || !value.startsWith("/") || value.startsWith("//")) {
    return false;
  }

  const pathname = value.split(/[?#]/, 1)[0].replace(/\/+$/, "") || "/";
  const blocked = [
    "/api",
    "/logout",
    "/auth/logout",
    "/formulario",
    "/r/",
    "/_next",
  ];

  return !blocked.some((prefix) => pathname === prefix || pathname.startsWith(prefix));
}

export function routeToArtifactName(route) {
  const pathname = redactRoutePath(route).split(/[?#]/, 1)[0].replace(/^\/+|\/+$/g, "");
  if (!pathname) return "inicio";
  return decodeURIComponent(pathname)
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-zA-Z0-9/_-]+/g, "-")
    .replace(/\//g, "__")
    .replace(/-+/g, "-")
    .toLowerCase();
}

export function redactRoutePath(value) {
  const pathname = String(value ?? "").split(/[?#]/, 1)[0];
  const dynamicSegment = /^(?:[0-9]+|[0-9a-f]{8}-[0-9a-f-]{27,}|(?:email-contact|driver|motorista|vehicle|veiculo|collaborator|colaborador|user|usuario|client|cliente|occurrence|ocorrencia|ticket|chamado|3coracoes-incident-type)-[a-z0-9-]+)$/i;
  return (pathname || "/")
    .split("/")
    .map((segment) => (dynamicSegment.test(segment) ? "[item]" : segment))
    .join("/") || "/";
}

export function isCanonicalCaptureRoute(requestedRoute, finalRoute) {
  return redactRoutePath(requestedRoute) === redactRoutePath(finalRoute);
}

export function redactRuntimeText(value) {
  return String(value ?? "")
    .replace(/\b([\w.+-]+)@([\w.-]+)\.[a-z]{2,}\b/gi, "[e-mail redigido]")
    .replace(/\b\d{3}\.\d{3}\.\d{3}-\d{2}\b/g, "[conteúdo redigido]")
    .replace(/\b(?:[A-Z]{3}[0-9][A-Z0-9][0-9]{2}|[A-Z]{3}-?[0-9]{4})\b/gi, "[conteúdo redigido]")
    .replace(/\b[0-9a-f]{8}-[0-9a-f-]{27,}\b/gi, "[identificador redigido]")
    .replace(/\b(Motorista|Colaborador|Usuário|Cliente|Placa|CPF|Telefone|E-mail):?\s+[^|\n]+/gi, "$1 [conteúdo redigido]");
}

export function sanitizeImageSource(value) {
  const source = String(value ?? "").trim();
  if (/^data:/i.test(source)) return "[imagem incorporada omitida]";
  if (/^blob:/i.test(source)) return "[imagem temporária omitida]";
  return source;
}

async function walkFiles(root) {
  const entries = await readdir(root, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = path.join(root, entry.name);
    if (entry.isDirectory()) files.push(...(await walkFiles(fullPath)));
    else files.push(fullPath);
  }
  return files;
}

function sourcePageToRoute(filePath, appRoot) {
  let relative = path.relative(appRoot, path.dirname(filePath)).replaceAll("\\", "/");
  if (!relative) return "/";
  const parts = relative
    .split("/")
    .filter((part) => part && !/^\(.+\)$/.test(part) && !part.startsWith("@"))
    .map((part) => {
      if (part === "[unit]") return "guarulhos";
      if (/^\[.*client.*\]$/i.test(part)) return "3-coracoes";
      return part;
    });
  if (parts.some((part) => part.includes("[") || part.includes("]"))) return null;
  const route = `/${parts.join("/")}`;
  return isInspectableRoute(route) ? route : null;
}

async function discoverSourceRoutes() {
  const appRoot = path.join(PROJECT_ROOT, "apps", "web", "src", "app");
  const files = (await walkFiles(appRoot)).filter((file) => /[\\/]page\.(?:tsx|jsx|ts|js)$/.test(file));
  return files
    .map((file) => ({
      route: sourcePageToRoute(file, appRoot),
      source: path.relative(PROJECT_ROOT, file).replaceAll("\\", "/"),
    }))
    .filter((entry) => entry.route)
    .sort((a, b) => a.route.localeCompare(b.route));
}

function increment(map, value) {
  const normalized = String(value ?? "").trim();
  if (!normalized || normalized === "rgba(0, 0, 0, 0)" || normalized === "normal") return;
  map.set(normalized, (map.get(normalized) ?? 0) + 1);
}

function topEntries(map, limit = 16) {
  return [...map.entries()].sort((a, b) => b[1] - a[1]).slice(0, limit);
}

async function collectPageContract(page) {
  const raw = await page.evaluate(() => {
    const text = (element) => (element?.textContent ?? "").replace(/\s+/g, " ").trim();
    const unique = (values) => [...new Set(values.filter(Boolean))];
    const visible = (element) => {
      const style = getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return style.display !== "none" && style.visibility !== "hidden" && rect.width > 0 && rect.height > 0;
    };
    const elements = [...document.querySelectorAll("body *")].filter(visible).slice(0, 1200);
    return {
      title: document.title,
      headings: unique([...document.querySelectorAll("h1,h2,h3")].map(text)).slice(0, 40),
      buttons: unique(
        [...document.querySelectorAll("button,[role='button'],[role='tab']")]
          .filter(visible)
          .map((element) => element.getAttribute("aria-label") || text(element)),
      ).slice(0, 80),
      tableHeaders: unique([...document.querySelectorAll("th,[role='columnheader']")].map(text)).slice(0, 80),
      controls: [...document.querySelectorAll("input,select,textarea")]
        .filter(visible)
        .slice(0, 80)
        .map((element) => ({
          tag: element.tagName.toLowerCase(),
          type: element.getAttribute("type") || "",
          name: element.getAttribute("name") || "",
          placeholder: element.getAttribute("placeholder") || "",
          ariaLabel: element.getAttribute("aria-label") || "",
        })),
      images: [...document.querySelectorAll("img")]
        .filter(visible)
        .slice(0, 80)
        .map((element) => ({
          src: element.getAttribute("src") || "",
          alt: element.getAttribute("alt") || "",
          className: element.getAttribute("class") || "",
        })),
      styles: elements.map((element) => {
        const style = getComputedStyle(element);
        return {
          fontFamily: style.fontFamily,
          fontSize: style.fontSize,
          fontWeight: style.fontWeight,
          color: style.color,
          backgroundColor: style.backgroundColor,
          borderRadius: style.borderRadius,
          gap: style.gap,
          padding: style.padding,
        };
      }),
      classes: elements.flatMap((element) => [...element.classList]),
    };
  });

  const styleKeys = ["fontFamily", "fontSize", "fontWeight", "color", "backgroundColor", "borderRadius", "gap", "padding"];
  const styleFrequencies = Object.fromEntries(styleKeys.map((key) => [key, new Map()]));
  for (const style of raw.styles) {
    for (const key of styleKeys) increment(styleFrequencies[key], style[key]);
  }
  const classFrequency = new Map();
  for (const className of raw.classes) increment(classFrequency, className);

  return {
    ...raw,
    headings: raw.headings.map(redactRuntimeText),
    buttons: raw.buttons.map(redactRuntimeText),
    tableHeaders: raw.tableHeaders.map(redactRuntimeText),
    controls: raw.controls.map((control) => ({
      ...control,
      name: redactRuntimeText(control.name),
      placeholder: redactRuntimeText(control.placeholder),
      ariaLabel: redactRuntimeText(control.ariaLabel),
    })),
    images: raw.images.map((image) => ({
      ...image,
      src: sanitizeImageSource(image.src),
      alt: redactRuntimeText(image.alt),
    })),
    styles: Object.fromEntries(styleKeys.map((key) => [key, topEntries(styleFrequencies[key])])),
    classes: topEntries(classFrequency, 80),
  };
}

async function redactPageForScreenshot(page) {
  await page.evaluate(() => {
    const protectedSelector = "header,nav,aside,h1,h2,h3,label,th,button,[role='button'],[role='tab'],[role='columnheader'],[class*='status'],[class*='badge']";
    for (const control of document.querySelectorAll("input,textarea")) {
      if (control instanceof HTMLInputElement || control instanceof HTMLTextAreaElement) control.value = "";
    }
    for (const cell of document.querySelectorAll("tbody td,[role='rowgroup'] [role='cell']")) {
      const walker = document.createTreeWalker(cell, NodeFilter.SHOW_TEXT);
      const nodes = [];
      while (walker.nextNode()) nodes.push(walker.currentNode);
      for (const node of nodes) {
        if (node.parentElement?.closest("[class*='status'],[class*='badge'],button")) continue;
        if (node.textContent?.trim()) node.textContent = "•••";
      }
    }
    const directSensitivePattern = /(?:\b[\w.+-]+@[\w.-]+\.[a-z]{2,}\b|\b\d{3}\.\d{3}\.\d{3}-\d{2}\b|\b[A-Z]{3}(?:-?\d{4}|\d[A-Z0-9]\d{2})\b|\b[0-9a-f]{8}-[0-9a-f-]{27,}\b)/i;
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const textNodes = [];
    while (walker.nextNode()) textNodes.push(walker.currentNode);
    for (const node of textNodes) {
      const parent = node.parentElement;
      const current = node.textContent?.trim() ?? "";
      if (!parent || !current) continue;
      if (/\bFe\b/i.test(getComputedStyle(parent).fontFamily)) {
        node.textContent = "•••";
        parent.closest("[aria-label]")?.setAttribute("aria-label", "Placa redigida");
        continue;
      }
      if (directSensitivePattern.test(current)) {
        node.textContent = current.replace(directSensitivePattern, "[conteúdo redigido]");
        continue;
      }
      let ancestor = parent;
      let signature = "";
      for (let depth = 0; ancestor && depth < 6; depth += 1, ancestor = ancestor.parentElement) {
        signature += ` ${ancestor.id} ${typeof ancestor.className === "string" ? ancestor.className : ""}`;
      }
      if (/(plate|placa)/i.test(signature) && !/^(placa|placas)$/i.test(current)) {
        node.textContent = "[conteúdo redigido]";
        continue;
      }
      if (parent.closest(protectedSelector)) continue;
      node.textContent = "•••";
    }
    const style = document.createElement("style");
    style.textContent = `
      *, *::before, *::after { animation-duration: 0s !important; animation-delay: 0s !important; transition-duration: 0s !important; caret-color: transparent !important; }
      video, canvas[data-sensitive], img[src^="data:"], img[src^="blob:"] { visibility: hidden !important; }
    `;
    document.head.appendChild(style);
  });
}

function mdCell(value) {
  return String(value ?? "").replaceAll("|", "\\|").replace(/\s+/g, " ").trim();
}

function listSection(title, items) {
  if (!items?.length) return `## ${title}\n\nNenhum item visível na captura.\n`;
  return `## ${title}\n\n${items.map((item) => `- ${mdCell(item)}`).join("\n")}\n`;
}

function styleSection(styles) {
  return Object.entries(styles)
    .map(([property, entries]) => {
      const rows = entries.map(([value, count]) => `| ${mdCell(value)} | ${count} |`).join("\n");
      return `### ${property}\n\n| Valor computado | Ocorrências amostradas |\n| --- | ---: |\n${rows || "| — | 0 |"}`;
    })
    .join("\n\n");
}

function pageMarkdown({ route, finalRoute, screenshotRelative, contract, source }) {
  const controls = contract.controls.map((control) =>
    `${control.tag}${control.type ? ` (${control.type})` : ""}: ${control.ariaLabel || control.placeholder || control.name || "sem rótulo"}`,
  );
  const images = contract.images.map((image) => `${image.src} — ${image.alt || "sem texto alternativo"}`);
  const classes = contract.classes.map(([className, count]) => `${className} (${count})`);
  return `# Referência da tela: ${route}\n\n` +
    `- Rota solicitada: \`${route}\`\n` +
    `- Rota final: \`${finalRoute}\`\n` +
    `- Fonte: \`${source ?? "descoberta em runtime"}\`\n` +
    `- Título: ${mdCell(contract.title)}\n` +
    `- Screenshot redigido: [abrir imagem](../${screenshotRelative.replaceAll("\\", "/")})\n\n` +
    `A captura remove valores de campos e conteúdo de linhas operacionais. Ela registra estrutura e aparência, não dados do cliente.\n\n` +
    listSection("Hierarquia visível", contract.headings) + "\n" +
    listSection("Ações visíveis", contract.buttons) + "\n" +
    listSection("Colunas de tabela", contract.tableHeaders) + "\n" +
    listSection("Controles", controls) + "\n" +
    listSection("Imagens", images) + "\n" +
    listSection("Classes mais frequentes", classes) + "\n" +
    `## Estilos computados mais frequentes\n\n${styleSection(contract.styles)}\n`;
}

async function extractSourceReferences(sourceRoutes) {
  const globalsPath = path.join(PROJECT_ROOT, "apps", "web", "src", "app", "globals.css");
  const css = await readFile(globalsPath, "utf8");
  const variableMatches = [...css.matchAll(/(--[a-zA-Z0-9_-]+)\s*:\s*([^;]+);/g)];
  const variables = [...new Map(variableMatches.map((match) => [match[1], match[2].trim()])).entries()];
  const fontFaces = [...css.matchAll(/@font-face\s*\{([\s\S]*?)\}/g)].map((match) => match[1].trim());

  const publicRoot = path.join(PROJECT_ROOT, "apps", "web", "public");
  const publicFiles = (await walkFiles(publicRoot))
    .filter((file) => /\.(?:png|jpe?g|webp|svg|gif|ico|ttf|woff2?)$/i.test(file))
    .map((file) => path.relative(publicRoot, file).replaceAll("\\", "/"))
    .sort();

  const componentRoot = path.join(PROJECT_ROOT, "apps", "web", "src", "components");
  const componentFiles = (await walkFiles(componentRoot))
    .filter((file) => /\.(?:tsx|jsx)$/.test(file) && !/\.spec\.|\.test\./.test(file))
    .map((file) => path.relative(PROJECT_ROOT, file).replaceAll("\\", "/"))
    .sort();

  return { variables, fontFaces, publicFiles, componentFiles, sourceRoutes };
}

async function writeSourceReferenceDocs(referencesRoot, source) {
  const tokenRows = source.variables.map(([name, value]) => `| \`${name}\` | \`${mdCell(value)}\` |`).join("\n");
  await writeFile(
    path.join(referencesRoot, "source-foundations.md"),
    `# Fundamentos extraídos do código\n\n## Tokens CSS globais\n\n| Token | Valor-base |\n| --- | --- |\n${tokenRows}\n\n` +
      `## Fontes declaradas\n\n${source.fontFaces.length ? source.fontFaces.map((face) => `\`\`\`css\n${face}\n\`\`\``).join("\n\n") : "Nenhuma declaração encontrada."}\n\n` +
      `Fonte canônica: \`apps/web/src/app/globals.css\`. Os valores em runtime prevalecem quando temas ou escopos os sobrescrevem.\n`,
    "utf8",
  );
  await writeFile(
    path.join(referencesRoot, "source-assets.md"),
    `# Imagens, ícones e fontes disponíveis\n\n` +
      `Use um ativo existente antes de desenhar, gerar ou importar outro. Confirme o uso pelo nome e pelas referências de tela.\n\n` +
      source.publicFiles.map((file) => `- \`apps/web/public/${file}\``).join("\n") + "\n",
    "utf8",
  );
  await writeFile(
    path.join(referencesRoot, "source-components.md"),
    `# Componentes visuais disponíveis\n\n` +
      `Procure nestes arquivos antes de criar qualquer elemento novo. Leia apenas os candidatos compatíveis com a tarefa.\n\n` +
      source.componentFiles.map((file) => `- \`${file}\``).join("\n") + "\n",
    "utf8",
  );
}

async function capture({ baseUrl, storageState, referencesRoot, maxPages }) {
  const base = assertLocalBaseUrl(baseUrl);
  const sourceRoutes = await discoverSourceRoutes();
  const sourceByRoute = new Map(sourceRoutes.map((entry) => [entry.route, entry.source]));
  const screenshotsRoot = path.join(referencesRoot, "screenshots");
  const pagesRoot = path.join(referencesRoot, "pages");
  await mkdir(screenshotsRoot, { recursive: true });
  await mkdir(pagesRoot, { recursive: true });
  await rm(screenshotsRoot, { recursive: true, force: true });
  await rm(pagesRoot, { recursive: true, force: true });
  await mkdir(screenshotsRoot, { recursive: true });
  await mkdir(pagesRoot, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const contextOptions = {
    storageState,
    viewport: { width: 1440, height: 1000 },
    colorScheme: "light",
    locale: "pt-BR",
    reducedMotion: "reduce",
  };
  const context = await browser.newContext(contextOptions);
  const anonymousContext = await browser.newContext({ ...contextOptions, storageState: undefined });
  const page = await context.newPage();
  const anonymousPage = await anonymousContext.newPage();
  const queued = [];
  const queuedSet = new Set();
  const visited = new Set();
  const results = [];

  function enqueue(route) {
    const pathname = route.split(/[?#]/, 1)[0].replace(/\/+$/, "") || "/";
    const routeKey = redactRoutePath(pathname);
    if (!isInspectableRoute(pathname) || queuedSet.has(routeKey) || visited.has(routeKey)) return;
    queuedSet.add(routeKey);
    queued.push({ pathname, routeKey });
  }

  for (const entry of sourceRoutes) enqueue(entry.route);
  ["/", "/dashboard", "/clientes/3-coracoes/guarulhos", "/admin", "/operacoes", "/captacao", "/chamados", "/csc"].forEach(enqueue);

  try {
    while (queued.length && visited.size < maxPages) {
      const { pathname: route, routeKey } = queued.shift();
      queuedSet.delete(routeKey);
      if (visited.has(routeKey)) continue;
      visited.add(routeKey);
      const artifactName = routeToArtifactName(routeKey);
      const screenshotPath = path.join(screenshotsRoot, `${artifactName}.png`);
      const pageDocPath = path.join(pagesRoot, `${artifactName}.md`);
      const capturePage = route === "/" ? anonymousPage : page;

      try {
        const response = await capturePage.goto(new URL(route, base).toString(), {
          waitUntil: "domcontentloaded",
          timeout: 30_000,
        });
        await capturePage.waitForTimeout(700);
        await capturePage
          .locator("h1,h2,h3")
          .filter({ hasText: /carregando/i })
          .first()
          .waitFor({ state: "hidden", timeout: 3_000 })
          .catch(() => {});
        const finalUrl = new URL(capturePage.url());
        if (finalUrl.origin !== base.origin) throw new Error("redirecionamento para origem externa");
        const finalRoute = redactRoutePath(finalUrl.pathname.replace(/\/+$/, "") || "/");
        const status = response?.status() ?? null;
        if (status && status >= 400) throw new Error(`HTTP ${status}`);
        if (!isCanonicalCaptureRoute(route, finalRoute)) {
          results.push({
            route: routeKey,
            finalRoute,
            status: "redirecionada; não usar como referência",
            source: sourceByRoute.get(route),
            artifactName,
            reason: `destino final \`${finalRoute}\``,
          });
          continue;
        }

        const links = await capturePage.locator("a[href]").evaluateAll((elements) =>
          elements.map((element) => element.getAttribute("href")).filter(Boolean),
        );
        for (const href of links) {
          try {
            const candidate = new URL(href, base.origin);
            if (candidate.origin === base.origin) enqueue(candidate.pathname);
          } catch {
            // href inválido não participa do inventário.
          }
        }

        const contract = await collectPageContract(capturePage);
        await redactPageForScreenshot(capturePage);
        await capturePage.screenshot({ path: screenshotPath, fullPage: true, animations: "disabled" });
        const screenshotRelative = path.relative(referencesRoot, screenshotPath);
        await writeFile(
          pageDocPath,
          pageMarkdown({
            route: routeKey,
            finalRoute,
            screenshotRelative,
            contract,
            source: sourceByRoute.get(route),
          }),
          "utf8",
        );
        results.push({ route: routeKey, finalRoute, status: "capturada", source: sourceByRoute.get(route), artifactName });
      } catch (error) {
        results.push({
          route: routeKey,
          finalRoute: "",
          status: "não capturada",
          source: sourceByRoute.get(route),
          artifactName,
          reason: redactRuntimeText(error instanceof Error ? error.message : "falha desconhecida"),
        });
      }
    }
  } finally {
    await anonymousContext.close();
    await context.close();
    await browser.close();
  }

  const source = await extractSourceReferences(sourceRoutes);
  await writeSourceReferenceDocs(referencesRoot, source);
  const routeRows = results
    .map((result) =>
      `| \`${result.route}\` | ${result.status} | ${result.source ? `\`${result.source}\`` : "descoberta em runtime"} | ${result.reason ? mdCell(result.reason) : `[referência](pages/${result.artifactName}.md)`} |`,
    )
    .join("\n");
  await writeFile(
    path.join(referencesRoot, "routes.md"),
    `# Inventário de rotas e capturas\n\n` +
      `Gerado do código e dos links autenticados do localhost. Rotas com identificadores dinâmicos entram quando aparecem como links reais.\n\n` +
      `| Rota | Resultado | Fonte | Evidência |\n| --- | --- | --- | --- |\n${routeRows}\n`,
    "utf8",
  );
  return results;
}

async function main() {
  const { values } = parseArgs({
    options: {
      "base-url": { type: "string" },
      "storage-state": { type: "string" },
      output: { type: "string" },
      "max-pages": { type: "string" },
    },
    strict: true,
  });
  const maxPages = Number(values["max-pages"] ?? DEFAULT_MAX_PAGES);
  if (!Number.isInteger(maxPages) || maxPages < 1 || maxPages > 500) {
    throw new Error("--max-pages deve estar entre 1 e 500.");
  }
  const results = await capture({
    baseUrl: values["base-url"] ?? "http://localhost:3000",
    storageState: path.resolve(values["storage-state"] ?? DEFAULT_STORAGE_STATE),
    referencesRoot: path.resolve(values.output ?? DEFAULT_REFERENCES_ROOT),
    maxPages,
  });
  const captured = results.filter((result) => result.status === "capturada").length;
  const redirected = results.filter((result) => result.status.startsWith("redirecionada")).length;
  const failed = results.length - captured - redirected;
  process.stdout.write(
    `Referências atualizadas: ${captured} tela(s) capturada(s), ${redirected} redirecionada(s), ${failed} falha(s).\n`,
  );
  if (!captured) process.exitCode = 1;
}

if (process.argv[1] && path.resolve(process.argv[1]) === SCRIPT_PATH) {
  main().catch((error) => {
    process.stderr.write(`Falha ao capturar o design do ERP: ${redactRuntimeText(error instanceof Error ? error.message : "falha desconhecida")}\n`);
    process.exitCode = 1;
  });
}
