param(
  [string]$Label = "support-test",
  [switch]$ArchivePluginLog
)

$ErrorActionPreference = "Stop"
$Project = "C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2"
$Game = "C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas"
$Data = Join-Path $Game "Data"
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$SafeLabel = ($Label -replace '[^A-Za-z0-9_.-]','_')
$Session = Join-Path $Project ("build\playtests\" + $Stamp + "_" + $SafeLabel)
New-Item -ItemType Directory -Force -Path $Session | Out-Null

$Files = [ordered]@{
  live_plugin = Join-Path $Data "NVSE\Plugins\FNVGModTHUG2.dll"
  active_esp = Join-Path $Data "REM_GModTHUG2.esp"
  astra_v88 = Join-Path $Project "build\hud88\bin\FNVGModTHUG2.dll"
  combine_sidecar = Join-Path $Data "REM_CombineArmor_Test.esp"
  prop_sidecar = Join-Path $Data "REM_GModProps_Catalog.esp"
  presentation_sidecar = Join-Path $Data "REM_WeaponPresentation_Fixes.esp"
}
$Hashes = [ordered]@{}
foreach($k in $Files.Keys){
  $p=$Files[$k]
  $Hashes[$k] = if(Test-Path -LiteralPath $p){ (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash } else { $null }
}

$PluginsPath = "C:\Users\BRAD\AppData\Local\FalloutNV\plugins.txt"
$PluginLines = if(Test-Path $PluginsPath){ Get-Content -LiteralPath $PluginsPath } else { @() }
$SidecarEnabled = [ordered]@{}
foreach($name in @("REM_CombineArmor_Test.esp","REM_GModProps_Catalog.esp","REM_WeaponPresentation_Fixes.esp")){
  $SidecarEnabled[$name] = [bool]($PluginLines | Where-Object { $_.Trim().TrimStart('*') -ieq $name })
}

$Running = @(Get-Process FalloutNV -ErrorAction SilentlyContinue | ForEach-Object {
  [pscustomobject]@{ Id=$_.Id; StartTime=$_.StartTime.ToString("o"); Path=$_.Path }
})
$Now = Get-Date
$Events = @(Get-WinEvent -FilterHashtable @{LogName='Application';StartTime=$Now.AddMinutes(-30)} -ErrorAction SilentlyContinue |
  Where-Object {$_.Message -match 'FalloutNV|FNVGModTHUG2'} |
  Select-Object -First 50 TimeCreated,Id,ProviderName,Message)
$Events | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $Session "events_preflight.json") -Encoding UTF8

$PluginLog = Join-Path $Game "FNVGModTHUG2.log"
if(Test-Path $PluginLog){
  Copy-Item -LiteralPath $PluginLog -Destination (Join-Path $Session "FNVGModTHUG2_preflight.log") -Force
  if($ArchivePluginLog){
    Copy-Item -LiteralPath $PluginLog -Destination (Join-Path $Session "FNVGModTHUG2_archived_before_test.log") -Force
  }
}

$Manifest=[ordered]@{
  session_dir=$Session
  label=$Label
  preflight_local_time=$Now.ToString("o")
  preflight_utc=$Now.ToUniversalTime().ToString("o")
  hashes=$Hashes
  sidecars_enabled=$SidecarEnabled
  fallout_running=$Running
  plugins_path=$PluginsPath
  note="Capture only. Does not launch Fallout, enable plugins, alter saves, or deploy Astra v88."
}
$Manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $Session "preflight.json") -Encoding UTF8
Write-Output $Session