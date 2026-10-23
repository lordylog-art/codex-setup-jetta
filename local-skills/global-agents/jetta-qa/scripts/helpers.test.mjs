import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, writeFileSync, rmSync, symlinkSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { risk, utility, rank, generateCoveringArray, measureCoverage } from './plan.mjs';
import { validateRun } from './validate-run.mjs';

test('risco e ranking preservam orçamento, obrigatórios e valores desconhecidos', () => {
  assert.equal(risk({ I: 4, P: 3, E: 3, C: 3 }), 83.75);
  assert.equal(risk({ I: 2, P: 2, E: 3, C: 2 }), 55);
  assert.throws(() => risk({ I: 5, P: 3, E: 3, C: 3 }));
  assert.throws(() => risk({ I: 4, P: null, E: 3, C: 3 }));
  const extra = { scenarioId: 'extra', R: 80, G: 1, N: 1, H: 0.5, U: 1, A: 0, D: 0, T: 4, impact: 4, mandatoryReasons: [], eligible: true };
  assert.ok(Math.abs(utility(extra) - 0.15) < 1e-12);
  assert.throws(() => utility({ ...extra, T: 0 }));
  const mandatory = { ...extra, scenarioId: 'mandatory', mandatoryReasons: ['integrity'], T: 5 };
  const result = rank([extra, mandatory], 6);
  assert.deepEqual(result.selected.map(x => x.scenarioId), ['mandatory']);
  assert.deepEqual(result.deferred.map(x => x.scenarioId), ['extra']);
  assert.equal(rank([mandatory], 4).mandatoryFeasible, false);
  assert.deepEqual(rank([{ ...extra, T: 1 }, mandatory], 4).selected, []);
  assert.equal(rank([{ ...mandatory, eligible: false }], 9).mandatoryFeasible, false);
  assert.throws(() => rank([extra, extra], 10));
});

const binary = { schemaVersion: 1, factors: { A: [0, 1], B: [0, 1], C: [0, 1] }, strength: 2, forbidden: [] };
const rows = [{ A: 0, B: 0, C: 0 }, { A: 0, B: 1, C: 1 }, { A: 1, B: 0, C: 1 }, { A: 1, B: 1, C: 0 }];
test('medição independente distingue 2-way de 3-way e geração é determinística', () => {
  assert.deepEqual(measureCoverage(binary, rows), { covered: 12, total: 12, ratio: 1 });
  assert.deepEqual(measureCoverage({ ...binary, strength: 3 }, rows), { covered: 4, total: 8, ratio: 0.5 });
  const generated = generateCoveringArray(binary);
  assert.equal(measureCoverage(binary, generated.rows).ratio, 1);
  assert.deepEqual(generateCoveringArray(binary), generated);
});
test('restrições contam só tuplas estendíveis, rejeitam entrada impossível e limitam custo', () => {
  const model = { ...binary, forbidden: [{ A: 1, B: 1 }] };
  const generated = generateCoveringArray(model);
  assert.ok(generated.rows.every(row => !(row.A === 1 && row.B === 1)));
  assert.equal(measureCoverage(model, generated.rows).total, 11);
  assert.equal(measureCoverage(model, generated.rows).ratio, 1);
  assert.throws(() => measureCoverage(model, [{ A: 1, B: 1, C: 0 }]));
  assert.throws(() => generateCoveringArray({ ...binary, forbidden: [{}] }));
  assert.throws(() => generateCoveringArray({ ...binary, factors: { A: [0, 0], B: [0, 1] } }));
  assert.throws(() => generateCoveringArray({ ...binary, forbidden: [{ X: 1 }] }));
  assert.throws(() => generateCoveringArray({ ...binary, factors: { A: Array.from({ length: 201 }, (_, i) => i), B: Array.from({ length: 201 }, (_, i) => i) } }));
});

