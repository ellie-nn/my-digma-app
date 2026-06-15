fuck off
это блокнот search1
#==========≠======≠
<application ... tools:node="replace">
<service android:name="org.oldschool.digmarecorder.DigmaJavaService" ... tools:node="replace"/>

#=================
- name: Hack Kivy Java Core to Persistent-Immortal
  run: |
    echo "=== [HACK] ХИРУРГИЧЕСКИЙ НАДРЕЗ В ЯДРЕ KIVY ==="
    find .buildozer/ -name "PythonService.java" -type f | while read -r java_file; do
      echo "Модифицируем системный файл: $java_file"
      
      # ХИРУРГИЧЕСКИЙ ЗАЖИМ БЕЗ ФЛАГА 'g':
      # Мы ищем строго строку возврата "return START_NOT_STICKY;" и меняем её 
      # на "return START_STICKY;". Соседние методы ядра Kivy останутся абсолютно нетронутыми!
      sed -i "s|return START_NOT_STICKY;|return START_STICKY;|g" "$java_file"
    done
  
#==================
java/org/kivy/android/PythonService.java
#--------------------
package org.kivy.android; // СТРОГО РОДНОЙ ПАКЕТ KIVY!

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Notification;

// Имя класса теперь СТРОГО совпадает с манифестом!
public class PythonService extends Service {
    @Override
    public void onCreate() {
        super.onCreate();
        
        // 1. Создаем канал уведомлений для Android 10/13 [↑]
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                "digma_channel", "Digma Service", NotificationManager.IMPORTANCE_LOW
            );
            NotificationManager manager = getSystemService(NotificationManager.class);
            if (manager != null) manager.createNotificationChannel(channel);
        }

        // 2. Строим уведомление бессмертия [↑]
        Notification.Builder builder = new Notification.Builder(this, "digma_channel")
            .setContentTitle("Digma Service")
            .setContentText("Фоновый мотор розетки работает...")
            .setSmallIcon(getApplicationInfo().icon);

        // 3. Запускаем Foreground (2 параметра для Android 10/13!) [↑]
        startForeground(101, builder.build());

        // 4. Поднимаем наш чистый независимый Linux-поток Python [↑]
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    // Запускаем файл service_motor.py из внутренней памяти приложения
                    String[] cmd = {"python3", getFilesDir().getAbsolutePath() + "/service_motor.py"};
                    Runtime.getRuntime().exec(cmd).waitFor();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        return START_STICKY; // Наш жесткий липкий зажим [↑]
    }

    @Override
    public IBinder onBind(Intent intent) { return null; }
}

#-------------------
        try:
            Context = autoclass('org.kivy.android.PythonActivity').mActivity
            
            Intent = autoclass('android.content.Intent')
            # Вызываем СТРОГО тот класс, который вы нашли в декомпилированном XML! [↑]
            ServiceClass = autoclass("org.kivy.android.PythonService")
            
            intent = Intent(Context, ServiceClass)
            result = Context.startForegroundService(intent)
            
            if not result:
                raise Exception("Операционная система Android вернула None!")
                
            self.label.text = "🚀 СЛУЖБА УСПЕШНО ЗАПУЩЕНА ЧЕРЕЗ РОДНОЙ JAVA-КЛАСС!"
        except Exception as e:
            self.label.text = f"❌ ОШИБКА ЗАПУСКА:\n{e}"

#------------------
android.add_src = java
services = digmaservice:service_motor.py:foreground

#=========≈=====
<service android:name="org.oldschool.digmarecorder.DigmaJavaService"
         android:process=":service"
         android:stopWithTask="false"
         android:exported="false" />
#==≈=============
# 1. Указываем путь к нашей Java-папке, чтобы Gradle скомпилировал DigmaJavaService
android.add_src = src

# 2. Удаляем старую строку services! Она больше НЕ НУЖНА, так как Kivy-сервисы мертвы
# services = ... (УДАЛИТЬ ИЛИ ЗАКОММЕНТИРОВАТЬ!)
#===============≈=
from kivy.app import App
from kivy.uix.widget import Widget
from jnius import autoclass

class EmptyWindowApp(App):
    def build(self):
        try:
            # 1. Достаем контекст активности окна
            Context = autoclass('org.kivy.android.PythonActivity').mActivity
            
            # 2. Напрямую вызываем нашу кастомную Java-службу!
            Intent = autoclass('android.content.Intent')
            ServiceClass = autoclass('org.oldschool.digmarecorder.DigmaJavaService')
            
            intent = Intent(Context, ServiceClass)
            Context.startForegroundService(intent) # Поджигаем фитиль!
            print("=== [MAIN] JAVA-СЛУЖБА УСПЕШНО ЗАПУЩЕНА ЧЕРЕЗ СТАРТ-ИНТЕНТ ===")
        except Exception as e:
            print(f"Ошибка запуска: {e}")
            
        return Widget() # Возвращаем абсолютно пустой графический виджет

