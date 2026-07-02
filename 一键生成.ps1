$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$records = Join-Path $root "html_records.json"
$outputDir = Join-Path $root "outputs\dalong_all_series"
$htmlGenRoot = "C:\Users\hz-user\Documents\HTML生成"
$generatedRoot = Join-Path $root "generated_html"
$tempControlFolder = "C:\Users\hz-user\Desktop\大龙\温控系列全部产品"

$python = "C:\Users\hz-user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$node = "C:\Users\hz-user\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
$nodeModules = "C:\Users\hz-user\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules"
$localNodeModules = Join-Path $root "node_modules"

if (!(Test-Path -LiteralPath $python)) { $python = "python" }
if (!(Test-Path -LiteralPath $node)) { $node = "node" }
if (!(Test-Path -LiteralPath $localNodeModules) -and (Test-Path -LiteralPath $nodeModules)) {
  New-Item -ItemType Junction -Path $localNodeModules -Target $nodeModules | Out-Null
}

$env:PYTHONIOENCODING = "utf-8"

Write-Host "1/3 正在生成 HTML 代码..."
& $python (Join-Path $root "run_html_generators.py") --script-root $htmlGenRoot --output-root $generatedRoot

Write-Host "2/3 正在抽取 HTML 记录..."
& $python (Join-Path $root "extract_html_records.py") --html-root $generatedRoot --out $records --sources "加热搅拌全部产品=Atomfair_heating_stirring_HTML" "温控系列全部产品=$tempControlFolder" "蒸馏系列全部产品=Atomfair_distillation_HTML"

Write-Host "3/3 正在生成 Excel..."
& $node (Join-Path $root "build_excel_from_html.mjs") $records $outputDir

Write-Host ""
Write-Host "完成："
Write-Host (Join-Path $outputDir "大龙全系列产品.xlsx")
Write-Host "桌面副本：C:\Users\hz-user\Desktop\大龙全系列产品.xlsx"
