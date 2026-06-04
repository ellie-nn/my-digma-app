//package org.kivy.android; // СТРОГО РОДНОЙ ПАКЕТ KIVY!
package org.oldschool.digmarecorder; // СТРОГО ВАШ ДОМЕН ИЗ SPEC!

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Notification;

// Имя класса строго уникальное!
public class DigmaJavaService extends Service {
    @Override
    public void onCreate() {
        super.onCreate();
        
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                "digma_channel", "Digma Service", NotificationManager.IMPORTANCE_LOW
            );
            NotificationManager manager = getSystemService(NotificationManager.class);
            if (manager != null) manager.createNotificationChannel(channel);
        }
    
        // ЗАМЕНЯЕМ СТАРЫЙ КУСОК НА СИСТЕМНЫЙ ИКОНОЧНЫЙ ЯКОРЬ ANDROID
        // android.R.drawable.stat_sys_warning — это стандартный системный значок, 
        // который железно зашит в ядро Android и доступен в любую микросекунду!
        Notification.Builder builder = new Notification.Builder(this, "digma_channel")
            .setContentTitle("Digma Service")
            .setContentText("Фоновый мотор розетки работает...")
            //.setSmallIcon(getApplicationInfo().icon);
            .setSmallIcon(android.R.drawable.stat_sys_warning); // Чистый андроид-ресурс!

        startForeground(101, builder.build());

        new Thread(new Runnable() {
            @Override
            public void run() {
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
        return START_STICKY; 
    }

    @Override
    public IBinder onBind(Intent intent) { return null; }
}
