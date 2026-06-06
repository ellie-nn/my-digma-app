# Жесткий приказ оптимизатору Gradle: сохранить наш Java-класс в бинарнике целиком!
#-keep class org.kivy.android.DigmaJavaService { *; }
#-keep class org.oldschool.digmarecorder.DigmaJavaService { *; }
# УЛЬТИМАТИВНЫЙ ИНЖЕНЕРНЫЙ ЩИТ PROGUARD
# Мы приказываем Gradle сохранить наш класс, все его методы, переменные 
# и системные коллбэки Android в абсолютно нетронутом бинарном виде!
-keep class org.oldschool.digmarecorder.DigmaJavaService {
    *;
}
-keep public class * extends android.app.Service
