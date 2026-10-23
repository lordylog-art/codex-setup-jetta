import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { pathToFileURL } from 'node:url';

function number(value, min, max, name) {
  if (typeof value !== 'number' || !Number.isFinite(value) || value < min || value > max) throw new Error(`Invalid ${name}`);
  return value;
}

export function risk(scores) {
  const weights = { I: 0.35, P: 0.25, E: 0.20, C: 0.20 };
  return Math.round(Object.entries(weights).reduce((sum, [key, weight]) => {
    const value = number(scores[key], 0, 4, key);
    if (!Number.isInteger(value)) throw new Error(`Invalid ordinal ${key}`);
    return sum + 100 * weight * value / 4;
  }, 0) * 100) / 100;
}

export function utility(candidate) {
  const weights = { G: 0.30, N: 0.20, H: 0.20, U: 0.15, A: 0.15 };
  const benefit = Object.entries(weights).reduce((sum, [key, weight]) => sum + weight * number(candidate[key], 0, 1, key), 0);
  const minutes = number(candidate.T, Number.MIN_VALUE, Number.MAX_VALUE, 'T');
  return number(candidate.R, 0, 100, 'R') / 100 * benefit * (1 - number(candidate.D, 0, 1, 'D')) / minutes;
}

export function rank(candidates, budgetMinutes) {
  number(budgetMinutes, 0, Number.MAX_VALUE, 'budgetMinutes');
  if (!Array.isArray(candidates)) throw new Error('Expected candidates array');
  const ids = new Set();
  const evaluated = candidates.map(candidate => {
    if (typeof candidate.scenarioId !== 'string' || !candidate.scenarioId.trim() || ids.has(candidate.scenarioId)) throw new Error('Invalid or duplicate scenarioId');
    ids.add(candidate.scenarioId);
    if (typeof candidate.eligible !== 'boolean' || !Array.isArray(candidate.mandatoryReasons) || candidate.mandatoryReasons.some(x => typeof x !== 'string' || !x.trim())) throw new Error('Expected eligibility and mandatoryReasons');
    return { ...candidate, impact: number(candidate.impact, 0, 4, 'impact'), score: utility(candidate) };
  });
  const compare = (a, b) => b.score - a.score || b.impact - a.impact || a.T - b.T || (a.scenarioId < b.scenarioId ? -1 : a.scenarioId > b.scenarioId ? 1 : 0);
  const mandatory = evaluated.filter(x => x.mandatoryReasons.length);
  const mandatoryFeasible = mandatory.every(x => x.eligible) && mandatory.reduce((sum, x) => sum + x.T, 0) <= budgetMinutes;
  let remaining = budgetMinutes;
  const selected = [], deferred = [];
  for (const item of [...mandatory.sort(compare), ...evaluated.filter(x => !x.mandatoryReasons.length).sort(compare)]) {
    if (item.eligible && item.T <= remaining && (item.mandatoryReasons.length || mandatoryFeasible)) {
      selected.push(item); remaining -= item.T;
    } else deferred.push(item);
  }
  return {
    selected, deferred, remainingMinutes: remaining,
    mandatoryFeasible,
  };
}

function choose(items, count) {
  if (!count) return [[]];
  return items.flatMap((item, index) => choose(items.slice(index + 1), count - 1).map(rest => [item, ...rest]));
}

