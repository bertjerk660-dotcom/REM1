# REM1 Bevy: build + scripted autotest + build manifest, in one reproducible step.
# Usage (from anywhere):
#   powershell -ExecutionPolicy Bypass -File bevy\tools\autotest.ps1 -BuildId B001 -Parent none
# Writes: <OutRoot>\<BuildId>\{autotest_report.json, screenshots, saves, logs}
#         bevy\builds\<BuildId>.json  (manifest: toolchain, git, input/output hashes, checks)
# Exit code 0 only if the build succeeds AND every autotest check passes.
param(
  [Parameter(Mandatory = $true)][string]$BuildId,
  [string]$Parent = 'none',
  [string]$Goal = '',
  [string]$OutRoot = 'D:\rem1_bevy_runs',
  # Keep the cargo target dir OFF the system drive: a full debug Bevy build exhausted C: (F-B002).
  [string]$TargetDir = 'D:\rem1_bevy_target_chat',
  [int]$TimeoutSec = 180
)
$ErrorActionPreference = 'Continue'
$bevy = Split-Path $PSScriptRoot -Parent
$repo = Split-Path $bevy -Parent
$env:PATH = "$env:USERPROFILE\.cargo\bin;" + $env:PATH
$env:CARGO_TARGET_DIR = $TargetDir
$out = Join-Path $OutRoot $BuildId
New-Item -ItemType Directory -Force $out | Out-Null

Push-Location $bevy
$t0 = Get-Date
cargo build 2>&1 | ForEach-Object { "$_" } | Out-File "$out\build.log" -Encoding utf8
$buildOk = ($LASTEXITCODE -eq 0)
$buildSec = [math]::Round(((Get-Date) - $t0).TotalSeconds, 1)
Pop-Location

$exe = Join-Path $TargetDir 'debug\rem1.exe'
$runExit = $null
if ($buildOk) {
  $env:RUST_LOG = 'warn,rem1=info'
  $p = Start-Process $exe -ArgumentList '--autotest', '--out', $out -WorkingDirectory $bevy `
    -RedirectStandardOutput "$out\stdout.txt" -RedirectStandardError "$out\stderr.txt" -PassThru
  $null = $p.Handle  # cache the handle so ExitCode is available after exit
  if (-not $p.WaitForExit($TimeoutSec * 1000)) { $p.Kill(); $runExit = 'timeout' } else { $runExit = $p.ExitCode }
}

# NB: do not name this 'H' - PowerShell resolves the built-in alias h (Get-History) first.
function Get-Sha([string]$path) { if (Test-Path $path) { (Get-FileHash $path -Algorithm SHA256).Hash } else { $null } }
Set-Alias -Name H -Value Get-Sha -Scope Script -Force -Option AllScope
$inputs = [ordered]@{}
foreach ($f in @('Cargo.toml', 'Cargo.lock') + (Get-ChildItem "$bevy\src" -Filter *.rs | Sort-Object Name | ForEach-Object { "src/" + $_.Name })) {
  $inputs[$f] = H (Join-Path $bevy $f)
}
$report = $null
if (Test-Path "$out\autotest_report.json") { $report = Get-Content "$out\autotest_report.json" -Raw | ConvertFrom-Json }
$allPass = $false
if ($report -ne $null -and $report.all_pass -eq $true) { $allPass = $true }
$shots = [ordered]@{}
Get-ChildItem $out -Filter *.png -EA SilentlyContinue | ForEach-Object { $shots[$_.Name] = H $_.FullName }

$manifest = [ordered]@{
  schema          = 'rem1-bevy-build-manifest/1'
  build_id        = $BuildId
  parent_build    = $Parent
  goal            = $Goal
  created         = (Get-Date).ToString('o')
  git             = [ordered]@{
    branch       = (git -C $repo rev-parse --abbrev-ref HEAD)
    head_at_run  = (git -C $repo rev-parse HEAD)
    dirty_paths  = @(git -C $repo status --porcelain -- bevy | ForEach-Object { $_.Trim() })
    note         = 'head_at_run is the parent commit when the run precedes its own commit; input hashes identify the exact tree tested.'
  }
  toolchain       = [ordered]@{ rustc = (rustc -V); cargo = (cargo -V); profile = 'dev'; target_dir = $TargetDir }
  engine          = [ordered]@{ bevy = '0.20.0'; rapier3d = '0.36.0' }
  host            = [ordered]@{ machine = $env:COMPUTERNAME; os = (Get-CimInstance Win32_OperatingSystem).Caption; gpu = @((Get-CimInstance Win32_VideoController).Name) }
  inputs_sha256   = $inputs
  outputs_sha256  = [ordered]@{ 'rem1.exe' = (H $exe) }
  build           = [ordered]@{ ok = $buildOk; seconds = $buildSec; warnings = @(Select-String -Path "$out\build.log" -Pattern '^warning' | ForEach-Object { $_.Line }) }
  autotest        = [ordered]@{ process_exit = $runExit; all_pass = $allPass; checks = $(if ($report) { $report.checks } else { @() }); physics_steps = $(if ($report) { $report.physics_steps } else { $null }); gamepads_detected = $(if ($report) { $report.gamepads_detected } else { $null }); duration_s = $(if ($report) { $report.duration_s } else { $null }) }
  evidence_dir    = $out
  screenshots_sha256 = $shots
}
New-Item -ItemType Directory -Force "$bevy\builds" | Out-Null
$manifest | ConvertTo-Json -Depth 8 | Out-File "$bevy\builds\$BuildId.json" -Encoding utf8
"build_ok=$buildOk run_exit=$runExit all_pass=$allPass manifest=$bevy\builds\$BuildId.json"
if ($buildOk -and $allPass -and $runExit -eq 0) { exit 0 } else { exit 1 }
