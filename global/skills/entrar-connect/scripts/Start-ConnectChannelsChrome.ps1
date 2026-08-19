param(
  [int]$Port = 9222,
  [string]$Url = "https://app.connectchannels.com.br/chat2/sessions",
  [string]$ProfileDir = "C:\Users\Jetta\Documents\Codex\2026-06-19\consegue-usar-o-chrome-com-minha\work\chrome-connectchannels-profile"
)

$ErrorActionPreference = "Stop"

function Test-Cdp {
  param([int]$Port)
  try {
    $response = Invoke-WebRequest -UseBasicParsing "http://127.0.0.1:$Port/json/version" -TimeoutSec 2
    return $response.Content
  } catch {
    return $null
  }
}

$existing = Test-Cdp -Port $Port
if ($existing) {
  Write-Output $existing
  exit 0
}

$chromePaths = @(
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
  "$env:LocalAppData\Google\Chrome\Application\chrome.exe"
)

$chrome = $chromePaths | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $chrome) {
  throw "Chrome nao encontrado nos caminhos padrao."
}

New-Item -ItemType Directory -Force -Path $ProfileDir | Out-Null

$args = @(
  "--remote-debugging-port=$Port",
  "--remote-allow-origins=*",
  "--user-data-dir=$ProfileDir",
  "--no-first-run",
  "--no-default-browser-check",
  $Url
)

Start-Process -FilePath $chrome -ArgumentList $args -WindowStyle Normal
Start-Sleep -Seconds 2

$started = Test-Cdp -Port $Port
if (-not $started) {
  throw "Chrome abriu, mas o CDP nao respondeu em http://127.0.0.1:$Port."
}

Write-Output $started
