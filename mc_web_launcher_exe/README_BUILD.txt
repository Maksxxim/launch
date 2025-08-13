# Minecraft Web Launcher — one-file EXE build
Соберите переносимый `MinecraftWebLauncher.exe`, который открывает интерфейс в браузере и запускает Minecraft локально.

## Быстрый старт (Windows)
1) Откройте `launcher_server.py` и поставьте свои `CLIENT_ID` и `REDIRECT_URI` (должен быть `http://localhost:5000/auth/callback`).  
2) Дважды кликните `build.bat` **или** выполните в PowerShell `.\build.ps1`.  
3) Заберите `dist\MinecraftWebLauncher.exe`. Запустите его — браузер сам откроется на `http://localhost:5000`.

## Важно
- EXE работает **без установленного Python** на конечном ПК. Java требуется для Minecraft Java Edition (обычно 17+).
- Токены сохраняются в `%APPDATA%\.minecraft\WebLauncher\tokens.json`.
- Для macOS/Linux собирать отдельно на соответствующей ОС.

## GitHub Actions (без локальной установки Python)
Залейте файлы в GitHub-репозиторий и используйте workflow из `.github/workflows/build.yml`. Он соберёт артефакт `MinecraftWebLauncher.exe`, который можно скачать со страницы Actions.