function universe(model) {
  if (model?.schemaVersion !== 1 || !model.factors || Array.isArray(model.factors)) throw new Error('Expected model schemaVersion 1 and factors object');
  const names = Object.keys(model.factors);
  if (names.length < 2 || names.length > 12 || ![2, 3].includes(model.strength) || model.strength > names.length) throw new Error('Expected 2–12 factors and strength 2 or 3');
  let combinations = 1;
  for (const [name, values] of Object.entries(model.factors)) {
    if (!name.trim() || !Array.isArray(values) || !values.length || values.some(x => !['string', 'number', 'boolean'].includes(typeof x) || (typeof x === 'number' && !Number.isFinite(x))) || new Set(values).size !== values.length) throw new Error(`Invalid values for ${name}`);
    combinations *= values.length;
  }
  // shortcut: bounded enumeration, use ACTS for models above these local limits.
  if (combinations > 20_000) throw new Error('Model exceeds 20000 assignments; split the model or use ACTS');
  const forbidden = model.forbidden ?? [];
  if (!Array.isArray(forbidden) || forbidden.some(rule => !rule || Array.isArray(rule) || typeof rule !== 'object' || Object.entries(rule).some(([name, value]) => !names.includes(name) || !model.factors[name].includes(value)))) throw new Error('Invalid forbidden conjunction');
  let assignments = [{}];
  for (const name of names) assignments = assignments.flatMap(row => model.factors[name].map(value => ({ ...row, [name]: value })));
  assignments = assignments.filter(row => !forbidden.some(rule => Object.entries(rule).every(([name, value]) => row[name] === value)));
  if (!assignments.length) throw new Error('Unsatisfiable model');
  const groups = choose(names, model.strength);
  if (assignments.length * groups.length > 100_000) throw new Error('Model exceeds local tuple work limit; split the model or use ACTS');
  return { names, assignments, groups };
}

function tupleKey(row, group) { return JSON.stringify(group.map(name => [name, row[name]])); }

export function generateCoveringArray(model) {
  const { assignments, groups } = universe(model);
  const candidates = assignments.map(row => ({ row, keys: groups.map(group => tupleKey(row, group)) }));
  const remaining = new Set(candidates.flatMap(x => x.keys));
  const rows = [];
  let work = 0;
  while (remaining.size) {
    let best, gain = 0;
    for (const candidate of candidates) {
      work += candidate.keys.length;
      if (work > 10_000_000) throw new Error('Generation exceeds local work limit; use ACTS');
      const uncovered = candidate.keys.filter(key => remaining.has(key)).length;
      if (uncovered > gain) { gain = uncovered; best = candidate; }
    }
    if (!best) throw new Error('No progress covering tuples');
    rows.push(best.row);
    best.keys.forEach(key => remaining.delete(key));
  }
  return { schemaVersion: 1, algorithm: 'bounded-greedy-v1', modelSha256: createHash('sha256').update(JSON.stringify(model)).digest('hex'), strength: model.strength, rows };
}

export function measureCoverage(model, rows) {
  const { names, assignments, groups } = universe(model);
  if (!Array.isArray(rows) || rows.length > 20_000) throw new Error('Expected at most 20000 measured rows');
  const validAssignments = new Set(assignments.map(row => JSON.stringify(names.map(name => row[name]))));
  for (const row of rows) {
    if (!row || Object.keys(row).length !== names.length || names.some(name => !Object.hasOwn(row, name)) || !validAssignments.has(JSON.stringify(names.map(name => row[name])))) throw new Error('Invalid measured assignment');
  }
  let covered = 0, total = 0;
  for (const group of groups) {
    const valid = new Set(assignments.map(row => tupleKey(row, group)));
    const observed = new Set(rows.map(row => tupleKey(row, group)));
    total += valid.size;
    covered += [...valid].filter(key => observed.has(key)).length;
  }
  return { covered, total, ratio: total ? covered / total : null };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    const [command, ...args] = process.argv.slice(2);
    const read = file => JSON.parse(readFileSync(file, 'utf8').replace(/^\uFEFF/, ''));
    let result;
    if (command === 'risk' && args.length === 4) result = { risk: risk(Object.fromEntries(['I', 'P', 'E', 'C'].map((key, index) => [key, Number(args[index])]))) };
    else if (command === 'cover' && args.length === 1) result = generateCoveringArray(read(args[0]));
    else if (command === 'measure' && args.length === 2) {
      const rows = read(args[1]); result = measureCoverage(read(args[0]), Array.isArray(rows) ? rows : rows.rows);
    } else if (command === 'rank' && args.length === 2) result = rank(read(args[0]), Number(args[1]));
    else throw new Error('Usage: plan.mjs risk I P E C | cover model.json | measure model.json rows.json | rank candidates.json worker-minutes');
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  } catch (error) { process.stderr.write(`${error.message}\n`); process.exitCode = 2; }
}
