#!/usr/bin/env node
import { spawn } from "node:child_process";
import { createRequire } from "node:module";
import {
  existsSync,
  mkdirSync,
  readdirSync,
  readFileSync,
  statSync,
  writeFileSync,
} from "node:fs";
import { dirname, extname, isAbsolute, resolve } from "node:path";
import { setTimeout as delay } from "node:timers/promises";

const SOURCE_EXTENSIONS = new Set([".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"]);
const DEFAULT_IGNORES = new Set([
  ".git",
  ".next",
  ".turbo",
  "coverage",
  "dist",
  "generated",
  "logs",
  "node_modules",
  "playwright-report",
  "test-results",
  "tmp",
]);

function parseArgs(argv) {
  const args = {
    paths: [],
    language: "pt-BR",
    out: "tmp/corretor-ortografico-report.json",
    languageTool: "tools/LanguageTool",
    serverUrl: "http://127.0.0.1:8010",
    minLength: 3,
    includeTests: false,
    maxItems: 0,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = argv[i + 1];
    if (arg === "--path") {
      args.paths.push(next);
      i += 1;
    } else if (arg === "--language") {
      args.language = next;
      i += 1;
    } else if (arg === "--out") {
      args.out = next;
      i += 1;
    } else if (arg === "--language-tool") {
      args.languageTool = next;
      i += 1;
    } else if (arg === "--server-url") {
      args.serverUrl = next.replace(/\/$/, "");
      i += 1;
    } else if (arg === "--min-length") {
      args.minLength = Number(next);
      i += 1;
    } else if (arg === "--max-items") {
      args.maxItems = Number(next);
      i += 1;
    } else if (arg === "--include-tests") {
      args.includeTests = true;
    } else if (arg === "--help" || arg === "-h") {
      args.help = true;
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }

  if (args.paths.length === 0) args.paths = ["apps/web/src", "apps/api/src"];
  return args;
}

function usage() {
  return `Usage:
  node audit-source-copy.mjs --path apps/web/src [--path apps/api/src]

Options:
  --language pt-BR
  --language-tool tools/LanguageTool
  --server-url http://127.0.0.1:8010
  --out tmp/corretor-ortografico-report.json
  --min-length 3
  --max-items 200
  --include-tests`;
}

async function isLanguageToolReady(serverUrl) {
  try {
    const response = await fetch(`${serverUrl}/v2/languages`, {
      signal: AbortSignal.timeout(2000),
    });
    return response.ok;
  } catch {
    return false;
  }
}

async function startLanguageTool(args) {
  if (await isLanguageToolReady(args.serverUrl)) {
    return { started: false, stop: async () => {} };
  }

  const toolDir = isAbsolute(args.languageTool)
    ? args.languageTool
    : resolve(process.cwd(), args.languageTool);
  const jar = resolve(toolDir, "languagetool-server.jar");
  if (!existsSync(jar)) {
    throw new Error(`LanguageTool server jar not found: ${jar}`);
  }

  const port = new URL(args.serverUrl).port || "8010";
  const child = spawn("java", ["-jar", jar, "--port", port], {
    cwd: toolDir,
    stdio: ["ignore", "pipe", "pipe"],
    windowsHide: true,
  });

  let stderr = "";
  child.stderr.on("data", (chunk) => {
    stderr += chunk.toString();
  });

  for (let attempt = 0; attempt < 60; attempt += 1) {
    if (await isLanguageToolReady(args.serverUrl)) {
      return {
        started: true,
        stop: async () => {
          child.kill();
          await delay(200);
        },
      };
    }
    await delay(500);
  }

  child.kill();
  throw new Error(`LanguageTool server did not start. ${stderr.trim()}`);
}

async function checkText(serverUrl, language, text) {
  const body = new URLSearchParams();
  body.set("language", language);
  body.set("text", text);

  const response = await fetch(`${serverUrl}/v2/check`, {
    method: "POST",
    headers: { "content-type": "application/x-www-form-urlencoded" },
    body,
  });

  if (!response.ok) {
    throw new Error(`LanguageTool check failed: ${response.status} ${await response.text()}`);
  }

  const result = await response.json();
  return result.matches ?? [];
}

function applySuggestions(text, matches) {
  const applicable = matches
    .filter((match) => match.replacements?.[0]?.value && Number.isInteger(match.offset))
    .sort((a, b) => b.offset - a.offset);

  let output = text;
  for (const match of applicable) {
    const replacement = match.replacements[0].value;
    output = `${output.slice(0, match.offset)}${replacement}${output.slice(match.offset + match.length)}`;
  }
  return output;
}

function loadTypeScript() {
  const requireFromProject = createRequire(resolve(process.cwd(), "package.json"));
  try {
    return requireFromProject("typescript");
  } catch (error) {
    throw new Error(`Cannot import TypeScript from this project. ${error.message}`);
  }
}

function listSourceFiles(inputPaths, includeTests) {
  const files = [];

  function visit(path) {
    const fullPath = isAbsolute(path) ? path : resolve(process.cwd(), path);
    if (!existsSync(fullPath)) return;

    const stat = statSync(fullPath);
    if (stat.isDirectory()) {
      const name = fullPath.split(/[\\/]/).pop();
      if (DEFAULT_IGNORES.has(name)) return;
      for (const entry of readdirSync(fullPath)) visit(resolve(fullPath, entry));
      return;
    }

    if (!stat.isFile()) return;
    if (!SOURCE_EXTENSIONS.has(extname(fullPath))) return;
    if (!includeTests && /\.(spec|test)\.[tj]sx?$/.test(fullPath)) return;
    files.push(fullPath);
  }

  for (const path of inputPaths) visit(path);
  return files.sort();
}

function textLooksHuman(text, minLength) {
  const normalized = text.replace(/\s+/g, " ").trim();
  if (normalized.length < minLength) return false;
  if (!/[A-Za-zÀ-ÿ]/.test(normalized)) return false;
  if (/^https?:\/\//i.test(normalized)) return false;
  if (/^[\w./:@-]+$/.test(normalized) && !/\s/.test(normalized)) return false;
  if (/^[A-Z0-9_./:@-]+$/.test(normalized)) return false;
  if (/^[\d\s.,:/-]+$/.test(normalized)) return false;
  return true;
}

function parentName(node) {
  return node?.name?.escapedText?.toString?.() ?? node?.name?.text ?? "";
}

function shouldSkipStringLiteral(ts, node) {
  const parent = node.parent;
  if (!parent) return false;

  if (
    ts.isImportDeclaration(parent) ||
    ts.isExportDeclaration(parent) ||
    ts.isExternalModuleReference(parent)
  ) {
    return true;
  }

  if (ts.isExpressionStatement(parent) && ts.isSourceFile(parent.parent)) {
    return true;
  }

  if (ts.isJsxAttribute(parent)) {
    const name = parentName(parent);
    return ["className", "href", "src", "style", "id", "data-testid"].includes(name);
  }

  if (ts.isPropertyAssignment(parent)) {
    const name = parentName(parent);
    return ["className", "href", "src", "style", "id", "path", "url", "method"].includes(name);
  }

  return false;
}

function extractStringsFromFile(ts, file) {
  const sourceText = readFileSync(file, "utf8");
  const sourceFile = ts.createSourceFile(file, sourceText, ts.ScriptTarget.Latest, true);
  const items = [];

  function pushText(node, rawText, kind) {
    const text = rawText.replace(/\s+/g, " ").trim();
    const pos = ts.getLineAndCharacterOfPosition(sourceFile, node.getStart(sourceFile));
    items.push({
      file,
      line: pos.line + 1,
      column: pos.character + 1,
      kind,
      text,
    });
  }

  function visit(node) {
    if ((ts.isStringLiteral(node) || ts.isNoSubstitutionTemplateLiteral(node)) && !shouldSkipStringLiteral(ts, node)) {
      pushText(node, node.text, ts.SyntaxKind[node.kind]);
    } else if (ts.isJsxText(node)) {
      pushText(node, node.getText(sourceFile), "JsxText");
    } else if (ts.isTemplateHead(node) || ts.isTemplateMiddle(node) || ts.isTemplateTail(node)) {
      pushText(node, node.text, ts.SyntaxKind[node.kind]);
    }
    ts.forEachChild(node, visit);
  }

  visit(sourceFile);
  return items;
}

function dedupeItems(items, minLength) {
  const seen = new Map();
  for (const item of items) {
    if (!textLooksHuman(item.text, minLength)) continue;
    const key = item.text;
    const existing = seen.get(key) ?? { text: item.text, occurrences: [] };
    existing.occurrences.push({
      file: item.file,
      line: item.line,
      column: item.column,
      kind: item.kind,
    });
    seen.set(key, existing);
  }
  return [...seen.values()];
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    console.log(usage());
    return;
  }

  const ts = loadTypeScript();
  const files = listSourceFiles(args.paths, args.includeTests);
  const extracted = files.flatMap((file) => extractStringsFromFile(ts, file));
  const uniqueItems = dedupeItems(extracted, args.minLength);
  const itemsToCheck = args.maxItems > 0 ? uniqueItems.slice(0, args.maxItems) : uniqueItems;

  const lt = await startLanguageTool(args);
  try {
    const textsWithIssues = [];
    for (const item of itemsToCheck) {
      const matches = await checkText(args.serverUrl, args.language, item.text);
      if (matches.length > 0) {
        textsWithIssues.push({
          ...item,
          matches: matches.map((match) => ({
            message: match.message,
            ruleId: match.rule?.id,
            offset: match.offset,
            length: match.length,
            context: match.context?.text,
            replacements: (match.replacements ?? []).slice(0, 5).map((replacement) => replacement.value),
          })),
          suggestedText: applySuggestions(item.text, matches),
        });
      }
    }

    const report = {
      generatedAt: new Date().toISOString(),
      language: args.language,
      paths: args.paths,
      languageTool: {
        serverUrl: args.serverUrl,
        startedByScript: lt.started,
      },
      summary: {
        filesScanned: files.length,
        extractedTextCount: extracted.length,
        uniqueTextCount: uniqueItems.length,
        checkedTextCount: itemsToCheck.length,
        issues: textsWithIssues.reduce((sum, item) => sum + item.matches.length, 0),
        textsWithIssues: textsWithIssues.length,
      },
      textsWithIssues,
    };

    const out = resolve(process.cwd(), args.out);
    mkdirSync(dirname(out), { recursive: true });
    writeFileSync(out, `${JSON.stringify(report, null, 2)}\n`, "utf8");
    console.log(`Wrote ${out}`);
    console.log(`Issues: ${report.summary.issues} in ${report.summary.textsWithIssues} text chunks`);
  } finally {
    await lt.stop();
  }
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
