[app]
source.dir = .
title = Digma Recorder
package.name = digmarecorder
package.domain = org.oldschool
version = 1.0.4
source.include_exts = py,png,jpg,kv,csv

requirements = python3,kivy
android.permissions = INTERNET, ACCESS_NETWORK_STATE
android.accept_sdk_license = True
orientation = portrait
fullscreen = 1
android.archs = arm64-v8a
android.gradle_options = android.lintOptions.abortOnError=false
