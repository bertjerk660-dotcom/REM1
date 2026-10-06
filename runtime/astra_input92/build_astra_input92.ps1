$ErrorActionPreference = 'Stop'
$candidate = 'C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2\third_party\NVSE-6.4.9\fnv_gmod_thug2_input92_candidate'
$evidence = 'C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2\build\runtime\astra_input92'
$msbuild = 'C:\Program Files\Microsoft Visual Studio\18\Community\MSBuild\Current\Bin\MSBuild.exe'
$commonLib = 'C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2\third_party\NVSE-6.4.9\common\Release VC9\common_vc9.lib'
New-Item -ItemType Directory -Force "$candidate\bin" | Out-Null
Copy-Item -LiteralPath $commonLib -Destination "$candidate\bin\common_vc9.lib"
Get-FileHash -LiteralPath $commonLib | Format-List Path,Hash | Out-File "$evidence\common_dependency.txt"
& $msbuild "$candidate\FNVGModTHUG2.vcxproj" /t:Build /p:Configuration=Release /p:Platform=Win32 "/p:SolutionDir=$candidate/" "/p:OutDir=$candidate/bin/" "/p:IntDir=$candidate/obj/" /p:BuildProjectReferences=false /p:PostBuildEventUseInBuild=false /v:minimal *> "$evidence\build.log"
$code = $LASTEXITCODE
Write-Output "BUILD_EXIT=$code"
Get-Content "$evidence\build.log" -Tail 18
exit $code
