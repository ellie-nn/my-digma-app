[app]
source.dir = .
title = Digma Recorder
package.name = digmarecorder
package.domain = org.oldschool
version = 1.0.4
source.include_exts = py,png,jpg,kv,csv

requirements = python3,kivy
android.permissions = INTERNET, ACCESS_NETWORK_STATE, FOREGROUND_SERVICE, WAKE_LOCK, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.accept_sdk_license = True
orientation = portrait
fullscreen = 1
android.archs = arm64-v8a
android.gradle_options = android.lintOptions.abortOnError=false

# ВКЛЮЧАЕМ ТОТ САМЫЙ ПРОПУСК В КОРЕНЬ ДЛЯ АНДРОИД 10 (СТРОГО БЕЗ ЛИШНИХ КАВЫЧЕК!)
android.meta_data = android.requestLegacyExternalStorage=true

# Наш фоновый мотор
services = DigmaService:service.py

