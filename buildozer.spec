[app]
# Имя приложения на экране вашего телефона
source.dir = .
title = Digma Recorder

# Техническое имя пакета (без пробелов)
package.name = digmarecorder
package.domain = org.oldschool

# Версия вашего приложения
version = 1.0

# Какие файлы упаковать внутрь APK
source.include_exts = py,png,jpg,kv,csv

# ТРЕБОВАНИЯ К БИБЛИОТЕКАМ (Сборщик сам скачает их из интернета)
requirements = python3,tinytuya,cryptography

# РАЗРЕШЕНИЯ ANDROID (Фоновый режим, интернет и локальная сеть)
android.permissions = INTERNET, ACCESS_NETWORK_STATE, FOREGROUND_SERVICE, WAKE_LOCK
android.accept_sdk_license = True

# Ориентация экрана
orientation = portrait
fullscreen = 1

# Настройки фонового сервиса (для работы 24/7)
services = DigmaService:main.py
