@echo off
setlocal
if not exist ".venv" (
  py -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python main.py --input input --output outputs\products.xlsx
pause