if __name__ == '__main__':
    EmptyWindowApp().run()
#====≈===========
android:stopWithTask="false"
#==================
import time
import sys

# Перенаправляем потоки ошибок в Documents, чтобы видеть работу
sys.stdout = open("app_log.txt", "a", encoding="utf-8")
sys.stderr = sys.stdout

class BackgroundMotor:
    def __init__(self):
        print("=== [PYTHON] БЕССМЕРТНЫЙ МОТОР ИНИЦИАЛИЗИРОВАН ===")
        sys.stdout.flush()

    def run_forever(self):
        while True:
            # Наш тестовый цикл: пишем время в файл лога
            print(f"[{time.strftime('%H:%M:%S')}] Фоновый процесс дышит в фоне!")
            sys.stdout.flush() # Принудительно выталкиваем строку на диск!
            time.sleep(1.0)

if __name__ == '__main__':
    BackgroundMotor().run_forever()
#=========≈====
package org.oldschool.digmarecorder;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Notification;

public class DigmaJavaService extends Service {
    @Override
    public void onCreate() {
        super.onCreate();
        // 1. Жестко зажимаем NotificationChannel на уровне родного Android
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                "digma_channel", "Digma Service", NotificationManager.IMPORTANCE_LOW
            );
            NotificationManager manager = getSystemService(NotificationManager.class);
            if (manager != null) manager.createNotificationChannel(channel);
        }

        // 2. Строим легальное уведомление бессмертия
        Notification.Builder builder = new Notification.Builder(this, "digma_channel")
            .setContentTitle("Digma Service")
            .setContentText("Фоновый мотор работает...")
            .setSmallIcon(getApplicationInfo().icon);

        // 3. УЛЬТИМАТИВНЫЙ СТАРТ FOREGROUND (Для Android 10/13 шлем 2 параметра!)
        startForeground(101, builder.build());

        // 4. ПОДЖИГАЕМ ЧИСТЫЙ LINUX-ПОТОК PYTHON
        new Thread(new Runnable() {
            @Override
            public void run() {
                // Вызываем нативный системный запуск нашего файла service_motor.py
                try {
                    String[] cmd = {"python3", getFilesDir().getAbsolutePath() + "/service_motor.py"};
                    Runtime.getRuntime().exec(cmd).waitFor();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        // ЖЕСТКИЙ ЗАЖИМ: Возвращаем START_STICKY на чистом Java! 
        // Теперь служба БУДЕТ возрождаться из пепла, игнорируя Kivy!
        return START_STICKY; 
    }

    @Override
    public IBinder onBind(Intent intent) { return null; }
}
#==≈============

#--------‐‐-----
MT Manager или APK Editor
p4a.hook = hook.py
# hook.py — ОЛДСКУЛЬНЫЙ ИНЖЕКТОР ПАСПОРТА СЛУЖБЫ (100% РАБОЧИЙ ВАРИАНТ)
from pathlib import Path
from pythonforandroid.toolchain import ToolchainCL

def after_apk_build(toolchain: ToolchainCL):
    print("=== [HOOK] СТАРТ ПЕРЕХВАТА МАНИФЕСТА ===")
    
    # ЭТАЛОННЫЙ ПУТЬ К МАНИФЕСТУ ВНУТРИ СЕРВЕРА ACTIONS (По чертежам Kivy)
    manifest_file = Path(toolchain._dist.dist_dir) / "src" / "main" / "AndroidManifest.xml"
    
    if not manifest_file.exists():
        print(f"=== [HOOK] КРИТИЧЕСКАЯ ОШИБКА: Манифест не найден по пути: {manifest_file} ===")
        return

    # Читаем манифест как обычный текст
    text = manifest_file.read_text(encoding="utf-8")
    
    # ВНИМАНИЕ: Наш точный поисковый маркер Java-класса службы!
    # Замените 'org.oldschool.digmarecorder' строго на ваш package.domain + package.name из spec!
    target = 'android:name="org.oldschool.digmarecorder.ServiceDigmaservice"'
    
    # Ищем, в каком месте текста притаилась наша служба
    pos = text.find(target)
    if pos != -1:
        # Находим закрывающий тег этой службы "/>"
        end = text.find("/>", pos)
        
        # Хирургический укол: врезаем тип dataSync прямо перед закрытием тега!
        text = (text[:end] + ' android:foregroundServiceType="dataSync"' + text[end:])
        
        # Перезаписываем готовый измененный файл обратно на диск сервера
        manifest_file.write_text(text, encoding="utf-8")
        print("=== [HOOK] УСПЕХ! Атрибут foregroundServiceType добавлен в манифест! ===")
    else:
        print("=== [HOOK] ОШИБКА: Строка службы не найдена в тексте манифеста! ===")
