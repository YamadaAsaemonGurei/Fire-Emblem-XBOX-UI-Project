@echo off
cd /d "%~dp0"
python -m pip install --target "%~dp0dependencies" -r "%~dp0requirements.txt"
pause
