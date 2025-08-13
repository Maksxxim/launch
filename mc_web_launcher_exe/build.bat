@echo off
setlocal
python --version >nul 2>nul || (echo Python не найден & exit /b 1)
python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install pyinstaller flask minecraft-launcher-lib
pyinstaller --noconfirm --onefile --name "MinecraftWebLauncher" --add-data "templates;templates" launcher_server.py
echo Готово. Файл: dist\MinecraftWebLauncher.exe
