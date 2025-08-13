$ErrorActionPreference = 'Stop'
python --version | Out-Null
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install pyinstaller flask minecraft-launcher-lib
$addData = "templates;templates"
pyinstaller --noconfirm --onefile --name "MinecraftWebLauncher" --add-data $addData launcher_server.py
Write-Host "Готово. Файл: dist\MinecraftWebLauncher.exe"
