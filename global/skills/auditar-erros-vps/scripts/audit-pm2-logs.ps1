param(
  [Parameter(Mandatory = $true)]
  [string]$SinceIso,

  [string]$LogDir = "",

  [string[]]$ProcessNamePrefixes = @("jetta-api", "jetta-web", "jetta-webhooks"),

  [int]$MaxTailLinesPerFile = 80000
)

$ErrorActionPreference = "Stop"

function Convert-ToSaoPauloDate([string]$Value) {
  if ($Value.EndsWith("Z") -or $Value -match "[+-]\d{2}:\d{2}$") {
    return [datetimeoffset]::Parse($Value).DateTime
  }
  return [datetime]::Parse($Value, [Globalization.CultureInfo]::InvariantCulture)
}

function Remove-Ansi([string]$Value) {
  return $Value -replace "\x1b\[[0-9;]*m", ""
}

function Sanitize-Message([string]$Value) {
  $clean = Remove-Ansi $Value
  $clean = $clean -replace "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", "<uuid>"
  $clean = $clean -replace "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "<email>"
  $clean = $clean -replace "\b\d{8,}\b", "<num>"
  $clean = $clean -replace "C:\\Jetta ERP\\JETTA-MOVE(\\.deploy-releases\\[^\\]+)?", "<app>"
  $clean = $clean -replace "\s+", " "
  return $clean.Trim()
}

function Get-EventTimestamp([string]$Line) {
  $clean = Remove-Ansi $Line
  $match = [regex]::Match($clean, "(\d{2})/(\d{2})/(\d{4}),\s+(\d{1,2}):(\d{2}):(\d{2})\s+(AM|PM)")
  if (-not $match.Success) {
    return $null
  }

  $stamp = "{0}/{1}/{2} {3}:{4}:{5} {6}" -f @(
    $match.Groups[1].Value,
    $match.Groups[2].Value,
    $match.Groups[3].Value,
    $match.Groups[4].Value,
    $match.Groups[5].Value,
    $match.Groups[6].Value,
    $match.Groups[7].Value
  )
  return [datetime]::ParseExact($stamp, "MM/dd/yyyy h:mm:ss tt", [Globalization.CultureInfo]::InvariantCulture)
}

function Get-Unit([string]$Line) {
  $clean = Remove-Ansi $Line
  foreach ($unit in @("guarulhos", "sumare", "vespasiano")) {
    if ($clean -match "(?i)\b$unit\b") {
      return $unit
    }
  }
  if ($clean -match "3-coracoes") {
    return "3-coracoes"
  }
  return "nao-identificado"
}

