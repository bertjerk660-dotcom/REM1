# GPT6/Opus handoff preflight
param([string]$Root = "C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
$ErrorActionPreference="Stop"
$required=@("AGENTS.md","context\BOOTSTRAP.md","context\GOAL.md","context\CURRENT_STATE.md","context\FAILURE_KNOWLEDGE.md","context\HANDOFFS\PHYSGUN_IDA68_EVIDENCE_CLOSURE.md","context\HANDOFFS\THUG2_PROP_EVIDENCE_CLOSURE.md","build\handoffs\gpt6_opus\MASTER_EXECUTION_QUEUE.json","build\handoffs\gpt6_opus\DEPENDENCY_GRAPH.json","build\handoffs\gpt6_opus\physgun\implementation_manifest.json","build\handoffs\gpt6_opus\thug2_props\conversion_queue.json","build\handoffs\gpt6_opus\REGRESSION_SPEC.json","build\handoffs\gpt6_opus\ACCEPTANCE_GATES.json","build\handoffs\gpt6_opus\SIDECAR_STRATEGY.json")
$missing=@($required|Where-Object{!(Test-Path (Join-Path $Root $_))})
$q=Get-Content (Join-Path $Root "build\handoffs\gpt6_opus\thug2_props\conversion_queue.json") -Raw|ConvertFrom-Json
$x=Get-Content (Join-Path $Root "build\prepared\prop_support_phase4\thug2_unresolved_reclassification_2026-10-06.json") -Raw|ConvertFrom-Json
$overlap=@($q.targets|Where-Object{$x.entries.identifier -contains $_.identifier})
$glbMissing=@();foreach($l in @($q.targets.level|Sort-Object -Unique)){if(!(Test-Path (Join-Path $Root ("build\prepared\thug2_prop_catalog\level_glb\"+$l+"\"+$l+".glb")))){$glbMissing+=$l}}
$phys=Get-Content (Join-Path $Root "build\handoffs\gpt6_opus\physgun\implementation_manifest.json") -Raw|ConvertFrom-Json
$idaMissing=@($phys.ida68|Where-Object{!(Test-Path $_)})
$result=[ordered]@{generated=(Get-Date).ToString("s");required_missing=$missing;prop_count=$q.target_count;semantic_overlap=$overlap.Count;missing_level_glbs=$glbMissing;ida68_missing=$idaMissing;known_physgun_asset_gaps=$phys.missing_assets;pass=($missing.Count -eq 0 -and $q.target_count -eq 85 -and $overlap.Count -eq 0 -and $glbMissing.Count -eq 0 -and $idaMissing.Count -eq 0)}
$result|ConvertTo-Json -Depth 6
$result|ConvertTo-Json -Depth 6|Set-Content (Join-Path $Root "build\handoffs\gpt6_opus\PREFLIGHT_RESULT.json") -Encoding UTF8
if(!$result.pass){exit 2}

# Runtime-map drift gate
$map=Get-Content (Join-Path $Root "build\handoffs\gpt6_opus\RUNTIME_INTEGRATION_MAP.json") -Raw|ConvertFrom-Json
$mappedSource=Join-Path $Root $map.active_source.path
$actualSourceHash=if(Test-Path $mappedSource){(Get-FileHash $mappedSource -Algorithm SHA256).Hash}else{"MISSING"}
$drift=($actualSourceHash -ne $map.active_source.sha256)
if($drift){Write-Error ("Runtime source drift: expected "+$map.active_source.sha256+" actual "+$actualSourceHash);exit 3}
Write-Output ("RUNTIME_MAP_SOURCE_HASH=PASS "+$actualSourceHash)

# Runtime harness readiness gate
$h=Join-Path $Root "build\handoffs\gpt6_opus\runtime_harness"
$need=@("BASELINE.json","PATCH_MANIFEST.json","COMPLETION_LEDGER.json","LOGGING_SPEC.json","CRASH_TRIAGE.json","STAGED_TESTS.json")
$hm=@($need|Where-Object{!(Test-Path (Join-Path $h $_))})
$ready=($hm.Count -eq 0)
$verdict=[ordered]@{READY_FOR_IMPLEMENTATION=if($ready){"YES"}else{"NO"};runtime_harness_missing=$hm;source_drift=$drift;preflight_base_pass=$result.pass}
$verdict|ConvertTo-Json -Depth 4|Set-Content (Join-Path $h "READY_VERDICT.json") -Encoding UTF8
$verdict|ConvertTo-Json -Depth 4
if(!$ready){exit 4}

# Current visual-feed validation
$feedValidator=Join-Path $Root "research\validate_opus_feed_bundle.ps1"
if(Test-Path $feedValidator){
  & $feedValidator -Root $Root
  if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}
}else{
  Write-Error "Missing research\validate_opus_feed_bundle.ps1"
  exit 4
}
