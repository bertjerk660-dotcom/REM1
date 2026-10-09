# O00 rollback: removes only the files this candidate added. Run in PowerShell.
$g='C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data'
Remove-Item "$g\REM_GoldenBench_Test.esp" -ErrorAction SilentlyContinue
Remove-Item "$g\meshes\rem\golden_bench" -Recurse -ErrorAction SilentlyContinue
Remove-Item "$g\textures\rem\golden_bench" -Recurse -ErrorAction SilentlyContinue
# If the sidecar was enabled for a test, remove its line from plugins.txt:
$pl="$env:LOCALAPPDATA\FalloutNV\plugins.txt"; (Get-Content $pl) | Where-Object { $_ -ne 'REM_GoldenBench_Test.esp' } | Set-Content $pl -Encoding ASCII
