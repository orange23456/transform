@echo off
setlocal
if not exist ".venv" (
  py -m venv .venv 2>nul
  if errorlevel 1 python -m venv .venv
)
".venv\Scripts\python.exe" -m pip install -r requirements.txt
".venv\Scripts\python.exe" main.py --input input --output outputs\products.xlsx
pause
