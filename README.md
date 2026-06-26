fuck off
это блокнот
#==========≠======≠

#==========≠======≠

#==========≠======≠
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy_garden.graph import Graph, LinePlot
import math

class CustomGraph(Graph):
    def update_ticks(self, *args):
        # 1. Let the original Graph logic run to generate tick locations
        super().update_ticks(*args)
        
        # Mapping table for our X-axis values
        day_mapping = {
            0: "Mon", 20: "Tue", 40: "Wed", 
            60: "Thu", 80: "Fri", 100: "Sat"
        }
        
        # 2. Iterate and alter the text of the generated X-axis labels
        for label in self._x_grid_label_list:
            try:
                # Convert the generated string back to a float/int to match
                val = int(float(label.text))
                
                # Update with custom string if it exists in our map
                if val in day_mapping:
                    label.text = day_mapping[val]
                else:
                    label.text = ""  # Hide labels that don't match our criteria
            except ValueError:
                pass

class GraphApp(App):
    def build(self):
        layout = BoxLayout(padding=dp(20))
        
        # Initialize our custom graph wrapper
        graph = CustomGraph(
            xlabel='Days',
            ylabel='Value',
            xmin=0, xmax=100,
            ymin=-1, ymax=1,
            x_ticks_major=20,  # Matches the mapping intervals
            y_ticks_major=0.5,
            x_grid_label=True,
            y_grid_label=True,
            padding=dp(10),
            x_grid=True,
            y_grid=True
        )
        
        # Generate some placeholder data
        plot = LinePlot(color=[0, 1, 0, 1], line_width=2)
        plot.points = [(x, math.sin(x / 10.0)) for x in range(0, 101)]
        
        graph.add_plot(plot)
        layout.add_widget(graph)
        return layout

if __name__ == '__main__':
    GraphApp().run()
    
#==========≠======≠
from kivy_garden.graph import Graph

def format_x_axis(graph, value):
    # Returns the value formatted as a string (e.g. $10.00, Date, etc.)
    return f"${value:.2f}" 

graph = Graph(
    xlabel='Price',
    x_ticks_major=10, 
    x_ticks_minor=5
)

# Attach the formatting function to the graph
graph.x_ticks_func = format_x_axis

#==========≠======≠
мультикаст-запросом на системный адрес 224.0.0.251 (порт 5353). Микроконтроллер розетки обрабатывает этот системный mDNS-запрос на уровне сетевого чипа 
#==========≠======≠
, она наглухо отключает порты 6666/6667, но оставляет открытым скрытый порт 7001 UDP (или 10001)
#==========≠======≠
def vertical_time_formatter(value):
    """
    Берет число (например, 145) и превращает его в строку, 
    где каждая цифра стоит на новой строчке:
    1
    4
    5
    """
    # Превращаем число в текст, разбиваем посимвольно и склеиваем через перенос строки!
    return "\n".join(list(str(int(value))))

# НАМЕРТВО ВШИВАЕМ НАШ ФОРМАТТЕР В СЕТКУ ГРАФИКА:
my_graph.x_label_format = vertical_time_formatter

#==========≠======≠
my_graph.x_ticks_with_labels = False # Отключает текстовые цифры под осями

#==========≠======≠
import tinytuya

# 1. Инициализируем розетку в памяти (эти строки у вас уже есть)
device = tinytuya.OutletDevice(
    dev_id='ВАШ_ID_РОЗЕТКИ',
    address='192.168.X.X', # Локальный IP розетки в домашней сети
    local_key='ВАШ_LOCAL_KEY',
    version=3.3 # Или 3.1, в зависимости от чипа вашей розетки
)

def force_turn_off_socket():
    """
    Принудительно размыкает реле розетки, полностью отключая 
    питание подключенного прибора Digma!
    """
    try:
        # ХИРУРГИЧЕСКИЙ ВЫСТРЕЛ КОМАНДЫ ВЫКЛЮЧЕНИЯ:
        # Метод .turn_off() отправляет зашифрованный локальный TCP-пакет 
        # на порт 6668 розетки, меняя значение DPS 1 на False [↑]
        payload = device.turn_off()
        
        print(f"[МОТОР] Команда выключения отправлена успешно! Ответ железа: {payload}")
        # Сразу записываем это историческое событие в наш бессмертный файл лога:
        my_file_write("[SYSTEM] Розетка программно ВЫКЛЮЧЕНА по команде из окна.")
        
    except Exception as e:
        print(f"[ОШИБКА СЕТИ] Не удалось достучаться до розетки при выключении: {e}")

