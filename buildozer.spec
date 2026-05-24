[app]
source.dir = .
title = Digma Recorder
package.name = digmarecorder
package.domain = org.oldschool
version = 1.0.2
source.include_exts = py,png,jpg,kv,csv

# ТРЕБОВАНИЯ: Только чистый Python и базовая библиотека Kivy
requirements = python3,kivy

# ПРАВА: Базовый минимум для вывода графики на экран телефона
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# ОРИЕНТАЦИЯ
orientation = portrait
fullscreen = 1

# Жестко указываем компилятору собрать под современную 64-битную архитектуру
android.archs = arm64-v8a
