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
# ТРЕБОВАНИЯ: Только чистый Python и базовая библиотека
requirements = python3,tinytuya

# РАЗРЕШЕНИЯ ANDROID (Фоновый режим, интернет и локальная сеть)
#android.permissions = INTERNET, ACCESS_NETWORK_STATE, FOREGROUND_SERVICE, WAKE_LOCK, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WAKE_LOCK
#android.accept_sdk_license = True
#android.meta_data = android.requestLegacyExternalStorage=true
#android.gradle_options = android.lintOptions.abortOnError=false

# ФИКС ДЛЯ ANDROID 10: Собираем строго под 64-битные современные процессоры
android.archs = arm64-v8a

# Ориентация экрана
orientation = portrait
fullscreen = 1

# Настройки фонового сервиса (для работы 24/7)
services = DigmaService:service.py

log_level = 1

# Ищем строку и убираем из нее тяжелые графические требования
#p4a.branch = master
#android.api = 29
#android.minapi = 29
#android.ndk_api = 29

# ОЛДСКУЛЬНЫЙ ГЛУШИТЕЛЬ ДЛЯ JAVA И XLINT:
# Принудительно отключаем панику компилятора из-за устаревшего API
android.gradle_options = android.lintOptions.abortOnError=false
android.add_compile_options = "-Xlint:-deprecation", "-Xlint:-options"

#-------------
[app]

# ПРАВА: Добавляем Bluetooth, который так яростно требует Gradle
#android.permissions = INTERNET, ACCESS_NETWORK_STATE, FOREGROUND_SERVICE, WAKE_LOCK, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, BLUETOOTH, BLUETOOTH_ADMIN

# ИГНОРИРОВАНИЕ ОШИБОК ИНСПЕКТОРА: Приказ Gradle не останавливать сборку
#android.gradle_options = android.lintOptions.abortOnError=false
#------------------

# =====================================================================
