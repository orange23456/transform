$ErrorActionPreference = "Stop"
if (!(Test-Path ".venv")) {
  if (Get-Command py -ErrorAction SilentlyContinue) {
    py -m venv .venv
  } else {
    python -m venv .venv
  }
}
$Python = ".\.venv\Scripts\python.exe"
& $Python -m pip install -r requirements.txt
& $Python main.py --input input --output outputs\products.xlsx