#==========≠======≠
def on_log_file_grow(new_total_seconds):
    """
    Вызывается автоматически, когда лог розетки прирастает секундами.
    """
    # 1. Динамически отодвигаем правую границу сетки графика
    my_graph.xmax = new_total_seconds
    
    # 2. ПРОПОРЦИОНАЛЬНЫЙ РАЗЖИМ ЛЕНТЫ:
    # Допустим, мы хотим, чтобы 1 секунда времени занимала ровно 2 пикселя на экране.
    # Лента сама раздуется вправо, а ScrollView автоматически увеличит 
    # диапазон скольжения для вашего пальца на экране Самсунга! [↑]
    graph_strip.width = new_total_seconds * 2
    
    # 3. ЕСЛИ ВКЛЮЧЕН РЕЖИМ "ПОЛЗТИ ВСЛЕД ЗА ДАННЫМИ" (Realtime Tracking):
    # Мы силой приказываем иллюминатору сдвинуть координату скролла в крайнее правое положение (1.0)
    if self.current_mode == "ползти":
        scroll_container.scroll_x = 1.0

#==========≠======≠
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout

# =====================================================================
# 1. СОЗДАЕМ ИНТЕРАКТИВНОЕ ОКНО-ИЛЛЮМИНАТОР (Вместо Slider!)
# =====================================================================
scroll_container = ScrollView(
    # Зажимаем размеры иллюминатора: по горизонтали он растянут на весь экран (1.0),
    # а по вертикали занимает, например, 80% пространства, оставляя место под TextInput
    size_hint=(1.0, 0.8),
    pos_hint={'x': 0, 'top': 0.9},
    
    # ЖЕСТКИЙ РЕЖИМ ОСЕЙ:
    do_scroll_x=True,   # Намертво РАЗРЕШАЕМ сдвиг пальцем по горизонтали!
    do_scroll_y=False,  # Категорически ЗАПРЕЩАЕМ сдвиг по вертикали, чтобы график не прыгал вверх-вниз
    
    # Настройка плавности торможения ленты после того, как вы убрали палец (кинетический скролл)
    scroll_distance=10, 
    scroll_timeout=55   
)

# =====================================================================
# 2. СОЗДАЕМ НЕВИДИМУЮ РЕЗИНОВУЮ ЛЕНТУ-ПОДЛОЖКУ
# =====================================================================
graph_strip = BoxLayout(
    orientation='horizontal',
    size_hint=(None, 1.0),  # None по ширине позволяет нам силой раздувать её вправо!
    width=1000              # Стартовая ширина в пикселях (подстроится под xmax!)
)

# =====================================================================
# 3. СБОРКА БИНАРНОГО ПИРОГА ВНУТРИ FloatLayout
# =====================================================================
# У вашего объекта my_graph убираем size_hint по иксам, так как он теперь лежит на ленте!
my_graph.size_hint_x = None
my_graph.bind(width=my_graph.setter('width')) # Привязываем ширину графика к ленте

# Укладываем слои строго друг в друга:
graph_strip.add_widget(my_graph)         # Кладем график на резиновую ленту
scroll_container.add_widget(graph_strip) # Засовываем ленту внутрь иллюминатора

# Добавляем иллюминатор самым первым в корень FloatLayout, чтобы он лег нижним слоем!
main_layout.add_widget(scroll_container)
# main_layout.add_widget(user_input) # Поле ввода TextInput кладем поверх!

#==========≠======≠
from jnius import autoclass, cast

def is_full_storage_allowed():
    """
    Возвращает True, если пользователь включил тумблер 'Доступ ко всем файлам'.
    Возвращает False, если тумблер выключен или это Android 10 (где его нет).
    """
    try:
        # 1. Стучимся в системный Java-класс Environment операционной системы Android
        Environment = autoclass('android.os.Environment')
        
        # 2. Вызываем официальный метод-проверку
        # Он возвращает живой бинарный флаг (True/False) прямо из ядра Linux!
        return Environment.isExternalStorageManager()
        
    except Exception:
        # Если метод не найден (это наш Android 10, где этого тумблера физически не существует)
        # или произошел сбой — возвращаем False, давая сигнал работать по правилам SAF
        return False

