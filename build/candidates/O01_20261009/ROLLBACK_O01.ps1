# O01 rollback: removes only the files this candidate added. Run in PowerShell.
$g='C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data'
Remove-Item "$g\REM_O01_ToolGun_Test.esp" -ErrorAction SilentlyContinue
Remove-Item "$g\meshes\rem\gmod\weapons\toolgun" -Recurse -ErrorAction SilentlyContinue
Remove-Item "$g\textures\rem\gmod\weapons\toolgun" -Recurse -ErrorAction SilentlyContinue
$pl="$env:LOCALAPPDATA\FalloutNV\plugins.txt"; (Get-Content $pl) | Where-Object { $_ -ne 'REM_O01_ToolGun_Test.esp' } | Set-Content $pl -Encoding ASCII
