[CmdletBinding()]
param([string]$VaultPath)

$ErrorActionPreference = 'Stop'
$pluginId = 'obsidian-local-rest-api'
$codexHome = Join-Path $env:USERPROFILE '.codex'
$obsidianExe = Join-Path $env:LOCALAPPDATA 'Programs\Obsidian\Obsidian.exe'
$obsidianCli = Join-Path $env:LOCALAPPDATA 'Programs\Obsidian\Obsidian.com'

if (-not (Test-Path -LiteralPath $obsidianCli)) {
    winget install --id Obsidian.Obsidian --exact --source winget --accept-package-agreements --accept-source-agreements --silent | Out-Null
}
if (-not (Test-Path -LiteralPath $obsidianCli)) { throw 'Obsidian CLI não foi instalada.' }
if (-not (Get-Process Obsidian -ErrorAction SilentlyContinue)) {
    Start-Process -FilePath $obsidianExe -WindowStyle Hidden
    Start-Sleep -Seconds 3
}

$versionOutput = & $obsidianCli version 2>&1
if ($LASTEXITCODE -ne 0) {
    throw "Habilite Settings > General > Advanced > Command line interface no Obsidian e execute novamente. $versionOutput"
}
$versionText = [string]$versionOutput
if ($versionText -notmatch '^([0-9]+\.[0-9]+\.[0-9]+)') { throw "Versão da CLI desconhecida: $versionText" }
if ([version]$Matches[1] -lt [version]'1.12.7') { throw "Atualize o instalador do Obsidian para 1.12.7 ou superior: $versionText" }

$knownVaults = @(& $obsidianCli vaults verbose)
if ($LASTEXITCODE -ne 0) { throw 'Falha ao listar vaults pelo Obsidian.' }
if ($VaultPath) {
    $VaultPath = (Resolve-Path -LiteralPath $VaultPath).Path
} else {
    $paths = @($knownVaults | ForEach-Object { ($_ -split "`t", 2)[-1] } | Where-Object { Test-Path -LiteralPath (Join-Path $_ '.obsidian') })
    if ($paths.Count -ne 1) { throw 'Informe -VaultPath de um vault existente; nenhum ou vários vaults foram encontrados.' }
    $VaultPath = $paths[0]
}
if (-not (Test-Path -LiteralPath (Join-Path $VaultPath '.obsidian'))) { throw "Não é um vault existente: $VaultPath" }
$vaultName = Split-Path -Leaf $VaultPath
if (-not ($knownVaults | Where-Object { ($_ -split "`t", 2)[-1] -eq $VaultPath })) {
    throw "Abra o vault existente no Obsidian e execute novamente: $VaultPath"
}

