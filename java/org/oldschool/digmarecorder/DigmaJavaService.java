package org.oldschool.digmarecorder;
import org.kivy.android.PythonService; // ДОБАВИТЬ ЭТУ СТРОКУ ИМПОРТА!

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.os.Vibrator;
//import android.os.Context;
import android.content.Context;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Notification;

//public class DigmaJavaService extends Service {
// Было: public class DigmaJavaService extends Service
// СТАНОВИТСЯ (Наследуем Kivy, чтобы Питон не падал при линковке!):
//public class DigmaJavaService extends PythonService {
// Теперь Kivy-ядро не сможет совершить суицид внутри нашей службы!
public class DigmaJavaService extends Service {
    
    // Вспомогательный метод для быстрой вибрации на чистом Java
    private void javaVibrate(int ms) {
        try {
            //Vibrator v = (Vibrator) getSystemService(Context.VIBRATOR_SERVICE);
            Vibrator v = (Vibrator) getSystemService(VIBRATOR_SERVICE);

            if (v != null) {
                v.vibrate(ms);
            }
        } catch (Exception e) {
            // Если даже вибратор не сработает — код пойдет дальше без вылетов
        }
    }

    @Override
    public void onCreate() {
        super.onCreate();
        
        // МАРКЕР 1: Служба родилась в памяти Android! (Один длинный гудок)
        javaVibrate(800);
        
        try {
            // 1. Создаем канал уведомлений
            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                NotificationChannel channel = new NotificationChannel(
                    "digma_channel", "Digma Service", NotificationManager.IMPORTANCE_LOW
                );
                NotificationManager manager = getSystemService(NotificationManager.class);
                if (manager != null) manager.createNotificationChannel(channel);
            }
            
            // МАРКЕР 2: Канал успешно зарегистрирован! (Два коротких пика)
            javaVibrate(150); try { Thread.sleep(200); } catch(Exception e){} javaVibrate(150);

            // 2. Строим уведомление бессмертия с системным значком
            Notification.Builder builder = new Notification.Builder(this, "digma_channel")
                .setContentTitle("Digma Service")
                .setContentText("Фоновый мотор работает...")
                .setSmallIcon(android.R.drawable.stat_sys_warning);

            // 3. Запускаем Foreground
            startForeground(101, builder.build());
            
            // МАРКЕР 3: Режим бессмертия успешно активирован! (Три коротких пика)
            javaVibrate(100); try { Thread.sleep(150); } catch(Exception e){}
            javaVibrate(100); try { Thread.sleep(150); } catch(Exception e){}
            javaVibrate(100);

        } catch (Exception err) {
            // ГЛУШИТЕЛЬ: Если споткнемся об уведомление — мы НЕ УПАДЕМ!
            // Мы сделаем один панический микро-пик и поедем запускать Питон
            javaVibrate(50);
        }

        // 4. Поднимаем наш чистый независимый Linux-поток Python
        try {
            new Thread(new Runnable() {
                @Override
                public void run() {
                    try {
                        // Финальный маркер перед прыжком в скрипт service_motor.py
                        javaVibrate(400);
                        
                        String[] cmd = {"python3", getFilesDir().getAbsolutePath() + "/service_motor.py"};
                        Runtime.getRuntime().exec(cmd).waitFor();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }).start();
        } catch (Exception thread_err) {
            javaVibrate(1000); // Тяжелый гудок, если поток не создался
        }
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        return START_STICKY; 
    }

    @Override
    public IBinder onBind(Intent intent) { return null; }
}
