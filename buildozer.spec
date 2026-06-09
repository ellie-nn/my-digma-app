[app]
source.dir = .
title = Digma Recorder
package.name = digmarecorder
package.domain = org.oldschool
version = 1.0.5
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
   #android.add_src = java

# 2. ЖЕСТКИЙ ПРАВИЛО-ЩИТ ДЛЯ GRADLE (ProGuard Keep Rules)
# Эти аргументы запрещают оптимизатору R8 сжимать, обфусцировать или вырезать наш Java-класс!
    #android.gradle_dependencies = 'com.android.tools.build:gradle:7.4.2'

android.manifest.application_arguments = android:requestLegacyExternalStorage="true"
    #android.manifest.application_xml = <service android:name='org.kivy.android.DigmaJavaService' android:process=':service' android:stopWithTask='false' android:exported='false' />
    #android.manifest.application_xml = <service android:name='org.oldschool.digmarecorder.DigmaJavaService' android:process=':service' android:stopWithTask='false' android:exported='false' />

# 1. Подключаем нашу Java-папку с кодом службы
    ##android.add_src = java

# 2. ОФИЦИАЛЬНЫЙ СИТ ПРЕДОХРАНИТЕЛЯ PROGUARD
# Эта легальная строчка принудительно запрещает Gradle оптимизировать, 
# сжимать или вырезать любые кастомные Java-классы из нашего проекта!
    #android.meta_data = proguard-rules.pro

# 3. Легально вшиваем тег службы в манифест (с одинарными кавычками!)
    #android.manifest.application_xml = <service android:name='org.kivy.android.DigmaJavaService' android:process=':service' android:stopWithTask='false' android:exported='false' />
# Легальный, штатный запуск файла защиты без конфликтов split('=')!

    #android.proguard_rules = proguard-rules.pro
# Было: android.proguard_rules = proguard-rules.pro
# СТАНОВИТСЯ (Указываем точный системный путь к корню нашего репозитория!):
    #android.proguard_rules = %(android_add_src)s/proguard-rules.pro
# Было: android.proguard_rules = %(android_add_src)s/proguard-rules.pro
# СТАНОВИТСЯ (Кристально чистый, легальный путь без капризов парсера!):
android.proguard_rules = java/proguard-rules.pro

# Приказываем Buildozer официально активировать правила ProGuard к нашей сборке!
android.proguard = True

# ЖЕСТКИЙ ПРИКАЗ ПОДМЕНЫ ДЛЯ GRADLE (Пишется строго в одну монолитную строчку!):
    #android.gradle_dependencies = "android.applicationVariants.all { variant -> variant.outputs.all { output -> output.processManifestProvider.get().doFirst { var sourceManifest = new File('${projectDir}/../../../../AndroidManifest.xml'); var targetManifest = new File(getMultiApkManifestOutputDirectory().get().asFile, 'AndroidManifest.xml'); if (sourceManifest.exists()) { targetManifest.text = sourceManifest.text; println('=== [GRADLE] МАНИФЕСТ ХИРУРГИЧЕСКИ ПОДМЕНЕН НА НАШ ФАЙЛ! ===') } } } }"
    #android.add_src = java

# УЛЬТИМАТИВНЫЙ ЭКРАНИРОВАННЫЙ ЗАЖИМ:
# Мы полностью замаскировали фигурные скобки под коды \u007b и \u007d, а кавычки экранировали обратным слэшем \". 
# Теперь парсер спека проглотит строку без единого писка, а Gradle на сервере выполнит чистую подмену манифеста из корня репозитория!
    #android.gradle_dependencies = "android.applicationVariants.all \u007b variant -> variant.outputs.all \u007b output -> output.processManifestProvider.get().doFirst \u007b var srcM = new File('${projectDir}/../../../../AndroidManifest.xml'); var tgtM = new File(getMultiApkManifestOutputDirectory().get().asFile, 'AndroidManifest.xml'); if (srcM.exists()) \u007b tgtM.text = srcM.text \u007d \u007d \u007d \u007d"
    #android.add_src = java

