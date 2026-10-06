param(
    [string]$Root = "C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2"
)

$ErrorActionPreference = "Stop"
$game = "C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas"
$outDir = Join-Path $Root "build\workflow"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

function File-State([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) {
        return [ordered]@{ path=$Path; exists=$false; bytes=$null; sha256=$null; modified=$null }
    }
    $i = Get-Item -LiteralPath $Path
    return [ordered]@{
        path=$Path
        exists=$true
        bytes=$i.Length
        sha256=(Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
        modified=$i.LastWriteTime.ToString("o")
    }
}

$protected = [ordered]@{
    active_source = File-State (Join-Path $Root "third_party\NVSE-6.4.9\fnv_gmod_thug2_plugin\main.cpp")
    installed_dll = File-State (Join-Path $game "Data\NVSE\Plugins\FNVGModTHUG2.dll")
    active_esp = File-State (Join-Path $game "Data\REM_GModTHUG2.esp")
    astra_v88 = File-State (Join-Path $Root "build\hud88\bin\FNVGModTHUG2.dll")
}

$handoffText = & (Join-Path $Root "research\validate_gpt6_opus_handoff.ps1") 2>&1 | Out-String
$supportText = & python -u (Join-Path $Root "research\validate_support_lane_state.py") 2>&1 | Out-String

$readyPath = Join-Path $Root "build\handoffs\gpt6_opus\runtime_harness\READY_VERDICT.json"
$preflightPath = Join-Path $Root "build\handoffs\gpt6_opus\PREFLIGHT_RESULT.json"
$supportPath = Join-Path $Root "build\validation\support_lane_state.json"

$ready = if(Test-Path $readyPath){ Get-Content $readyPath -Raw | ConvertFrom-Json } else { $null }
$preflight = if(Test-Path $preflightPath){ Get-Content $preflightPath -Raw | ConvertFrom-Json } else { $null }
$support = if(Test-Path $supportPath){ Get-Content $supportPath -Raw | ConvertFrom-Json } else { $null }

$processes = @()
Get-Process FalloutNV,FNVScript,xFOEdit -ErrorAction SilentlyContinue | ForEach-Object {
    $processes += [ordered]@{ name=$_.ProcessName; id=$_.Id; start_time=$_.StartTime.ToString("o") }
}

$result = [ordered]@{
    schema = "rem.workflow_checkpoint.v1"
    generated_local = (Get-Date).ToString("o")
    protected = $protected
    handoff = [ordered]@{
        ready_for_implementation = if($ready){$ready.READY_FOR_IMPLEMENTATION}else{$null}
        source_drift = if($ready){$ready.source_drift}else{$null}
        preflight_pass = if($preflight){$preflight.pass}else{$null}
        prop_count = if($preflight){$preflight.prop_count}else{$null}
        semantic_overlap = if($preflight){$preflight.semantic_overlap}else{$null}
        missing_level_glbs = if($preflight){@($preflight.missing_level_glbs)}else{@()}
        ida68_missing = if($preflight){@($preflight.ida68_missing)}else{@()}
        known_physgun_asset_gaps = if($preflight){@($preflight.known_physgun_asset_gaps)}else{@()}
    }
    support_validator = [ordered]@{
        status = if($support){$support.status}else{$null}
        checks = if($support){@($support.checks).Count}else{0}
        error_count = if($support){$support.error_count}else{$null}
    }
    active_processes = $processes
    implementation_preflight_ready = (
        $ready -and $ready.READY_FOR_IMPLEMENTATION -eq "YES" -and
        $preflight -and $preflight.pass -eq $true -and
        $support -and $support.status -eq "pass" -and
        @($support.checks | Where-Object { $_.severity -eq "error" -and -not $_.pass }).Count -eq 0
    )
    notes = @(
        "This checkpoint is workflow evidence only; it does not prove gameplay stability or satisfy human promotion gates.",
        "No deployment or runtime file mutation is performed by this script.",
        "Re-run before each Astra/Opus implementation or promotion pass because concurrent sessions may change state."
    )
}

$json = $result | ConvertTo-Json -Depth 8
$json | Set-Content -LiteralPath (Join-Path $outDir "CURRENT_CHECKPOINT.json") -Encoding UTF8
$json