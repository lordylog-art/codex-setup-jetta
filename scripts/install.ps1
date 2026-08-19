[CmdletBinding()]
param(
    [string]$JettaPath = 'C:\Projetos\Jeta Move',
    [switch]$InstallRtk
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$codexHome = Join-Path $env:USERPROFILE '.codex'
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backup = Join-Path $env:USERPROFILE ".codex-backup\\$stamp"

New-Item -ItemType Directory -Force -Path $codexHome, $backup, (Join-Path $codexHome 'skills'), (Join-Path $codexHome 'references') | Out-Null
foreach ($name in 'AGENTS.md', 'RTK.md') {
    $target = Join-Path $codexHome $name
    if (Test-Path $target) { Copy-Item -LiteralPath $target -Destination $backup -Force }
    Copy-Item -LiteralPath (Join-Path $root "global\\$name") -Destination $target -Force
}
Copy-Item -Path (Join-Path $root 'global\skills\*') -Destination (Join-Path $codexHome 'skills') -Recurse -Force
Copy-Item -Path (Join-Path $root 'global\references\*') -Destination (Join-Path $codexHome 'references') -Recurse -Force

if (Test-Path $JettaPath) {
    Copy-Item -LiteralPath (Join-Path $root 'jetta\\AGENTS.md') -Destination (Join-Path $JettaPath 'AGENTS.md') -Force
    Copy-Item -LiteralPath (Join-Path $root 'jetta\\.agents') -Destination $JettaPath -Recurse -Force
    Copy-Item -LiteralPath (Join-Path $root 'jetta\\.specify') -Destination $JettaPath -Recurse -Force
} else {
    Write-Warning "ERP Jetta não encontrado em $JettaPath. A configuração global foi instalada; execute novamente com -JettaPath após clonar o projeto."
}

if ($InstallRtk) { & (Join-Path $PSScriptRoot 'install-rtk.ps1') }
Write-Host "Configuração aplicada. Backup global: $backup"
