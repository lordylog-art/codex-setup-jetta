import assert from "node:assert/strict";
import { readdir, readFile } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import {
  assertLocalBaseUrl,
  isCanonicalCaptureRoute,
  isInspectableRoute,
  redactRoutePath,
  redactRuntimeText,
  routeToArtifactName,
  sanitizeImageSource,
} from "./capture-erp-design.mjs";

const SKILL_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const REFERENCES_ROOT = path.join(SKILL_ROOT, "references");

test("aceita somente origens locais sem credenciais, query ou fragmento", () => {
  assert.equal(assertLocalBaseUrl("http://localhost:3000").origin, "http://localhost:3000");
  assert.equal(assertLocalBaseUrl("http://127.0.0.1:3000").origin, "http://127.0.0.1:3000");
  assert.throws(() => assertLocalBaseUrl("https://erp.exemplo.com"), /localhost/i);
  assert.throws(() => assertLocalBaseUrl("http://user:secret@localhost:3000"), /credenciais/i);
  assert.throws(() => assertLocalBaseUrl("http://localhost:3000/?token=abc"), /query|fragmento/i);
});

test("inspeciona somente páginas GET seguras do aplicativo", () => {
  assert.equal(isInspectableRoute("/clientes/3-coracoes/guarulhos/programacao/programacao"), true);
  assert.equal(isInspectableRoute("/admin/usuarios"), true);
  assert.equal(isInspectableRoute("/api/auth/me"), false);
  assert.equal(isInspectableRoute("/logout"), false);
  assert.equal(isInspectableRoute("/formulario/segredo"), false);
  assert.equal(isInspectableRoute("https://externo.example/path"), false);
});

test("não aceita redirecionamento como referência da rota solicitada", () => {
  assert.equal(isCanonicalCaptureRoute("/admin/usuarios", "/admin/usuarios"), true);
  assert.equal(
    isCanonicalCaptureRoute(
      "/clientes/3-coracoes/guarulhos/cadastros/motoristas/4f935324-e832-4205-a55b-7bdd18ddd115",
      "/clientes/3-coracoes/guarulhos/cadastros/motoristas/4f935324-e832-4205-a55b-7bdd18ddd115",
    ),
    true,
  );
  assert.equal(
    isCanonicalCaptureRoute("/clientes/cooperflora/guarulhos/cadastros/motoristas", "/selecionar-cliente"),
    false,
  );
});

test("redige valores operacionais sem apagar rótulos estruturais", () => {
  const input = "Motorista João da Silva | Placa ABC1D23 | reserva DEF-1234 | CPF 123.456.789-00 | Status Em rota";
  const output = redactRuntimeText(input);
  assert.match(output, /Motorista \[conteúdo redigido\]/);
  assert.match(output, /Placa \[conteúdo redigido\]/);
  assert.match(output, /CPF \[conteúdo redigido\]/);
  assert.match(output, /Status Em rota/);
  assert.doesNotMatch(output, /João|ABC1D23|123\.456/);
  assert.doesNotMatch(output, /DEF-1234/);
});

test("redige identificadores concretos de rotas descobertas", () => {
  assert.equal(
    redactRoutePath("/admin/clientes/0dcb2583-e70b-4068-a1b2-dae455c14bef"),
    "/admin/clientes/[item]",
  );
  assert.equal(
    redactRoutePath("/clientes/3-coracoes/guarulhos/cadastros/e-mails/email-contact-004"),
    "/clientes/3-coracoes/guarulhos/cadastros/e-mails/[item]",
  );
  assert.equal(
    redactRoutePath("/clientes/3-coracoes/guarulhos/cadastros/ocorrencias/3coracoes-incident-type-016"),
    "/clientes/3-coracoes/guarulhos/cadastros/ocorrencias/[item]",
  );
});

test("gera nomes determinísticos e seguros para artefatos", () => {
  assert.equal(routeToArtifactName("/"), "inicio");
  assert.equal(
    routeToArtifactName("/clientes/3-coracoes/guarulhos/cadastros/motoristas"),
    "clientes__3-coracoes__guarulhos__cadastros__motoristas",
  );
});

test("não incorpora imagens privadas ou efêmeras nos arquivos Markdown", () => {
  assert.equal(sanitizeImageSource("data:image/jpeg;base64,segredo"), "[imagem incorporada omitida]");
  assert.equal(sanitizeImageSource("blob:http://localhost:3000/uuid"), "[imagem temporária omitida]");
  assert.equal(sanitizeImageSource("/images/vehicles/toco.png"), "/images/vehicles/toco.png");
});

test("mantém uma captura visual para cada referência de página", async () => {
  const pages = (await readdir(path.join(REFERENCES_ROOT, "pages"))).filter((name) => name.endsWith(".md"));
  const screenshots = new Set(await readdir(path.join(REFERENCES_ROOT, "screenshots")));
  assert.ok(pages.length >= 1);
  for (const pageName of pages) {
    assert.ok(screenshots.has(pageName.replace(/\.md$/, ".png")), `screenshot ausente para ${pageName}`);
  }
});

test("não persiste identificadores pessoais nas referências de runtime", async () => {
  const pageNames = (await readdir(path.join(REFERENCES_ROOT, "pages"))).filter((name) => name.endsWith(".md"));
  const contents = await Promise.all([
    readFile(path.join(REFERENCES_ROOT, "routes.md"), "utf8"),
    ...pageNames.map((name) => readFile(path.join(REFERENCES_ROOT, "pages", name), "utf8")),
  ]);
  const joined = contents.join("\n");
  assert.doesNotMatch(joined, /data:image|blob:http/i);
  assert.doesNotMatch(joined, /\b(?:[A-Z]{3}[0-9][A-Z0-9][0-9]{2}|[A-Z]{3}-?[0-9]{4})\b/);
  assert.doesNotMatch(joined, /\b\d{3}\.\d{3}\.\d{3}-\d{2}\b/);
  assert.doesNotMatch(joined, /\b[0-9a-f]{8}-[0-9a-f-]{27,}\b/i);
  assert.doesNotMatch(joined, /[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}/);
});
