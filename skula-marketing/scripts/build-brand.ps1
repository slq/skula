param([string]$Root = (Split-Path $PSScriptRoot -Parent))
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$brandDir = Join-Path $Root 'brand'
$publicDir = Join-Path $Root 'public'
New-Item -ItemType Directory -Force -Path $brandDir,$publicDir | Out-Null
$navy = '#17354A'
$teal = '#138F88'
$mint = '#66DFCB'
function SaveUtf8([string]$Path, [string]$Content) {
  [IO.File]::WriteAllText($Path, $Content, [Text.UTF8Encoding]::new($false))
}
function Outline([string]$Text, [single]$Size, [single]$X, [single]$Y, [string]$Color) {
  $family = [Drawing.FontFamily]::new('Segoe UI')
  $path = [Drawing.Drawing2D.GraphicsPath]::new()
  $path.AddString($Text, $family, 1, $Size, [Drawing.PointF]::new(0,0), [Drawing.StringFormat]::GenericTypographic)
  $bounds = $path.GetBounds()
  $points = $path.PathPoints
  $types = $path.PathTypes
  $commands = [Collections.Generic.List[string]]::new()
  $culture = [Globalization.CultureInfo]::InvariantCulture
  function Coord([single]$Value) { return $Value.ToString('0.###', $culture) }
  for ($i = 0; $i -lt $points.Length; $i++) {
    $type = $types[$i] -band 7
    $px = Coord ($points[$i].X - $bounds.X + $X)
    $py = Coord ($points[$i].Y - $bounds.Y + $Y)
    if ($type -eq 0) { $commands.Add("M$px $py") }
    elseif ($type -eq 1) { $commands.Add("L$px $py") }
    elseif ($type -eq 3) {
      $x2 = Coord ($points[$i+1].X - $bounds.X + $X)
      $y2 = Coord ($points[$i+1].Y - $bounds.Y + $Y)
      $x3 = Coord ($points[$i+2].X - $bounds.X + $X)
      $y3 = Coord ($points[$i+2].Y - $bounds.Y + $Y)
      $commands.Add("C$px $py $x2 $y2 $x3 $y3")
      $i += 2
    }
    if (($types[$i] -band 128) -ne 0) { $commands.Add('Z') }
  }
  $width = $bounds.Width
  $path.Dispose()
  $family.Dispose()
  return @{ Svg = ('<path fill="' + $Color + '" d="' + ($commands -join ' ') + '"/>'); Width = $width }
}
function Mark([string]$Roof, [string]$Left, [string]$Right) {
  return @"
<path d="M24 54 64 21 104 54" fill="none" stroke="$Roof" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M28 61C40 57 51 60 60 67V104C50 98 40 94 28 97Z" fill="$Left"/>
<path d="M68 67C77 60 88 57 100 61V97C88 94 78 98 68 104Z" fill="$Right"/>
"@
}
function Svg([string]$ViewBox, [string]$Body, [string]$Title) {
  return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="' + $ViewBox + '" role="img" aria-label="' + $Title + '"><title>' + $Title + '</title>' + $Body + '</svg>'
}
$normalMark = Mark $navy $teal $teal
$lightMark = Mark '#FFFFFF' $mint $mint
SaveUtf8 (Join-Path $brandDir 'mark.svg') (Svg '0 0 128 128' $normalMark 'Skula — dom i otwarta książka')
SaveUtf8 (Join-Path $brandDir 'mark-light.svg') (Svg '0 0 128 128' $lightMark 'Skula — znak na ciemne tło')
SaveUtf8 (Join-Path $brandDir 'mark-mono.svg') (Svg '0 0 128 128' (Mark 'currentColor' 'currentColor' 'currentColor') 'Skula')
foreach ($variant in @('logo','logo-light','logo-mono')) {
  $firstColor = $navy; $lastColor = $teal; $sign = $normalMark
  if ($variant -eq 'logo-light') { $firstColor = '#FFFFFF'; $lastColor = $mint; $sign = $lightMark }
  if ($variant -eq 'logo-mono') { $firstColor = 'currentColor'; $lastColor = 'currentColor'; $sign = Mark 'currentColor' 'currentColor' 'currentColor' }
  $first = Outline 'Skula' 66 142 39 $firstColor
  $last = @{ Svg = ''; Width = 0 }
  $totalWidth = [Math]::Ceiling(142 + $first.Width + 4 + $last.Width + 24)
  SaveUtf8 (Join-Path $brandDir ($variant + '.svg')) (Svg "0 0 $totalWidth 128" ($sign + $first.Svg + $last.Svg) 'Skula')
}
$appMark = Mark '#FFFFFF' $mint '#FFFFFF'
$appBody = '<rect width="128" height="128" rx="28" fill="' + $navy + '"/><g transform="translate(11.52 11.52) scale(.82)">' + $appMark + '</g>'
SaveUtf8 (Join-Path $brandDir 'app-icon.svg') (Svg '0 0 128 128' $appBody 'Skula — ikona aplikacji')
$faviconBody = '<rect width="32" height="32" rx="7" fill="' + $navy + '"/><path d="M7 13 16 5.5 25 13" fill="none" stroke="#FFFFFF" stroke-width="2.75" stroke-linecap="round" stroke-linejoin="round"/><path d="M7 15Q11 14 14.5 16.5V26Q11 24 7 24.5Z" fill="' + $mint + '"/><path d="M17.5 16.5Q21 14 25 15V24.5Q21 24 17.5 26Z" fill="#FFFFFF"/>'
SaveUtf8 (Join-Path $publicDir 'favicon.svg') (Svg '0 0 32 32' $faviconBody 'Skula')
$maskableBody = '<rect width="128" height="128" fill="' + $navy + '"/><g transform="translate(20.48 20.48) scale(.68)">' + $appMark + '</g>'
SaveUtf8 (Join-Path $brandDir 'app-icon-maskable.svg') (Svg '0 0 128 128' $maskableBody 'Skula — ikona maskowalna')
$appleBody = '<rect width="128" height="128" fill="' + $navy + '"/><g transform="translate(11.52 11.52) scale(.82)">' + $appMark + '</g>'
SaveUtf8 (Join-Path $brandDir 'apple-touch-icon.svg') (Svg '0 0 128 128' $appleBody 'Skula — ikona Apple')
# Preserve the calculated viewBox for the outlined wordmark.
$logoSource = [IO.File]::ReadAllText((Join-Path $brandDir 'logo.svg'))
$logoView = [regex]::Match($logoSource, 'viewBox="([^"]+)"').Groups[1].Value
$previewLogo = $logoSource -replace '^<svg[^>]+>', ('<svg x="66" y="151" width="566" height="128" viewBox="' + $logoView + '">')
$lightSource = [IO.File]::ReadAllText((Join-Path $brandDir 'logo-light.svg'))
$previewLight = $lightSource -replace '^<svg[^>]+>', ('<svg x="730" y="174" width="444" height="105" viewBox="' + $logoView + '">')
$preview = @"
<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="850" viewBox="0 0 1280 850">
<rect width="1280" height="850" fill="#F4F7F8"/>
<text x="72" y="70" font-family="Segoe UI,Arial,sans-serif" font-size="16" font-weight="600" letter-spacing="3" fill="$teal">Skula / IDENTYFIKACJA</text>
<rect x="40" y="111" width="620" height="257" rx="22" fill="white"/>
<rect x="680" y="111" width="560" height="257" rx="22" fill="$navy"/>
$previewLogo
$previewLight
<text x="72" y="336" font-family="Segoe UI,Arial,sans-serif" font-size="14" fill="#647784">LOGO / JASNE TŁO</text>
<text x="712" y="336" font-family="Segoe UI,Arial,sans-serif" font-size="14" fill="#A7BFCA">LOGO / CIEMNE TŁO</text>
<rect x="40" y="388" width="375" height="310" rx="22" fill="white"/>
<rect x="435" y="388" width="375" height="310" rx="22" fill="white"/>
<rect x="830" y="388" width="410" height="310" rx="22" fill="white"/>
<svg x="135" y="426" width="184" height="184" viewBox="0 0 128 128">$appBody</svg>
<svg x="547" y="441" width="150" height="150" viewBox="0 0 128 128">$normalMark</svg>
<svg x="938" y="477" width="64" height="64" viewBox="0 0 32 32">$faviconBody</svg>
<svg x="1034" y="493" width="32" height="32" viewBox="0 0 32 32">$faviconBody</svg>
<svg x="1095" y="501" width="16" height="16" viewBox="0 0 32 32">$faviconBody</svg>
<text x="72" y="658" font-family="Segoe UI,Arial,sans-serif" font-size="14" fill="#647784">IKONA APLIKACJI</text>
<text x="467" y="658" font-family="Segoe UI,Arial,sans-serif" font-size="14" fill="#647784">ZNAK / DOM + KSIĄŻKA</text>
<text x="862" y="658" font-family="Segoe UI,Arial,sans-serif" font-size="14" fill="#647784">FAVICON / 64 · 32 · 16 PX</text>
<rect x="72" y="745" width="32" height="32" rx="10" fill="$navy"/>
<text x="117" y="767" font-family="Segoe UI,Arial,sans-serif" font-size="15" fill="$navy">Granat #17354A</text>
<rect x="329" y="745" width="32" height="32" rx="10" fill="$teal"/>
<text x="374" y="767" font-family="Segoe UI,Arial,sans-serif" font-size="15" fill="$navy">Turkus #138F88</text>
<rect x="586" y="745" width="32" height="32" rx="10" fill="$mint"/>
<text x="631" y="767" font-family="Segoe UI,Arial,sans-serif" font-size="15" fill="$navy">Mięta #66DFCB</text>
<text x="72" y="815" font-family="Segoe UI,Arial,sans-serif" font-size="14" fill="#647784">SVG + PNG + ICO / GOTOWE DO UŻYCIA</text>
</svg>
"@
SaveUtf8 (Join-Path $brandDir 'preview.svg') $preview
Write-Output 'Wygenerowano pliki SVG w brand/ i public/.'