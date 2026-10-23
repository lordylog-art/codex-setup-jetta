import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync, renameSync, mkdirSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join } from 'node:path';
import { randomUUID } from 'node:crypto';

export const sessionFile = process.env.CONNECT_SESSION_FILE || join(homedir(), '.codex', 'connect-channels-session.dpapi');
const assembly = "[void][Reflection.Assembly]::LoadWithPartialName('System.Security'); ";
function dpapi(input, decrypt = false) {
  assert(process.platform === 'win32', 'Saved Connect sessions require Windows DPAPI');
  const script = decrypt
    ? "$bytes = [Convert]::FromBase64String([Console]::In.ReadToEnd()); [Console]::Out.Write([Text.Encoding]::UTF8.GetString([Security.Cryptography.ProtectedData]::Unprotect($bytes,$null,[Security.Cryptography.DataProtectionScope]::CurrentUser)))"
    : "$bytes = [Text.Encoding]::UTF8.GetBytes([Console]::In.ReadToEnd()); [Console]::Out.Write([Convert]::ToBase64String([Security.Cryptography.ProtectedData]::Protect($bytes,$null,[Security.Cryptography.DataProtectionScope]::CurrentUser)))";
  const result = spawnSync(join(process.env.SystemRoot || 'C:/Windows', 'System32', 'WindowsPowerShell', 'v1.0', 'powershell.exe'), ['-NoProfile', '-NonInteractive', '-Command', assembly + script], {
    input, encoding: 'utf8', windowsHide: true, timeout: 10000,
  });
  assert(result.status === 0 && result.stdout, 'Windows could not protect/read this user session');
  return result.stdout;
}
export function readSession(path = sessionFile) {
  let encrypted;
  try { encrypted = readFileSync(path, 'utf8'); }
  catch (error) { if (error.code === 'ENOENT') return null; throw Error('Cannot read Connect session file'); }
  return JSON.parse(dpapi(encrypted, true));
}
export function writeSession(session, path = sessionFile) {
  const encrypted = dpapi(JSON.stringify(session));
  mkdirSync(dirname(path), { recursive: true });
  const temp = `${path}.${randomUUID()}.tmp`;
  writeFileSync(temp, encrypted, { flag: 'wx', mode: 0o600 });
  renameSync(temp, path);
}
