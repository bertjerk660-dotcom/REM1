param(
  [Parameter(Mandatory=$true)][string]$SessionDir
)
$ErrorActionPreference="Stop"
$Project="C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2"
$Game="C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas"
$Data=Join-Path $Game "Data"
$Pre=Get-Content -Raw -LiteralPath (Join-Path $SessionDir "preflight.json") | ConvertFrom-Json
$Start=[datetime]::Parse($Pre.preflight_local_time)
$Now=Get-Date

$Files=[ordered]@{
  live_plugin = Join-Path $Data "NVSE\Plugins\FNVGModTHUG2.dll"
  active_esp = Join-Path $Data "REM_GModTHUG2.esp"
  astra_v88 = Join-Path $Project "build\hud88\bin\FNVGModTHUG2.dll"
  combine_sidecar = Join-Path $Data "REM_CombineArmor_Test.esp"
  prop_sidecar = Join-Path $Data "REM_GModProps_Catalog.esp"
  presentation_sidecar = Join-Path $Data "REM_WeaponPresentation_Fixes.esp"
}
$Hashes=[ordered]@{}
foreach($k in $Files.Keys){
  $p=$Files[$k]
  $Hashes[$k]=if(Test-Path -LiteralPath $p){(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash}else{$null}
}

$Events=@(Get-WinEvent -FilterHashtable @{LogName='Application';StartTime=$Start} -ErrorAction SilentlyContinue |
 Where-Object {$_.Message -match 'FalloutNV|FNVGModTHUG2'} |
 Select-Object TimeCreated,Id,ProviderName,Message)
$Events | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $SessionDir "events_postflight.json") -Encoding UTF8

$Log=Join-Path $Game "FNVGModTHUG2.log"
if(Test-Path $Log){ Copy-Item -LiteralPath $Log -Destination (Join-Path $SessionDir "FNVGModTHUG2_postflight.log") -Force }

$HashChanges=[ordered]@{}
foreach($k in $Hashes.Keys){
  $before=$Pre.hashes.$k
  $after=$Hashes[$k]
  $HashChanges[$k]=[ordered]@{before=$before;after=$after;changed=($before -ne $after)}
}

$Post=[ordered]@{
  session_dir=$SessionDir
  postflight_local_time=$Now.ToString("o")
  elapsed_seconds=[math]::Round(($Now-$Start).TotalSeconds,2)
  hashes=$Hashes
  hash_changes=$HashChanges
  relevant_application_events=$Events.Count
  fallout_running_after=[bool](Get-Process FalloutNV -ErrorAction SilentlyContinue)
  note="Evidence capture only. Human gameplay observations must be added separately."
}
$Post | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $SessionDir "postflight.json") -Encoding UTF8
$Post | ConvertTo-Json -Depth 6