# БРОНЕБОЙНЫЙ ЗАЖИМ BASE64:
# Парсер спека видит только буквы и цифры, поэтому не выдаст ошибку "dependencies {". 
# А Gradle на сервере раскодирует эту строку в идеальный скрипт подмены манифеста!
    #android.gradle_dependencies = "byte[] d = java.util.Base64.getDecoder().decode('YW5kcm9pZC5hcHBsaWNhdGlvblZhcmlhbnRzLmFsbCB7IHYgLT4gdi5vdXRwdXRzLmFsbCB7IG8gLT4gby5wcm9jZXNzTWFuaWZlc3RQcm92aWRlci5nZXQoKS5kb0ZpcnN0IHsgdmFyIHMgPSBuZXcgRmlsZSgnLi4vLi4vLi4vLi4vQW5kcm9pZE1hbmlmZXN0LnhtbCcpOyB2YXIgdCA9IG5ldyBGaWxlKGdldE11bHRpQXBrTWFuaWZlc3RPdXRwdXREaXJlY3RvcnkoKS5nZXQoKS5hc0ZpbGUsICdBbmRyb2lkTWFuaWZlc3QueG1sJyk7IGlmIChzLmV4aXN0cygpKSB7IHQudGV4dCA9IHMudGV4dDsgcHJpbnRsbihbJz09PSBbR1JBRExFXSBNQU5JRkVTVCBTV0FQUEVEXSA9PT0nXSk7IH0gfSB9IH0gOw=='); new GroovyShell().evaluate(new String(d))"

# УЛЬТИМАТИВНЫЙ ГЛОБАЛЬНЫЙ ЗАЖИМ BASE64:
# Мы перекодировали скрипт с директивой project.afterEvaluate. 
# Теперь код легально вырвется из блока dependencies и намертво перезапишет манифест файлом 1.0.4.1 из корня!
    #android.gradle_dependencies = "byte[] d = java.util.Base64.getDecoder().decode('cHJvamVjdC5hZnRlckV2YWx1YXRlIHsgYW5kcm9pZC5hcHBsaWNhdGlvblZhcmlhbnRzLmFsbCB7IHYgLT4gdi5vdXRwdXRzLmFsbCB7IG8gLT4gby5wcm9jZXNzTWFuaWZlc3RQcm92aWRlci5nZXQoKS5kb0ZpcnN0IHsgdmFyIHMgPSBuZXcgRmlsZSgnLi4vLi4vLi4vLi4vQW5kcm9pZE1hbmlmZXN0LnhtbCcpOyB2YXIgdCA9IG5ldyBGaWxlKGdldE11bHRpQXBrTWFuaWZlc3RPdXRwdXREaXJlY3RvcnkoKS5nZXQoKS5hc0ZpbGUsICdBbmRyb2lkTWFuaWZlc3QueG1sJyk7IGlmIChzLmV4aXN0cygpKSB7IHQudGV4dCA9IHMudGV4dDsgcHJpbnRsbihbJz09PSBbR1JBRExFXSBNQU5JRkVTVCBTV0FQUEVEXSA9PT0nXSk7IH0gfSB9IH0gfSB9'); new GroovyShell(project.class.classLoader).evaluate(new String(d))"
android.add_src = java

# БРОНЕБОЙНАЯ ИНЪЕКЦИЯ КАВЫЧЕК BASE64:
# Мы силой закрываем метод implementation с помощью '); }, а в конце открывать пустой вызов, чтобы не сломать парсер Gradle.
# Код гарантированно вырвется на глобальный уровень проекта и намертво подменит манифест файлом 1.0.4.1 из корня!
    #android.gradle_dependencies = "dummy'); }; project.afterEvaluate { android.applicationVariants.all { v -> v.outputs.all { o -> o.processManifestProvider.get().doFirst { var s = new File('../../../../AndroidManifest.xml'); var t = new File(getMultiApkManifestOutputDirectory().get().asFile, 'AndroidManifest.xml'); if (s.exists()) { t.text = s.text; println('=== [GRADLE] MANIFEST SWAPPED ==='); } } } } }; dependencies { implementation('dummy"

android.gradle_dependencies = androidx.annotation:annotation:1.1.0 \u007d \n //
#\u0027\u0029 \u007d \n println(\u0027=== [GRADLE INIT] ХАК-СКРИПТ РАБОТАЕТ ВНУТРИ СИСТЕМНОГО BUILD.GRADLE ===\u0027); //"
