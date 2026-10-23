import { readFileSync, realpathSync, statSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';

const outcomes = ['PASS', 'FAIL', 'BLOCKED', 'INCONCLUSIVE'];
const boundaries = ['static', 'component', 'browser-mocked-api', 'real-browser', 'real-http', 'real-http-and-database', 'real-browser-http-and-database', 'external-integration'];
const fingerprintFields = ['baseSha', 'headSha', 'localDeltaHash', 'contractHash', 'servedContentHash', 'environmentHash'];
function requireThat(condition, message) { if (!condition) throw new Error(message); }
function text(value) { return typeof value === 'string' && value.trim().length > 0; }
function strings(value) { return Array.isArray(value) && value.length > 0 && value.every(text) && new Set(value).size === value.length; }
function index(items, key) {
  requireThat(Array.isArray(items), `Expected ${key} array`);
  const result = new Map();
  for (const item of items) {
    requireThat(item && text(item[key]) && !result.has(item[key]), `Missing or duplicate ${key}`);
    result.set(item[key], item);
  }
  return result;
}
function checkFingerprint(value) {
  requireThat(value && fingerprintFields.every(key => typeof value[key] === 'string' && new RegExp(key.endsWith('Sha') ? '^[a-f0-9]{40}$' : '^[a-f0-9]{64}$').test(value[key])), 'Invalid fingerprint');
}

export function validateRun(run, artifactRoot) {
  requireThat(run?.schemaVersion === 1 && text(run.runId) && text(run.ticketId), 'Expected run schemaVersion 1, runId and ticketId');
  requireThat(['Quick', 'Standard', 'Deep'].includes(run.mode), 'Invalid mode');
  checkFingerprint(run.fingerprint);
  requireThat(run.environment && text(run.environment.authorizationRef) && text(run.environment.isolationRef) && run.environment.syntheticDataOnly === true && run.environment.externalEffectsDisabled === true, 'Missing authorized synthetic isolated environment');
  requireThat(run.modeReview && typeof run.modeReview.satisfied === 'boolean' && text(run.modeReview.reviewer) && text(run.modeReview.rationale), 'Missing explicit mode review');
  const requirements = index(run.requirements, 'requirementId');
  requireThat(requirements.size > 0, 'No requirements');
  const scenarios = index(run.scenarios, 'scenarioId');
  const attempts = index(run.attempts, 'executionId');
  const evidence = index(run.evidence, 'evidenceId');
  const findings = index(run.findings, 'findingId');
  const obligations = new Map();
  for (const requirement of requirements.values()) {
    requireThat(typeof requirement.risk === 'number' && Number.isFinite(requirement.risk) && requirement.risk >= 0 && requirement.risk <= 100, 'Invalid requirement risk');
    requireThat(Array.isArray(requirement.obligations) && requirement.obligations.length, 'Requirement needs obligations');
    for (const obligation of requirement.obligations) {
      requireThat(obligation && text(obligation.obligationId) && !obligations.has(obligation.obligationId) && typeof obligation.mandatory === 'boolean' && boundaries.includes(obligation.requiredBoundary), 'Invalid or duplicate obligation or required boundary');
      obligations.set(obligation.obligationId, obligation);
    }
  }
  for (const scenario of scenarios.values()) {
    requireThat(strings(scenario.obligationIds) && scenario.obligationIds.every(id => obligations.has(id)), 'Scenario references unknown obligation');
    requireThat(/^[A-H]$/.test(scenario.persona) && text(scenario.oracle?.source) && text(scenario.oracle?.expected) && boundaries.includes(scenario.requiredBoundary), 'Missing persona, oracle or required boundary');
    requireThat(scenario.obligationIds.every(id => obligations.get(id).requiredBoundary === scenario.requiredBoundary), 'Scenario cannot change obligation required boundary');
    requireThat(scenario.notRunReason == null || text(scenario.notRunReason), 'Invalid notRunReason');
  }
  const root = realpathSync(artifactRoot);
  for (const item of evidence.values()) {
    requireThat(item.runId === run.runId && attempts.has(item.executionId), 'Evidence belongs to another run or execution');
    requireThat(text(item.path) && !path.isAbsolute(item.path) && !path.win32.isAbsolute(item.path) && !item.path.split(/[\\/]/).includes('..'), 'Unsafe evidence path');
    const resolved = realpathSync(path.resolve(root, item.path));
    const relative = path.relative(root, resolved);
    requireThat(relative && !relative.startsWith(`..${path.sep}`) && relative !== '..' && !path.isAbsolute(relative) && statSync(resolved).isFile(), 'Evidence escapes artifact root or is not a file');
    requireThat(item.sanitized === true && boundaries.includes(item.mechanism), 'Evidence must declare sanitization and mechanism');
    requireThat(typeof item.sha256 === 'string' && /^[a-f0-9]{64}$/.test(item.sha256) && createHash('sha256').update(readFileSync(resolved)).digest('hex') === item.sha256, 'Evidence hash mismatch');
  }
  const scenarioAttempts = new Map([...scenarios.keys()].map(id => [id, []]));
  for (const attempt of attempts.values()) {
    requireThat(scenarios.has(attempt.scenarioId) && Number.isInteger(attempt.attempt) && attempt.attempt >= 1 && attempt.attempt <= 3, 'Invalid scenario or attempt number');
    requireThat(outcomes.includes(attempt.outcome) && ['NONE', 'PRODUCT', 'TEST', 'ENVIRONMENT', 'ORACLE_UNKNOWN'].includes(attempt.failureClass) && boundaries.includes(attempt.boundary), 'Invalid outcome, classification or boundary');
    checkFingerprint(attempt.fingerprint);
    requireThat(fingerprintFields.every(key => attempt.fingerprint[key] === run.fingerprint[key]), 'Execution fingerprint differs from run');
    const start = Date.parse(attempt.startedAt), end = Date.parse(attempt.endedAt);
    requireThat(Number.isFinite(start) && Number.isFinite(end) && end >= start, 'Invalid execution timestamps');
    requireThat(Array.isArray(attempt.evidenceIds) && new Set(attempt.evidenceIds).size === attempt.evidenceIds.length && attempt.evidenceIds.every(id => evidence.has(id) && evidence.get(id).executionId === attempt.executionId && evidence.get(id).mechanism === attempt.boundary), 'Missing or unrelated execution evidence');
    if (['PASS', 'FAIL'].includes(attempt.outcome)) requireThat(strings(attempt.assertions) && strings(attempt.evidenceIds), 'Conclusive execution needs assertions and evidence');
    if (attempt.outcome === 'PASS') requireThat(attempt.failureClass === 'NONE', 'PASS cannot hide failure classification');
    if (attempt.outcome === 'FAIL') requireThat(attempt.failureClass !== 'NONE', 'FAIL needs triage classification');
    const previous = scenarioAttempts.get(attempt.scenarioId);
    requireThat(!previous.some(x => x.attempt === attempt.attempt), 'Duplicate attempt ordinal');
    previous.push(attempt);
  }
  for (const finding of findings.values()) {
    requireThat(typeof finding.confirmed === 'boolean' && attempts.has(finding.executionId), 'Invalid finding execution');
    requireThat(strings(finding.evidenceIds) && finding.evidenceIds.every(id => evidence.has(id) && evidence.get(id).executionId === finding.executionId), 'Finding requires related evidence');
    if (finding.confirmed) {
      const attempt = attempts.get(finding.executionId);
      requireThat(['P0', 'P1', 'P2', 'P3'].includes(finding.severity) && text(finding.expected) && text(finding.observed) && strings(finding.reproduction), 'Confirmed finding needs severity and reproduction');
      requireThat(attempt.outcome === 'FAIL' && attempt.failureClass === 'PRODUCT', 'Confirmed product finding needs failed product execution');
    }
  }
  for (const attempt of attempts.values()) if (attempt.outcome === 'FAIL' && attempt.failureClass === 'PRODUCT') {
    requireThat([...findings.values()].some(finding => finding.confirmed && finding.executionId === attempt.executionId), 'Product failure needs a confirmed reproducible finding');
  }
  const states = new Map();
  for (const [id, scenario] of scenarios) {
    const history = scenarioAttempts.get(id).sort((a, b) => a.attempt - b.attempt);
    const latest = history.at(-1);
    let status = scenario.notRunReason ? 'BLOCKED' : 'INCONCLUSIVE';
    if (latest) {
      status = latest.outcome;
      if (status === 'FAIL' && latest.failureClass !== 'PRODUCT') status = 'INCONCLUSIVE';
      if (latest.boundary !== scenario.requiredBoundary) status = 'INCONCLUSIVE';
      if (status === 'PASS' && history.some(x => x.outcome !== 'PASS')) {
        const review = scenario.instabilityReview;
        if (!review || !text(review.reviewer) || !text(review.rationale) || !strings(review.evidenceIds) || !review.evidenceIds.every(key => evidence.has(key) && history.some(x => x.executionId === evidence.get(key).executionId))) status = 'INCONCLUSIVE';
      }
    }
    if (history.some(x => x.outcome === 'FAIL' && x.failureClass === 'PRODUCT' && x.boundary === scenario.requiredBoundary)) status = 'FAIL';
    states.set(id, status);
  }
  const obligationStates = new Map();
  for (const [id] of obligations) {
    const related = [...scenarios.values()].filter(x => x.obligationIds.includes(id)).map(x => states.get(x.scenarioId));
    const status = related.includes('FAIL') ? 'FAIL' : related.includes('PASS') ? 'PASS' : related.includes('BLOCKED') ? 'BLOCKED' : 'INCONCLUSIVE';
    obligationStates.set(id, status);
  }
  let requirementsVerified = 0, requirementsPassed = 0, riskTotal = 0, riskVerified = 0;
  for (const requirement of requirements.values()) {
    const statuses = requirement.obligations.map(x => obligationStates.get(x.obligationId));
    const verified = statuses.every(x => ['PASS', 'FAIL'].includes(x));
    if (verified) { requirementsVerified++; riskVerified += requirement.risk; }
    if (statuses.every(x => x === 'PASS')) requirementsPassed++;
    riskTotal += requirement.risk;
  }
  const pendingObligations = [...obligations.values()].filter(x => !['PASS', 'FAIL'].includes(obligationStates.get(x.obligationId))).map(x => ({ ...x, status: obligationStates.get(x.obligationId) }));
  const mandatoryPending = pendingObligations.filter(x => x.mandatory);
  const confirmed = [...findings.values()].filter(x => x.confirmed);
  const inconclusiveExecution = [...states].some(([id, value]) => value === 'INCONCLUSIVE' && scenarioAttempts.get(id).length > 0);
  const status = confirmed.length ? 'FAIL'
    : mandatoryPending.some(x => x.status === 'BLOCKED') ? 'BLOCKED'
      : !requirementsVerified || mandatoryPending.length || !run.modeReview.satisfied || inconclusiveExecution ? 'INCONCLUSIVE' : 'PASS';
  return {
    schemaVersion: 1, runId: run.runId, status,
    releaseRecommendation: status === 'PASS' ? 'ELIGIBLE_FOR_REVIEW' : 'HOLD',
    requirementsVerified, requirementsPassed, requirementsTotal: requirements.size,
    riskCoverage: riskTotal ? riskVerified / riskTotal : null,
    scenariosTotal: scenarios.size, attemptsTotal: attempts.size,
    scenarioResults: Object.fromEntries(states), pendingObligations,
    confirmedFindingIds: confirmed.map(x => x.findingId),
    limitation: 'Structural validation only; the orchestrator must review oracle, environment, scope completeness and evidence semantics.',
  };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    requireThat(process.argv.length === 3, 'Usage: validate-run.mjs manifest.json');
    const manifestPath = path.resolve(process.argv[2]);
    const result = validateRun(JSON.parse(readFileSync(manifestPath, 'utf8').replace(/^\uFEFF/, '')), path.dirname(manifestPath));
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    process.exitCode = result.status === 'PASS' ? 0 : 1;
  } catch (error) { process.stderr.write(`${error.message}\n`); process.exitCode = 2; }
}
