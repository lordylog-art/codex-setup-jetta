$ErrorActionPreference = 'Stop'

$projectRoot = 'C:\Scripts\ERP JETTA'
$deployScript = Join-Path $projectRoot 'deploy.ps1'
$webhooksScript = Join-Path $projectRoot 'deploy-webhooks.ps1'

function Invoke-DeployStep {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Label,

        [Parameter(Mandatory = $true)]
        [scriptblock] $Command
    )

    Write-Host ""
    Write-Host "==> $Label"
    & $Command
    $exitCode = $LASTEXITCODE

    if ($null -eq $exitCode) {
        $exitCode = 0
    }

    if ($exitCode -ne 0) {
        throw "$Label falhou com exit code $exitCode."
    }
}

if (-not (Test-Path -LiteralPath $projectRoot -PathType Container)) {
    throw "Diretorio do projeto nao encontrado: $projectRoot"
}

if (-not (Test-Path -LiteralPath $deployScript -PathType Leaf)) {
    throw "Script nao encontrado: $deployScript"
}

if (-not (Test-Path -LiteralPath $webhooksScript -PathType Leaf)) {
    throw "Script nao encontrado: $webhooksScript"
}

Push-Location -LiteralPath $projectRoot
try {
    Invoke-DeployStep -Label 'git pull' -Command {
        & git pull
    }

    Invoke-DeployStep -Label 'deploy.ps1 -AllowDirectProductionDeploy' -Command {
        & '.\deploy.ps1' -AllowDirectProductionDeploy
    }

    Invoke-DeployStep -Label 'deploy-webhooks.ps1' -Command {
        & '.\deploy-webhooks.ps1'
    }

    Write-Host ""
    Write-Host "DEPLOY_VPS_RESULT=OK"
}
finally {
    Pop-Location
}