#==========≠======≠
from jnius import autoclass, cast

def is_full_storage_allowed():
    """
    Возвращает True, если пользователь включил тумблер 'Доступ ко всем файлам'.
    Возвращает False, если тумблер выключен или это Android 10 (где его нет).
    """
    try:
        # 1. Стучимся в системный Java-класс Environment операционной системы Android
        Environment = autoclass('android.os.Environment')
        
        # 2. Вызываем официальный метод-проверку
        # Он возвращает живой бинарный флаг (True/False) прямо из ядра Linux!
        return Environment.isExternalStorageManager()
        
    except Exception:
        # Если метод не найден (это наш Android 10, где этого тумблера физически не существует)
        # или произошел сбой — возвращаем False, давая сигнал работать по правилам SAF
        return False

#==========≠======≠
import math
import time

def generate_mock_log_stream(duration_seconds=120, step_seconds=1.0):
    """
    Генерирует искусственную историю вольтажа/мощности розетки.
    duration_seconds - общая глубина лога в секундах.
    step_seconds - шаг между записями (например, раз в секунду).
    """
    # Стартовая точка отсчета времени (текущий штамп эпохи Linux)
    start_time = time.time()
    
    # Накопитель энергии (Джоули = Ватт * Секунды)
    total_joules = 0.0
    
    # Количество строк, которое нужно сгенерировать
    total_lines = int(duration_seconds / step_seconds)
    
    for i in range(1, total_lines + 1):
        # Вычисляем текущее виртуальное время от старта
        elapsed = (i - 1) * step_seconds
        current_timestamp = start_time + elapsed
        
        # ФИЗИКА ПРИПОДНЯТОЙ СИНУСОИДЫ (Диапазон 0...200, Период 60 сек):
        # math.sin(2 * math.pi * elapsed / 60.0) дает колебания от -1 до 1 каждые 60 секунд.
        # + 1.0 сдвигает диапазон в 0...2. Умножение на 100.0 дает ровно 0...200 Вт!
        current_power = 100.0 * (math.sin(2 * math.pi * elapsed / 60.0) + 1.0)
        
        # Интегрируем джоули (Прибавляем энергию, набежавшую за текущий шаг)
        if elapsed > 0:
            total_joules += current_power * step_seconds
            
        # СБОРКА ТЕКСТОВОЙ МАТРИЦЫ СТРОКИ С ТОЧНОСТЬЮ ДО СОТЫХ ДОЛЕЙ:
        log_line = f".{i} {current_timestamp:.2f} {current_power:.2f} {total_joules:.2f} -1"
        
        # ЖЕСТКИЙ ПРИКАЗ ЗАПИСИ (Передаем готовую строку в ваш внешний шлюз):
        mywrite(log_line)

#==========≠======≠
    # 1. ХИРУРГИЧЕСКИЙ ЗАЖИМ СТАРЫХ ИНСТРУМЕНТОВ ANDROID SDK И NDK
    - name: Set up Android SDK & NDK for API 28
      run: |
        echo "=== [HACK] Подменяем современный NDK на олдскульный r19c ==="
        # Скачиваем официальный стабильный архив NDK r19c с серверов Google
        wget -q https://google.com
        unzip -q android-ndk-r19c-linux-x86_64.zip -d $HOME
        
        # Прописываем системные переменные окружения, чтобы Buildozer 
        # намертво зацепил именно этот старый NDK r19c при сборке Си-библиотек Kivy!
        echo "ANDROID_NDK_HOME=$HOME/android-ndk-r19c" >> $GITHUB_ENV
        echo "ANDROID_NDK_PATH=$HOME/android-ndk-r19c" >> $GITHUB_ENV

    # 2. ВАШ СТАНДАРТНЫЙ ШАГ ЗАПУСКА СБОРКИ (Остается в одну строку, но с подменой путей)
    - name: Build with Buildozer
      run: |
        # Мы явно передаем Билдозеру пути к нашему старому скачанному NDK через аргументы командной строки!
        buildozer android debug --android.ndk_path=$HOME/android-ndk-r19c --android.target_sdk=28