$pluginFolder = Join-Path $VaultPath ".obsidian\plugins\$pluginId"
if (-not (Test-Path -LiteralPath (Join-Path $pluginFolder 'manifest.json'))) {
    & $obsidianCli "vault=$vaultName" plugin:install "id=$pluginId" enable | Out-Null
} else {
    & $obsidianCli "vault=$vaultName" plugin:enable "id=$pluginId" | Out-Null
}
if ($LASTEXITCODE -ne 0) { throw "Falha ao habilitar $pluginId." }
$pluginDataPath = Join-Path $pluginFolder 'data.json'
if (-not (Test-Path -LiteralPath $pluginDataPath)) {
    throw 'Permita plugins da comunidade em Settings > Community plugins e execute novamente.'
}
$gitRoot = & git -C $VaultPath rev-parse --show-toplevel 2>$null
if ($LASTEXITCODE -eq 0 -and $gitRoot) {
    $relativePlugin = [IO.Path]::GetRelativePath($gitRoot, $pluginFolder).Replace('\', '/')
    $tracked = & git -C $gitRoot ls-files --error-unmatch -- "$relativePlugin/data.json" 2>$null
    if ($LASTEXITCODE -eq 0) { throw "Configuração com chave já versionada em Git: $tracked" }
    $excludePath = & git -C $gitRoot rev-parse --git-path info/exclude
    if (-not [IO.Path]::IsPathRooted($excludePath)) { $excludePath = Join-Path $gitRoot $excludePath }
    $excludeLines = @("/$relativePlugin/", "/$([IO.Path]::GetRelativePath($gitRoot, (Join-Path $VaultPath '.obsidian\community-plugins.json')).Replace('\', '/'))")
    $existingExcludes = if (Test-Path -LiteralPath $excludePath) { @(Get-Content -LiteralPath $excludePath) } else { @() }
    foreach ($line in $excludeLines) {
        if ($existingExcludes -notcontains $line) { Add-Content -LiteralPath $excludePath -Value $line }
    }
}
$pluginData = Get-Content -LiteralPath $pluginDataPath -Raw | ConvertFrom-Json
if (-not $pluginData.apiKey) { throw 'A chave do plugin ainda não foi gerada.' }
$securePort = [int]$pluginData.port
$insecurePort = [int]$pluginData.insecurePort
$env:OBSIDIAN_API_KEY = [string]$pluginData.apiKey
[Environment]::SetEnvironmentVariable('OBSIDIAN_API_KEY', $env:OBSIDIAN_API_KEY, 'User')
$auth = @{ Authorization = "Bearer $env:OBSIDIAN_API_KEY" }

$endpoint = $null
try {
    $status = Invoke-RestMethod -Uri "https://127.0.0.1:$securePort/" -Headers $auth -TimeoutSec 5
    if ($status.authenticated) { $endpoint = "https://127.0.0.1:$securePort/mcp/" }
} catch { }
if (-not $endpoint) {
    if (-not $pluginData.enableInsecureServer) {
        $backupDir = Join-Path $env:USERPROFILE '.codex-backup'
        New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
        $backup = Join-Path $backupDir "obsidian-plugin-data-$(Get-Date -Format 'yyyyMMdd-HHmmss').json"
        Copy-Item -LiteralPath $pluginDataPath -Destination $backup
        $pluginData.enableInsecureServer = $true
        $pluginData | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $pluginDataPath -Encoding utf8
        & $obsidianCli "vault=$vaultName" plugin:disable "id=$pluginId" | Out-Null
        & $obsidianCli "vault=$vaultName" plugin:enable "id=$pluginId" | Out-Null
    }
    $status = Invoke-RestMethod -Uri "http://127.0.0.1:$insecurePort/" -Headers $auth -TimeoutSec 10
    if (-not $status.authenticated) { throw 'Servidor HTTP do Obsidian não autenticou.' }
    $endpoint = "http://127.0.0.1:$insecurePort/mcp/"
}
$port = if ($endpoint.StartsWith('https:')) { $securePort } else { $insecurePort }
$listeners = @(Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction Stop)
if (-not $listeners -or @($listeners | Where-Object { $_.LocalAddress -notin @('127.0.0.1', '::1') }).Count) {
    throw "Porta $port não está limitada ao loopback."
}
$discover = @{
    jsonrpc = '2.0'; id = 1; method = 'server/discover'
    params = @{ _meta = @{
        'io.modelcontextprotocol/protocolVersion' = '2026-07-28'
        'io.modelcontextprotocol/clientInfo' = @{ name = 'codex-setup-jetta'; version = '1.0.0' }
        'io.modelcontextprotocol/clientCapabilities' = @{}
    } }
} | ConvertTo-Json -Depth 8 -Compress
$mcpHeaders = $auth.Clone()
$mcpHeaders['MCP-Protocol-Version'] = '2026-07-28'
$mcpHeaders['Mcp-Method'] = 'server/discover'
$mcpHeaders['Accept'] = 'application/json'
$discovered = Invoke-RestMethod -Uri $endpoint -Method Post -Headers $mcpHeaders -ContentType 'application/json' -Body $discover -TimeoutSec 10
if (-not $discovered.result) { throw 'Endpoint MCP não respondeu ao server/discover.' }

New-Item -ItemType Directory -Path $codexHome -Force | Out-Null
$configPath = Join-Path $codexHome 'config.toml'
$config = if (Test-Path -LiteralPath $configPath) { Get-Content -LiteralPath $configPath -Raw } else { '' }
$existingBlock = [regex]::Match($config, '(?ms)^\[mcp_servers\.obsidian\]\s*$.*?(?=^\[|\z)').Value
if ($existingBlock) {
    if ($existingBlock -notmatch [regex]::Escape("url = `"$endpoint`"") -or $existingBlock -notmatch 'bearer_token_env_var = "OBSIDIAN_API_KEY"') {
        throw 'Bloco MCP obsidian existente difere do endpoint validado; revise sem sobrescrever outras opções.'
    }
} else {
    if (Test-Path -LiteralPath $configPath) { Copy-Item -LiteralPath $configPath -Destination "$configPath.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')" }
    $block = "`r`n[mcp_servers.obsidian]`r`nurl = `"$endpoint`"`r`nbearer_token_env_var = `"OBSIDIAN_API_KEY`"`r`nrequired = false`r`n"
    $codexVersion = & codex --version
    if ($codexVersion -match '([0-9]+\.[0-9]+\.[0-9]+)' -and [version]$Matches[1] -ge [version]'0.149.1') {
        $block += "default_tools_approval_mode = `"approve`"`r`n"
    }
    [IO.File]::AppendAllText($configPath, $block, [Text.UTF8Encoding]::new($false))
}

$sourceAgents = Get-Content -LiteralPath (Join-Path (Split-Path -Parent $PSScriptRoot) 'global\AGENTS.md') -Raw
$section = [regex]::Match($sourceAgents, '(?ms)^## Obsidian\s*$.*\z').Value
if (-not $section) { throw 'Seção Obsidian ausente em global/AGENTS.md.' }
$agentsPath = Join-Path $codexHome 'AGENTS.md'
$agents = if (Test-Path -LiteralPath $agentsPath) { Get-Content -LiteralPath $agentsPath -Raw } else { '' }
if ($agents -notmatch '(?m)^## Obsidian\s*$') {
    if (Test-Path -LiteralPath $agentsPath) { Copy-Item -LiteralPath $agentsPath -Destination "$agentsPath.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')" }
    [IO.File]::AppendAllText($agentsPath, "`r`n$section", [Text.UTF8Encoding]::new($false))
}

$servers = & codex mcp list 2>&1
if ($LASTEXITCODE -ne 0 -or -not ($servers -match '(?m)^obsidian\s+')) { throw 'Codex não reconheceu o MCP obsidian.' }
Write-Host "Obsidian $versionText; vault=$VaultPath; MCP=$endpoint; autenticação e loopback validados."
