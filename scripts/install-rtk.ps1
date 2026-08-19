$ErrorActionPreference = 'Stop'
$release = Invoke-RestMethod 'https://api.github.com/repos/rtk-ai/rtk/releases/latest'
$asset = $release.assets | Where-Object { $_.name -eq 'rtk-x86_64-pc-windows-msvc.zip' }
$checksums = $release.assets | Where-Object { $_.name -eq 'checksums.txt' }
if ($null -eq $asset -or $null -eq $checksums) { throw 'Release Windows do RTK não encontrada.' }

$temp = Join-Path $env:TEMP ('rtk-' + [guid]::NewGuid())
$zip = Join-Path $temp $asset.name
$sum = Join-Path $temp $checksums.name
$out = Join-Path $env:USERPROFILE '.local\\bin'
New-Item -ItemType Directory -Force -Path $temp, $out | Out-Null
try {
    Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $zip
    Invoke-WebRequest -Uri $checksums.browser_download_url -OutFile $sum
    $line = Get-Content $sum | Where-Object { $_ -match [regex]::Escape($asset.name) } | Select-Object -First 1
    $expected = ($line -split '\\s+')[0].ToLowerInvariant()
    $actual = (Get-FileHash -Algorithm SHA256 $zip).Hash.ToLowerInvariant()
    if ($actual -ne $expected) { throw 'Checksum do RTK inválido.' }
    $extract = Join-Path $temp 'extract'
    Expand-Archive -LiteralPath $zip -DestinationPath $extract
    $binary = Get-ChildItem -Path $extract -Filter rtk.exe -Recurse | Select-Object -First 1
    if ($null -eq $binary) { throw 'rtk.exe ausente no pacote oficial.' }
    Copy-Item -LiteralPath $binary.FullName -Destination (Join-Path $out 'rtk.exe') -Force
    $userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
    if (($userPath -split ';') -notcontains $out) { [Environment]::SetEnvironmentVariable('Path', "$userPath;$out", 'User') }
    & (Join-Path $out 'rtk.exe') init -g --codex
    & (Join-Path $out 'rtk.exe') --version
} finally {
    Remove-Item -LiteralPath $temp -Recurse -Force -ErrorAction SilentlyContinue
}
