# Validate generated Opus visual feed bundle without deploying runtime
param([string]$Root = "C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
$ErrorActionPreference = "Stop"
$feedDir = Join-Path $Root "build\handoffs\gpt6_opus\feed_bundle"
$required = @(
  "OPUS_VISUAL_QUEUE.json",
  "CODE_CONTEXT.md",
  "ASSET_REFERENCE_INDEX.json",
  "OPUS_START_PROMPT.md",
  "HANDOFF_INDEX.json",
  "FEED_MANIFEST.json"
)
$missing = @($required | Where-Object { !(Test-Path (Join-Path $feedDir $_)) })
if($missing.Count -gt 0){ throw ("Missing feed files: " + ($missing -join ", ")) }

$feed = Get-Content (Join-Path $feedDir "FEED_MANIFEST.json") -Raw | ConvertFrom-Json
$queue = Get-Content (Join-Path $feedDir "OPUS_VISUAL_QUEUE.json") -Raw | ConvertFrom-Json
$assets = Get-Content (Join-Path $feedDir "ASSET_REFERENCE_INDEX.json") -Raw | ConvertFrom-Json
$source = Join-Path $Root "third_party\NVSE-6.4.9\fnv_gmod_thug2_plugin\main.cpp"
$sourceHash = (Get-FileHash $source -Algorithm SHA256).Hash
$sourcePass = ($sourceHash -eq $feed.source_hash)

$generated = @()
foreach($g in $feed.generated_files){
  $p = Join-Path $Root $g.path
  $exists = Test-Path $p
  $actual = if($exists){(Get-FileHash $p -Algorithm SHA256).Hash}else{"MISSING"}
  $generated += [ordered]@{path=$g.path;exists=$exists;expected=$g.sha256;actual=$actual;pass=($exists -and $actual -eq $g.sha256)}
}

$packetChecks = @()
foreach($packet in $assets.source_packets){
  foreach($part in $packet.required_model_components){
    $p=$part.local_source
    $exists=($p -and (Test-Path $p))
    $actual=if($exists){(Get-FileHash $p -Algorithm SHA256).Hash}else{"MISSING"}
    $packetChecks += [ordered]@{packet=$packet.id;relative=$part.relative;exists=$exists;expected=$part.sha256;actual=$actual;pass=($exists -and $actual -eq $part.sha256)}
  }
}

$dll = "C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data\NVSE\Plugins\FNVGModTHUG2.dll"
$esp = "C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data\REM_GModTHUG2.esp"
$baseline=[ordered]@{
  dll_actual=(Get-FileHash $dll -Algorithm SHA256).Hash
  dll_expected="BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41"
  esp_actual=(Get-FileHash $esp -Algorithm SHA256).Hash
  esp_expected="0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7"
}
$baseline.pass=($baseline.dll_actual -eq $baseline.dll_expected -and $baseline.esp_actual -eq $baseline.esp_expected)

$taskIds=@($queue.tasks | ForEach-Object {$_.id})
$queuePass=($taskIds.Count -eq 6 -and $taskIds[0] -eq "O01" -and $queue.reserved_for_astra.Count -ge 5)
$assetPolicyPass=($feed.proprietary_assets_embedded -eq $false)
$generatedPass=(@($generated | Where-Object {!$_.pass}).Count -eq 0)
$packetPass=(@($packetChecks | Where-Object {!$_.pass}).Count -eq 0)

$result=[ordered]@{
  generated=(Get-Date).ToString("s")
  mode="PREPARATION_ONLY"
  missing_feed_files=$missing
  source_hash=[ordered]@{actual=$sourceHash;expected=$feed.source_hash;pass=$sourcePass}
  generated_files_pass=$generatedPass
  generated_files=$generated
  required_source_components_pass=$packetPass
  required_source_components_checked=$packetChecks.Count
  required_source_component_failures=@($packetChecks | Where-Object {!$_.pass})
  protected_baseline=$baseline
  queue=[ordered]@{task_ids=$taskIds;pass=$queuePass;astra_reserved=$queue.reserved_for_astra}
  proprietary_assets_embedded=$feed.proprietary_assets_embedded
  asset_policy_pass=$assetPolicyPass
  pass=($missing.Count -eq 0 -and $sourcePass -and $generatedPass -and $packetPass -and $baseline.pass -and $queuePass -and $assetPolicyPass)
}
$result | ConvertTo-Json -Depth 8 | Set-Content (Join-Path $feedDir "VALIDATION_RESULT.json") -Encoding UTF8
$result | ConvertTo-Json -Depth 8
if(!$result.pass){ exit 2 }