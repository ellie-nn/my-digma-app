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