function fixture(t) {
  const dir = mkdtempSync(path.join(tmpdir(), 'jetta-qa-'));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  writeFileSync(path.join(dir, 'proof.txt'), 'synthetic evidence');
  const fingerprint = { baseSha: 'a'.repeat(40), headSha: 'b'.repeat(40), localDeltaHash: 'c'.repeat(64), contractHash: 'd'.repeat(64), servedContentHash: 'e'.repeat(64), environmentHash: 'f'.repeat(64) };
  const run = {
    schemaVersion: 1, runId: 'synthetic-run', ticketId: 'fixture-ticket', mode: 'Quick', fingerprint,
    environment: { authorizationRef: 'synthetic-test-only', isolationRef: 'temporary-directory', syntheticDataOnly: true, externalEffectsDisabled: true },
    modeReview: { reviewer: 'synthetic-reviewer', satisfied: true, rationale: 'isolated helper test, no ERP' },
    requirements: [{ requirementId: 'R1', risk: 80, obligations: [{ obligationId: 'O1', mandatory: true, requiredBoundary: 'component' }] }],
    scenarios: [{ scenarioId: 'S1', obligationIds: ['O1'], persona: 'A', oracle: { source: 'fixture-contract', expected: 'synthetic evidence exists' }, requiredBoundary: 'component', notRunReason: null }],
    attempts: [{ executionId: 'X1', scenarioId: 'S1', attempt: 1, fingerprint: { ...fingerprint }, outcome: 'PASS', failureClass: 'NONE', boundary: 'component', assertions: ['synthetic invariant checked'], evidenceIds: ['E1'], startedAt: '2026-10-19T12:00:00Z', endedAt: '2026-10-19T12:00:01Z' }],
    evidence: [{ evidenceId: 'E1', executionId: 'X1', runId: 'synthetic-run', path: 'proof.txt', sha256: createHash('sha256').update('synthetic evidence').digest('hex'), sanitized: true, mechanism: 'component' }],
    findings: [],
  };
  return { dir, run };
}
test('PASS exige assert, oráculo, proveniência e arquivo íntegro; hash sozinho não prova semântica', t => {
  const { dir, run } = fixture(t);
  assert.equal(validateRun(run, dir).status, 'PASS');
  const bad = structuredClone(run);
  bad.attempts[0].assertions = [];
  assert.throws(() => validateRun(bad, dir));
  bad.attempts[0] = { ...run.attempts[0], fingerprint: { ...run.fingerprint, headSha: '0'.repeat(40) } };
  assert.throws(() => validateRun(bad, dir));
  writeFileSync(path.join(dir, 'proof.txt'), 'tampered');
  assert.throws(() => validateRun(run, dir));
});
test('fronteira simulada não satisfaz obrigação de banco real', t => {
  const { dir, run } = fixture(t);
  run.scenarios[0].requiredBoundary = 'real-http-and-database';
  run.requirements[0].obligations[0].requiredBoundary = 'real-http-and-database';
  assert.equal(validateRun(run, dir).status, 'INCONCLUSIVE');
  assert.equal(validateRun(run, dir).riskCoverage, 0);
});
test('cobertura inclui FAIL confirmado e não inclui bloqueio; FAIL prevalece', t => {
  const { dir, run } = fixture(t);
  run.requirements.push({ requirementId: 'R2', risk: 60, obligations: [{ obligationId: 'O2', mandatory: true, requiredBoundary: 'component' }] }, { requirementId: 'R3', risk: 20, obligations: [{ obligationId: 'O3', mandatory: true, requiredBoundary: 'component' }] });
  run.scenarios[0].obligationIds.push('O2');
  run.scenarios.push({ ...run.scenarios[0], scenarioId: 'S3', obligationIds: ['O3'], notRunReason: 'database unavailable' });
  run.attempts[0].outcome = 'FAIL';
  run.attempts[0].failureClass = 'PRODUCT';
  run.findings.push({ findingId: 'F1', confirmed: true, severity: 'P1', executionId: 'X1', expected: 'valid invariant', observed: 'broken invariant', reproduction: ['prepare fixture', 'observe failure'], evidenceIds: ['E1'] });
  const result = validateRun(run, dir);
  assert.equal(result.status, 'FAIL');
  assert.equal(result.riskCoverage, 0.875);
  assert.equal(result.requirementsVerified, 2);
  assert.equal(result.requirementsPassed, 0);
  assert.equal(result.pendingObligations[0].status, 'BLOCKED');
});
test('ausência de execução e orçamento/oráculo incompletos não geram PASS', t => {
  const { dir, run } = fixture(t);
  run.attempts = []; run.evidence = [];
  assert.equal(validateRun(run, dir).status, 'INCONCLUSIVE');
  run.scenarios[0].notRunReason = 'runtime unavailable';
  assert.equal(validateRun(run, dir).status, 'BLOCKED');
  run.requirements[0].risk = 0;
  assert.equal(validateRun(run, dir).riskCoverage, null);
});
test('nenhum requisito verificado não pode produzir PASS mesmo sem obrigatórios', t => {
  const { dir, run } = fixture(t);
  run.requirements[0].obligations[0].mandatory = false;
  run.attempts = []; run.evidence = [];
  assert.equal(validateRun(run, dir).status, 'INCONCLUSIVE');
});
test('defeito confirmado em fronteira insuficiente bloqueia sem inflar cobertura', t => {
  const { dir, run } = fixture(t);
  run.scenarios[0].requiredBoundary = 'real-http-and-database';
  run.requirements[0].obligations[0].requiredBoundary = 'real-http-and-database';
  run.attempts[0].outcome = 'FAIL'; run.attempts[0].failureClass = 'PRODUCT';
  run.findings.push({ findingId: 'F1', confirmed: true, severity: 'P1', executionId: 'X1', expected: 'valid invariant', observed: 'broken invariant', reproduction: ['prepare fixture', 'observe failure'], evidenceIds: ['E1'] });
  const result = validateRun(run, dir);
  assert.equal(result.status, 'FAIL');
  assert.equal(result.riskCoverage, 0);
});
test('PASS após falha não esconde flake e nem defeito de produto no mesmo conteúdo', t => {
  const { dir, run } = fixture(t);
  const second = structuredClone(run.attempts[0]);
  second.executionId = 'X2'; second.attempt = 2; second.evidenceIds = ['E2'];
  run.evidence.push({ ...run.evidence[0], evidenceId: 'E2', executionId: 'X2' });
  run.attempts[0].outcome = 'FAIL'; run.attempts[0].failureClass = 'TEST';
  run.attempts.push(second);
  assert.equal(validateRun(run, dir).status, 'INCONCLUSIVE');
  run.scenarios[0].instabilityReview = { reviewer: 'synthetic-reviewer', rationale: 'fixture setup corrected, invariant preserved', evidenceIds: ['E1', 'E2'] };
  assert.equal(validateRun(run, dir).status, 'PASS');
  run.attempts[0].failureClass = 'PRODUCT';
  run.findings.push({ findingId: 'F1', confirmed: true, severity: 'P2', executionId: 'X1', expected: 'valid invariant', observed: 'broken invariant', reproduction: ['prepare fixture', 'observe failure'], evidenceIds: ['E1'] });
  assert.equal(validateRun(run, dir).status, 'FAIL');
});
test('alternativa simulada não rebaixa fronteira de obrigação congelada', t => {
  const { dir, run } = fixture(t);
  run.requirements[0].obligations[0].requiredBoundary = 'real-http-and-database';
  run.scenarios.push({ ...run.scenarios[0], scenarioId: 'SDB', requiredBoundary: 'real-http-and-database', notRunReason: 'database unavailable' });
  assert.throws(() => validateRun(run, dir), /boundary/i);
});
test('IDs conflitantes, versões, evidência alheia e caminhos externos são rejeitados', t => {
  const { dir, run } = fixture(t);
  for (const change of [
    x => { x.schemaVersion = 2; },
    x => { x.evidence.push({ ...x.evidence[0] }); },
    x => { x.evidence[0].path = '../outside.txt'; },
    x => { x.evidence[0].path = path.resolve(dir, 'proof.txt'); },
    x => { x.evidence[0].executionId = 'OTHER'; },
    x => { x.evidence[0].runId = 'OTHER'; },
    x => { x.attempts[0].evidenceIds = ['MISSING']; },
    x => { x.scenarios[0].oracle.expected = ''; },
    x => { x.scenarios[0].obligationIds = ['UNKNOWN']; },
  ]) {
    const bad = structuredClone(run); change(bad);
    assert.throws(() => validateRun(bad, dir));
  }
});
test('symlink que escapa da raiz não pode servir de evidência', t => {
  const { dir, run } = fixture(t);
  const outside = mkdtempSync(path.join(tmpdir(), 'jetta-qa-outside-'));
  t.after(() => rmSync(outside, { recursive: true, force: true }));
  writeFileSync(path.join(outside, 'proof.txt'), 'synthetic evidence');
  symlinkSync(outside, path.join(dir, 'escape'), process.platform === 'win32' ? 'junction' : 'dir');
  run.evidence[0].path = 'escape/proof.txt';
  assert.throws(() => validateRun(run, dir));
});
