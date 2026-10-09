# Game-input helper for the O00 runtime self-test: scancode keys, clicks, focus, screenshots.
Add-Type -AssemblyName System.Drawing, System.Windows.Forms
if (-not ('GI' -as [type])) {
Add-Type @"
using System; using System.Runtime.InteropServices;
public static class GI {
  [StructLayout(LayoutKind.Sequential)] struct KI { public ushort vk, scan; public uint flags, time; public IntPtr extra; }
  [StructLayout(LayoutKind.Sequential)] struct MI { public int dx, dy; public uint data, flags, time; public IntPtr extra; }
  [StructLayout(LayoutKind.Explicit)] struct IN { [FieldOffset(0)] public uint type; [FieldOffset(8)] public KI k; [FieldOffset(8)] public MI m; }
  [DllImport("user32.dll")] static extern uint SendInput(uint n, IN[] i, int s);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L, T, R, B; }
  public static void Key(ushort scan, bool up) {
    var i = new IN[1]; i[0].type = 1; i[0].k.scan = scan; i[0].k.flags = 0x8u | (up ? 0x2u : 0u);
    SendInput(1, i, Marshal.SizeOf(typeof(IN)));
  }
  public static void Mouse(uint flags, int dx, int dy) {
    var i = new IN[1]; i[0].type = 0; i[0].m.flags = flags; i[0].m.dx = dx; i[0].m.dy = dy;
    SendInput(1, i, Marshal.SizeOf(typeof(IN)));
  }
}
"@
}
$SC = @{ '`'=0x29; 'ESC'=0x01; 'ENTER'=0x1C; 'SPACE'=0x39; 'W'=0x11; 'A'=0x1E; 'S'=0x1F; 'D'=0x20; 'E'=0x12; 'TAB'=0x0F; 'F5'=0x3F; 'F9'=0x43; 'UP'=0x48; 'DOWN'=0x50 }
$CH = @{}
"1234567890".ToCharArray() | ForEach-Object -Begin { $k = 2 } -Process { $CH[[string]$_] = $k; $k++ }
$CH['0'] = 0x0B
@{q=0x10;w=0x11;e=0x12;r=0x13;t=0x14;y=0x15;u=0x16;i=0x17;o=0x18;p=0x19;a=0x1E;s=0x1F;d=0x20;f=0x21;g=0x22;h=0x23;j=0x24;k=0x25;l=0x26;z=0x2C;x=0x2D;c=0x2E;v=0x2F;b=0x30;n=0x31;m=0x32}.GetEnumerator() | ForEach-Object { $CH[$_.Key] = $_.Value }
$CH[' '] = 0x39; $CH['.'] = 0x34; $CH['-'] = 0x0C; $CH['_'] = 0x0C

function Tap($scan, $ms = 60) { [GI]::Key($scan, $false); Start-Sleep -Milliseconds $ms; [GI]::Key($scan, $true); Start-Sleep -Milliseconds 60 }
function Hold($scan, $ms) { [GI]::Key($scan, $false); Start-Sleep -Milliseconds $ms; [GI]::Key($scan, $true) }
function TypeText($t) {
  foreach ($c in $t.ToCharArray()) {
    $s = [string]$c; $shift = ($s -eq '_') -or ($s -cmatch '[A-Z]')
    $k = $CH[$s.ToLower()]
    if ($null -eq $k) { throw "no scancode for '$s'" }
    if ($shift) { [GI]::Key(0x2A, $false) }
    Tap $k 30
    if ($shift) { [GI]::Key(0x2A, $true) }
  }
}
# The console key TOGGLES. Open once, send any number of Cmd lines, then close once.
function OpenCon { Tap 0x29; Start-Sleep -Milliseconds 400 }
function CloseCon { Tap 0x29; Start-Sleep -Milliseconds 300 }
function Cmd($cmd) { TypeText $cmd; Tap 0x1C; Start-Sleep -Milliseconds 450 }
function Console($cmd) { OpenCon; Cmd $cmd; CloseCon }
function GameWin { Get-Process FalloutNV -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1 }
function Focus { $p = GameWin; if ($p) { [GI]::ShowWindow($p.MainWindowHandle, 9) | Out-Null; [GI]::SetForegroundWindow($p.MainWindowHandle) | Out-Null; Start-Sleep -Milliseconds 400 } }
function Shot($name, $scale = 0.5) {
  $p = GameWin; $r = New-Object GI+RECT
  if ($p) { [GI]::GetWindowRect($p.MainWindowHandle, [ref]$r) | Out-Null } else { $r.R = 2560; $r.B = 1440 }
  $w = $r.R - $r.L; $h = $r.B - $r.T
  $bmp = New-Object System.Drawing.Bitmap $w, $h
  $g = [System.Drawing.Graphics]::FromImage($bmp); $g.CopyFromScreen($r.L, $r.T, 0, 0, $bmp.Size)
  $sm = New-Object System.Drawing.Bitmap $bmp, ([int]($w * $scale)), ([int]($h * $scale))
  $out = "C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2\build\candidates\O00_20261009\runtime_evidence\$name.png"
  New-Item -ItemType Directory -Force (Split-Path $out) | Out-Null
  $sm.Save($out, [System.Drawing.Imaging.ImageFormat]::Png); $g.Dispose(); $bmp.Dispose(); $sm.Dispose()
  "shot $out (${w}x${h})"
}
function Click($x, $y) {  # window-relative pixel
  $p = GameWin; $r = New-Object GI+RECT; [GI]::GetWindowRect($p.MainWindowHandle, [ref]$r) | Out-Null
  $sx = [int](($r.L + $x) * 65535 / [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width)
  $sy = [int](($r.T + $y) * 65535 / [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height)
  [GI]::Mouse(0x8001, $sx, $sy); Start-Sleep -Milliseconds 80; [GI]::Mouse(0x0002, 0, 0); Start-Sleep -Milliseconds 60; [GI]::Mouse(0x0004, 0, 0)
}
function Look($dx, $dy) { [GI]::Mouse(0x0001, $dx, $dy) }