function Classify-Event([string]$Line, [string]$FileName) {
  $clean = Remove-Ansi $Line
  $service = if ($FileName -match "webhooks") { "jetta-webhooks" } elseif ($FileName -match "web") { "jetta-web" } else { "jetta-api" }
  $unit = Get-Unit $clean

  if ($clean -match "PrismaClientKnownRequestError|Foreign key constraint violated|P20\d\d") {
    return @{
      category = "erro-real"
      nature = "bug-codigo-ou-dado"
      severity = "alta"
      title = "Prisma/RequestLog ou banco"
      service = $service
      unit = $unit
      impact = "Falha real em persistencia ou integridade de dados."
    }
  }

  if ($clean -match "RouteExpenseStatusSyncScheduler|status de custo extra") {
    return @{
      category = "job-operacional"
      nature = "sync-operacional"
      severity = "media"
      title = "Job de status de custo extra"
      service = $service
      unit = $unit
      impact = "Job recorrente falhou; pode atrasar status operacional."
    }
  }

  if ($clean -match "SacSyncScheduler|sync autom.+SAC") {
    return @{
      category = "job-operacional"
      nature = "sync-operacional"
      severity = "media"
      title = "Job de sync SAC"
      service = $service
      unit = $unit
      impact = "Job recorrente falhou; pode atrasar acompanhamento SAC."
    }
  }

  if ($clean -match "Google Sheets.*copyPaste|filtered out row") {
    return @{
      category = "erro-real"
      nature = "integracao-externa"
      severity = "alta"
      title = "Google Sheets copyPaste em linha filtrada"
      service = $service
      unit = $unit
      impact = "Escrita em planilha falhou; dado operacional pode ficar pendente."
    }
  }

  if ($clean -match "Google Sheets.*429|Quota exceeded") {
    return @{
      category = "job-operacional"
      nature = "integracao-externa"
      severity = "media"
      title = "Google Sheets quota"
      service = $service
      unit = $unit
      impact = "Limite externo atingido; retries podem atrasar sincronizacao."
    }
  }

  if ($clean -match "IncidentEmailSyncScheduler.*concluiu com falhas") {
    return @{
      category = "job-operacional"
      nature = "sync-operacional"
      severity = "media"
      title = "Job de e-mails de ocorrencias"
      service = $service
      unit = $unit
      impact = "Job terminou com falhas; ocorrencias por e-mail podem atrasar."
    }
  }

  if ($clean -match "IncidentMailboxService.*IMAP|Falha ass.ncrona no IMAP") {
    return @{
      category = "job-operacional"
      nature = "integracao-externa"
      severity = "media"
      title = "IMAP de ocorrencias instavel"
      service = $service
      unit = $unit
      impact = "Falha externa/intermitente no IMAP."
    }
  }

  if ($clean -match "Falha no envio SMTP|EmailQueueService.*(reagendado|falha|tempor)") {
    return @{
      category = "job-operacional"
      nature = "integracao-externa"
      severity = "media"
      title = "SMTP/fila de email instavel"
      service = $service
      unit = $unit
      impact = "Envio pode atrasar, mas a fila tenta retry."
    }
  }

  if ($clean -match "Connect Channels template API request failed|AvailabilityService.*Connect Channels") {
    return @{
      category = "job-operacional"
      nature = "integracao-externa"
      severity = "media"
      title = "Connect Channels disponibilidade instavel"
      service = $service
      unit = $unit
      impact = "Integracao externa falhou; pode cair para retry ou leitura alternativa."
    }
  }

  if ($clean -match "\sERROR\s|Exception|unhandled|fatal") {
    return @{
      category = "inconclusivo"
      nature = "erro-sem-taxonomia"
      severity = "media"
      title = "Erro sem taxonomia"
      service = $service
      unit = $unit
      impact = "Evento precisa de investigacao manual."
    }
  }

  if ($clean -match "\sWARN\s|Falha|failed|timeout|ECONNRESET|ETIMEDOUT|EENVELOPE|EMESSAGE|ESOCKET") {
    return @{
      category = "ruido-ou-warning"
      nature = "warning-operacional"
      severity = "baixa"
      title = "Warning operacional"
      service = $service
      unit = $unit
      impact = "Warning sem evidencia suficiente de erro real."
    }
  }

  return $null
}

function Get-Fingerprint([hashtable]$Classification, [string]$Line) {
  $message = ""
  if ($Classification.title -in @("Erro sem taxonomia", "Warning operacional")) {
    $message = Sanitize-Message $Line
    $message = $message -replace "\d{2}/\d{2}/\d{4},\s+\d{1,2}:\d{2}:\d{2}\s+(AM|PM)", "<ts>"
    $message = $message.ToLowerInvariant()
    $message = $message.Substring(0, [Math]::Min(180, $message.Length))
  }
  return "{0}|{1}|{2}|{3}|{4}|{5}" -f @(
    $Classification.category,
    $Classification.nature,
    $Classification.service,
    $Classification.unit,
    $Classification.title,
    $message
  )
}

$since = Convert-ToSaoPauloDate $SinceIso
if ([string]::IsNullOrWhiteSpace($LogDir)) {
  $LogDir = Join-Path $env:USERPROFILE ".pm2\logs"
}

