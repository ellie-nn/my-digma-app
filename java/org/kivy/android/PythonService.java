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