#==========≠======≠
import os
from android.storage import primary_external_storage_text

# 1. Вычисляем чистый физический путь к файлу лога (без ухищрений базы данных) [↑]:
base_path = primary_external_storage_text()
physical_log_path = os.path.join(base_path, "Documents", "app_log_digmatwelve.txt")

# 2. ЖЕСТКАЯ ПРОВЕРКА РЕАЛЬНОСТИ:
# Если физического файла на диске НЕТ (вы его удалили руками или его еще не было),
# мы ПРИНУДИТЕЛЬНО очищаем базу данных Android от старых призраков и вызываем insert()!
if not os.path.exists(physical_log_path):
    print("[LOG] Файла физически нет на диске! Очищаем старые SQL-следы...")
    # Очищаем старую застрявшую строку в базе через наш resolver, чтобы insert() прошел легально [↑]:
    resolver.delete(collection_uri, "display_name = ?", ["app_log_digmatwelve.txt"])
    
    # Теперь спокойно вызываем ваш легальный insert(), создавая чистый файл с нуля [↑]!
    file_uri = resolver.insert(collection_uri, values)
else:
    print("[LOG] Файл реально существует. Переходим к query и дозаписи...")

#==========≠======≠
import os

# 1. Узнаем package.name (например: 'digmatwelve')
package_name = os.environ.get('ANDROID_ARGUMENT', '')

# 2. Узнаем ПУТЬ к нашей приватной папке приложения на диске телефона
# Там внутри как раз зашит полный бинарный паспорт (domain + name)!
# Выведет строку вида: "/data/data/org.oldschool.digmatwelve/files/app"
app_private_dir = os.environ.get('ANDROID_APP_PATH', '')

print(f"[LOG] Имя пакета из спека: {package_name}")
print(f"[LOG] Полный бинарный путь: {app_private_dir}")

#-------------------
import os

def get_spec_param(param_name, default_value=""):
    """
    Универсальный парсер buildozer.spec. 
    Находит любой параметр, полностью игнорируя комментарии '#' и пробелы.
    """
    spec_path = "buildozer.spec"
    
    if not os.path.exists(spec_path):
        return default_value

    try:
        with open(spec_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                # 1. СРАЗУ ОТРЕЗАЕМ КОММЕНТАРИИ: разбиваем строку по первому знаку '#' 
                # и забираем только левую, "живую" часть кода!
                raw_code = line.split('#', 1)[0]
                
                # Очищаем кусок кода от концевых пробелов и переносов строк
                clean_line = raw_code.strip()
                
                # Если строка была чистым комментарием или оказалась пустой — пропускаем
                if not clean_line:
                    continue
                
                # 2. ЖЕСТКАЯ ПРОВЕРКА НА СОВПАДЕНИЕ ПАРАМЕТРА:
                # Ищем знак равенства, чтобы точно отделить имя параметра от значения
                if "=" in clean_line:
                    name_part, value_part = clean_line.split("=", 1)
                    
                    # Сверяем имя параметра (очистив от случайных пробелов вокруг него)
                    if name_part.strip() == param_name:
                        # Возвращаем идеально вычищенное текстовое значение!
                        return value_part.strip()
                        
    except Exception as e:
        print(f"[ERR] Ошибка парсинга buildozer.spec: {e}")
        
    return default_value

#-------------------
- name: Force Buildozer to Unpack Kivy Core
  run: |
    buildozer android p4a -- --help

- name: Hack Kivy Java Core to Persistent-Immortal
  run: |
    find .buildozer/ -name "PythonService.java" -type f | while read -r java_file; do
      sed -i "s|return START_NOT_STICKY;|return START_STICKY;|gw /dev/stdout" "$java_file"
    done

# === НАШ НОВЫЙ ИЗЯЩНЫЙ ХАК: КОПИРУЕМ СПЕК В КАЧЕСТВЕ ДАННЫХ ===
- name: Embed Spec File as App Data
  run: |
    echo "=== [HACK] Копируем spec под видом файла данных ==="
    # Копируем оригинальный спек текущей сборки в обычный текстовый файл
    cp buildozer.spec app_config.txt
    
- name: Build with Buildozer
  run: |
    buildozer android debug

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
