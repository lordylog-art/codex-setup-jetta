import { createWriteStream } from 'node:fs';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { randomBytes } from 'node:crypto';
import { spawn } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const workspace = process.env.CONNECT_FACTORY_WORKSPACE ?? 'C:\\Projetos\\Jeta Move';
const runtimeDir = path.join(workspace, '.runtime', 'connect-agent-factory');
const stateFile = path.join(runtimeDir, 'codex-session.json');
const serverFile = path.join(workspace, 'tools', 'connect-agent-factory', 'server.mjs');
const healthUrl = 'http://127.0.0.1:4317/v1/health';
const command = process.argv[2] ?? 'status';

async function readState() {
  try {
    return JSON.parse(await readFile(stateFile, 'utf8'));
  } catch {
    return null;
  }
}

async function readHealth() {
  try {
    const response = await fetch(healthUrl, { signal: AbortSignal.timeout(2_000) });
    if (!response.ok) return null;
    const body = await response.json();
    return body?.ok === true ? body : null;
  } catch {
    return null;
  }
}

function processExists(pid) {
  if (!Number.isInteger(pid) || pid <= 0) return false;
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

async function status() {
  const [health, state] = await Promise.all([readHealth(), readState()]);
  if (!health) return { state: 'STOPPED', paired: false };
  if (!state?.controlCode || !processExists(state.pid)) {
    return { state: 'RUNNING_CONTROL_UNAVAILABLE', paired: health.paired === true };
  }
  return {
    state: health.paired === true ? 'READY' : 'PAIRING_REQUIRED',
    paired: health.paired === true,
    controlCode: state.controlCode,
    ...(health.paired === true ? {} : { pairingCode: state.controlCode }),
  };
}

async function start() {
  const current = await status();
  if (current.state !== 'STOPPED') return current;

  await mkdir(runtimeDir, { recursive: true });
  const controlCode = randomBytes(18).toString('base64url');
  const stdout = createWriteStream(path.join(runtimeDir, 'skill-server.out.log'), { flags: 'a' });
  const stderr = createWriteStream(path.join(runtimeDir, 'skill-server.err.log'), { flags: 'a' });
  await Promise.all([
    new Promise((resolve, reject) => stdout.once('open', resolve).once('error', reject)),
    new Promise((resolve, reject) => stderr.once('open', resolve).once('error', reject)),
  ]);
  const child = spawn(process.execPath, [fileURLToPath(import.meta.url), 'serve'], {
    detached: true,
    windowsHide: true,
    stdio: ['ignore', stdout, stderr],
    env: { ...process.env, CONNECT_FACTORY_SESSION_CODE: controlCode },
  });
  child.unref();
  await writeFile(stateFile, JSON.stringify({
    pid: child.pid,
    controlCode,
    startedAt: new Date().toISOString(),
  }), { encoding: 'utf8', mode: 0o600 });

  const deadline = Date.now() + 10_000;
  while (Date.now() < deadline) {
    if (await readHealth()) {
      return { state: 'PAIRING_REQUIRED', paired: false, controlCode, pairingCode: controlCode };
    }
    await new Promise((resolve) => setTimeout(resolve, 250));
  }
  throw new Error('A fábrica local não iniciou em 127.0.0.1:4317. Consulte o log sanitizado em .runtime/connect-agent-factory.');
}

async function adopt() {
  const controlCode = process.env.CONNECT_FACTORY_SESSION_CODE;
  const pid = Number(process.env.CONNECT_FACTORY_SESSION_PID);
  if (!controlCode || !Number.isInteger(pid) || !processExists(pid) || !(await readHealth())) {
    throw new Error('Não foi possível adotar a fábrica local informada.');
  }
  await mkdir(runtimeDir, { recursive: true });
  await writeFile(stateFile, JSON.stringify({
    pid,
    controlCode,
    startedAt: new Date().toISOString(),
  }), { encoding: 'utf8', mode: 0o600 });
  return { state: 'ADOPTED', paired: true };
}

async function serve() {
  const controlCode = process.env.CONNECT_FACTORY_SESSION_CODE;
  if (!controlCode) throw new Error('Código local ausente para iniciar a fábrica.');
  const { createFactoryServer } = await import(pathToFileURL(serverFile).href);
  const factory = createFactoryServer({
    pairingCode: controlCode,
    controlCode,
    auditFile: path.join(runtimeDir, 'audit.jsonl'),
  });
  await factory.listen({ port: 4317 });
  const close = async () => {
    await factory.close();
    process.exit(0);
  };
  process.on('SIGINT', close);
  process.on('SIGTERM', close);
}

if (command === 'serve') {
  await serve();
} else if (command === 'start') {
  console.log(JSON.stringify(await start()));
} else if (command === 'status') {
  console.log(JSON.stringify(await status()));
} else if (command === 'adopt') {
  console.log(JSON.stringify(await adopt()));
} else {
  throw new Error('Comando inválido. Use status, start ou adopt.');
}
