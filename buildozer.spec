[app]
source.dir = .
title = Digma Recorder
package.name = digmarecorder
package.domain = org.oldschool
version = 1.0.4
source.include_exts = py,png,jpg,kv,csv

requirements = python3,kivy,pyaes,oscpy
#,schedule
#android.permissions = INTERNET,ACCESS_NETWORK_STATE,FOREGROUND_SERVICE,WAKE_LOCK, WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.permissions = INTERNET,ACCESS_NETWORK_STATE,FOREGROUND_SERVICE,POST_NOTIFICATIONS,WAKE_LOCK,VIBRATE,FOREGROUND_SERVICE_DATA_SYNC,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,READ_MEDIA_IMAGES,READ_MEDIA_AUDIO,READ_MEDIA_VIDEO
#android.permissions = INTERNET,ACCESS_NETWORK_STATE,FOREGROUND_SERVICE,POST_NOTIFICATIONS,WAKE_LOCK,VIBRATE

android.accept_sdk_license = True
orientation = portrait
fullscreen = 1
android.archs = arm64-v8a
android.gradle_options = android.lintOptions.abortOnError=false

   # ВКЛЮЧАЕМ ТОТ САМЫЙ ПРОПУСК В КОРЕНЬ ДЛЯ АНДРОИД 10 (СТРОГО БЕЗ ЛИШНИХ КАВЫЧЕК!)
   #android.meta_data = android.requestLegacyExternalStorage=true
#android.manifest.application_arguments = android:requestLegacyExternalStorage="true"
 
   #android.manifest.application_arguments = <service android:name="org.kivy.android.DigmaJavaService" android:process=":service" android:stopWithTask="false" android:exported="false" />
   #android.manifest.application_arguments = android:requestLegacyExternalStorage="true" <service android:name="org.kivy.android.DigmaJavaService" android:process=":service" android:stopWithTask="false" android:exported="false" />
   #android.manifest.application_xml = <service android:name="org.kivy.android.DigmaJavaService" android:process=":service" android:stopWithTask="false" android:exported="false" />
   #android.manifest.application_xml =
   #    <service android:name='org.kivy.android.DigmaJavaService' android:process=':service' android:stopWithTask='false' android:exported='false' />


   # Наш фоновый мотор
   #services = digmaservice:service.py:foreground
   #services = digmaservice:service/main.py:foreground
   #:foregroundServiceType=dataSync

   # Прямая легальная вставка атрибута для нашей Java-службы в Манифест!
   #android.manifest.service_attributes = android
   #:foregroundServiceType="dataSync"
   #android.manifest_template = AndroidManifest.xml

   #p4a.hook = hook.py

# КАТЕГОРИЧЕСКИЙ ПРИКАЗ КИВИ: НЕ УБИВАТЬ СЛУЖБУ ПРИ СМАХИВАНИИ ОКНА!
android.services_stop_on_task_removed = False


   #services = digmaservice:service_motor.py:foreground
   #services = DigmaJavaService:service_motor.py:foreground
   
# ПОЛНОСТЬЮ СТИРАЕМ ИЛИ КОММЕНТИРУЕМ ВСЕ НАШИ ПРОШЛЫЕ ЭКСПЕРИМЕНТЫ:
   # android.manifest_template = ...
   # android.manifest.application_xml = ...
   # android.manifest.application_arguments = ...
   # services = ...

# 1. Подключаем нашу Java-папку с кодом службы
android.add_src = java

# 2. ЖЕСТКИЙ ПРАВИЛО-ЩИТ ДЛЯ GRADLE (ProGuard Keep Rules)
# Эти аргументы запрещают оптимизатору R8 сжимать, обфусцировать или вырезать наш Java-класс!
#android.gradle_dependencies = 'com.android.tools.build:gradle:7.4.2'
android.manifest.application_arguments = android:requestLegacyExternalStorage="true"
#android.manifest.application_xml = <service android:name='org.kivy.android.DigmaJavaService' android:process=':service' android:stopWithTask='false' android:exported='false' />

# 1. Подключаем нашу Java-папку с кодом службы
##android.add_src = java

# 2. ОФИЦИАЛЬНЫЙ СИТ ПРЕДОХРАНИТЕЛЯ PROGUARD
# Эта легальная строчка принудительно запрещает Gradle оптимизировать, 
# сжимать или вырезать любые кастомные Java-классы из нашего проекта!
#android.meta_data = proguard-rules.pro

# 3. Легально вшиваем тег службы в манифест (с одинарными кавычками!)
#android.manifest.application_xml = <service android:name='org.kivy.android.DigmaJavaService' android:process=':service' android:stopWithTask='false' android:exported='false' />
# Легальный, штатный запуск файла защиты без конфликтов split('=')!
android.proguard_rules = proguard-rules.pro