$emptySummary = {
  param([string]$Reason)
  [ordered]@{
    remote_now = (Get-Date).ToString("o")
    since = $since.ToString("o")
    scanned_files = @()
    unique_groups = 0
    raw_events = 0
    by_category = [ordered]@{
      "erro-real" = 0
      "job-operacional" = 0
      "ruido-ou-warning" = 0
      "inconclusivo" = 0
    }
    groups = @()
    limitation = $Reason
  } | ConvertTo-Json -Depth 8
}

if (-not (Test-Path -LiteralPath $LogDir)) {
  & $emptySummary "Diretorio de logs nao encontrado: $LogDir"
  exit 0
}

$prefixPattern = "^(?:{0}).*(?:error|out).*\.log$" -f (($ProcessNamePrefixes | ForEach-Object { [regex]::Escape($_) }) -join "|")
$groups = [ordered]@{}
$scannedFiles = @()

Get-ChildItem -LiteralPath $LogDir -File |
  Where-Object { $_.Name -match $prefixPattern -and $_.LastWriteTime -ge $since.AddHours(-2) } |
  Sort-Object Name |
  ForEach-Object {
    $file = $_
    $scannedFiles += $file.Name
    Get-Content -LiteralPath $file.FullName -Tail $MaxTailLinesPerFile -ReadCount 1000 | ForEach-Object {
      foreach ($line in $_) {
        $eventAt = Get-EventTimestamp $line
        if ($null -eq $eventAt -or $eventAt -lt $since) {
          continue
        }

        $classification = Classify-Event $line $file.Name
        if ($null -eq $classification) {
          continue
        }

        $fingerprint = Get-Fingerprint $classification $line
        if (-not $groups.Contains($fingerprint)) {
          $groups[$fingerprint] = [ordered]@{
            fingerprint = $fingerprint
            title = $classification.title
            category = $classification.category
            nature = $classification.nature
            severity = $classification.severity
            service = $classification.service
            unit = $classification.unit
            impact = $classification.impact
            occurrences = 0
            first = $null
            last = $null
            files = @{}
            sample = Sanitize-Message $line
          }
        }

        $group = $groups[$fingerprint]
        $group.occurrences++
        if ($null -eq $group.first -or $eventAt -lt [datetime]$group.first) { $group.first = $eventAt.ToString("o") }
        if ($null -eq $group.last -or $eventAt -gt [datetime]$group.last) { $group.last = $eventAt.ToString("o") }
        if (-not $group.files.Contains($file.Name)) { $group.files[$file.Name] = 0 }
        $group.files[$file.Name]++
      }
    }
  }

$allGroups = @($groups.Values)
$rawEvents = 0
foreach ($item in $allGroups) {
  $rawEvents += [int]$item.occurrences
}
$summary = [ordered]@{
  remote_now = (Get-Date).ToString("o")
  since = $since.ToString("o")
  scanned_files = $scannedFiles
  max_tail_lines_per_file = $MaxTailLinesPerFile
  unique_groups = $allGroups.Count
  raw_events = $rawEvents
  by_category = [ordered]@{
    "erro-real" = @($allGroups | Where-Object { $_.category -eq "erro-real" }).Count
    "job-operacional" = @($allGroups | Where-Object { $_.category -eq "job-operacional" }).Count
    "ruido-ou-warning" = @($allGroups | Where-Object { $_.category -eq "ruido-ou-warning" }).Count
    "inconclusivo" = @($allGroups | Where-Object { $_.category -eq "inconclusivo" }).Count
  }
  groups = @($allGroups | Sort-Object @{ Expression = {
      switch ($_.severity) {
        "critica" { 0 }
        "alta" { 1 }
        "media" { 2 }
        "baixa" { 3 }
        default { 4 }
      }
    }}, @{ Expression = "occurrences"; Descending = $true })
}

$summary | ConvertTo-Json -Depth 8
