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

[executed on device: DESKTOP-6PTSS3D (ac6e0673-c817-443f-a58e-9e6494209436)]