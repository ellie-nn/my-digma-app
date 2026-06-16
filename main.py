#import warnings
# ДАЕМ КОМАНДУ ПИТОНУ: ПОЛНОСТЬЮ ИГНОРИРОВАТЬ ЛЮБЫЕ ДЕКОРАТИВНЫЕ WARNINGS
#warnings.filterwarnings("ignore")


import logging  # ИМПОРТИРУЕМ МОДУЛЬ ЛОГОВ
# 2. ЖЕСТКИЙ ЗАЖИМ ДЛЯ ТИНИТУИ: отключаем логирование ошибок уровня CRITICAL и ниже!
logging.disable(logging.CRITICAL)

import tinytuya
#if 'tinytuya' in sys.modules:

import time
import os
#import signal
#import csv
import pyaes
import sys


from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform
#from android.storage import primary_external_storage_path

from kivy.core.window import Window

from jnius import autoclass #, cast

# === СПИСОК УДАЛЕННЫХ И НЕНУЖНЫХ МОДУЛЕЙ ===
# import csv           # Больше не нужен, пишем строки через Java-стрим напрямую [↑]
# import signal        # Удален, фоновый мотор гасится штатными средствами Android [↑]
# from jnius import cast # Лишний метод, для Java-моста достаточно только autoclass [↑]
# from android.storage import primary_external_storage_path # Путь заблокирован ядром Linux [↑]

# ОСТАВЛЯЕМ ЗДЕСЬ СТРОГО ДЛЯ ГРАФИКИ И СТАРТА:
#from kivy.app import App
#from kivy.uix.label import Label
#from kivy.clock import Clock          # Чтобы раз в секунду читать лог службы
#from kivy.utils import platform       # Проверка, что мы на Android, а не на ПК
#from kivy.core.window import Window   # Наш шедевральный датчик фокуса окон

# ПЕРЕНОСИМ СЮДА ДЛЯ ЧЕРНОВОЙ РАБОТЫ В ФОНЕ:
#import os                             # Для os.getcwd() или системных проверок
#import sys                            # Для sys.stdout/sys.stderr и перехвата print()
#from jnius import autoclass           # Наш ультимативный мост к Java-базе MediaStore

#from plyer import notification
#notification.notify(title="Digma Recorder", message="Самописец успешно запущен!", timeout=3)

DEVICE_ID = 'bf1a864dc80b65d878lv65'
LOCAL_KEY = 'X@o=_T>sgCfWGeEz'
FILE_CSV = 'power_history.csv'
#SUB_DIR = "digma/" if os.android.get('ANDROID_ARGUMENT','')=='digmarecorderok' else ''
SUB_DIR = ''

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
# Импортируем легальный Kivy-движок для графиков
from kivy_garden.graph import Graph, LinePlot

# Точный путь к файлу данных нашего бессмертного 12-го релиза
#LOG_PATH = 'Documents/'+SUB_DIR+'servicework.txt'
#LOG_PATH = "/Documents/servicework.txt"
LOG_PATH = "/storage/emulated/0/Documents/"

def append_to_public_documents(filename, text_content):
    try:
        Context = autoclass('org.kivy.android.PythonActivity').mActivity
        ContentValues = autoclass('android.content.ContentValues')
        MediaStoreFiles = autoclass('android.provider.MediaStore$Files')
        resolver = Context.getContentResolver()
        collection_uri = MediaStoreFiles.getContentUri("external")
        
        #print(f'Collection\n{collection_uri}\n')
        # 1. ОЛДСКУЛЬНЫЙ ИНСПЕКТОР БАЗЫ ДАННЫХ (Ищем старый файл по имени)
        # Составляем SQL-запрос к Android: имя файла и папка Documents
        #selection = f"_display_name='{filename}' AND relative_path='Documents/'"
        # Ищем файл по имени, а папку — по маске "содержит слово Documents"
        relpath = "Documents/"+SUB_DIR
        selection = f"_display_name='{filename}' AND relative_path LIKE '%Documents/"+SUB_DIR+"%'"

        cursor = resolver.query(collection_uri, ["_id"], selection, None, None)
        #print(f'Cursor\n{cursortostring(Cursor)}\n{cursor.moveToFirst()}\n')
        if cursor and cursor.moveToFirst():
            # ФАЙЛ НАЙДЕН в базе! Достаем его уникальный числовой ID
            file_id = cursor.getLong(cursor.getColumnIndex("_id"))
            ContentUris = autoclass('android.content.ContentUris')
            # Превращаем ID в ту самую старую, живую ссылку Uri
            file_uri = ContentUris.withAppendedId(collection_uri, file_id)
            cursor.close()
        else:
            # ФАЙЛА ЕЩЕ НЕТ — регистрируем новую строку в Documents/
            if cursor: cursor.close()
            values = ContentValues()
            values.put("_display_name", filename)
            #values.put("mime_type", "text/plain")
            values.put("mime_type", "application/octet-stream")
            values.put("relative_path", "Documents/"+SUB_DIR)
            file_uri = resolver.insert(collection_uri, values)
        
        # 2. ОТКРЫВАЕМ СИСТЕМНЫЙ СТРИМ В РЕЖИМЕ СТРОГОЙ ДОЗАПИСИ "wa"
        output_stream = resolver.openOutputStream(file_uri, "wa")
        output_stream.write(bytes(text_content + "\n", 'utf-8'))
        output_stream.close()
        
    except Exception as e:
        # Если тестируем на ПК в Pydroid — пишем обычным Си-методом дозаписи
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(text_content + "\n")
        

# СТРОИМ КЛАСС-ПЕРЕХВАТЧИК
class MediaStoreStdout:
    def write(self, message):
        # Если прилетает не пустая строка — отправляем её в наш Java-мост
        if message and message.strip():
            # Вызываем вашу отлаженную функцию дозаписи в Documents!
            append_to_public_documents("app_log.txt", message.strip())
    def flush(self):
        pass  # Системная заглушка, обязательная для потоков stdout
    
if True:
    def build_voltage_graph(file_path):
        #"""
        #ФУНКЦИЯ-ПРОЖЕКТОР: Читает файл, собирает вольтаж и строит график.
        #"""
        graph = Graph(
            xlabel='Время', ylabel='Вольты',
            x_ticks_minor=1, x_ticks_major=5,
            y_ticks_minor=5, y_ticks_major=10,
            y_grid_label=True, x_grid_label=True,
            padding=10, x_grid=True, y_grid=True,
            xmin=0, xmax=20,  
            ymin=0, ymax=300
        )

        plot = LinePlot(color=[0, 0.6, 1, 1], line_width=2.5)
        points = []
        #import os

# Родной андроидный хак для новичков:
# На Android 10 переменная 'EXTERNAL_STORAGE' всегда намертво знает 
# правильный абсолютный путь к вашей внутренней памяти (уже со всеми нужными слэшами!)
        base_dir = os.environ.get('EXTERNAL_STORAGE', '/storage/emulated/0')

# Собираем путь в лоб, без ручных слэшей
        file_path = os.path.join(base_dir, 'Documents', 'work.txt')
        with open(file_path, "w", encoding="utf-8", errors="ignore") as f:
            tmpl='10 20 30 40'
            f.write((tmpl+'\n')*3+tmpl)
            f.flush
        file_path = os.path.join(base_dir, 'Documents', 'servicework.txt')
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    x_index = 0
                    for line in f:
                        if True:
                            try:
                                # Хирургический вырез значения вольтажа из строки лога
                                voltage_value = float(line.split()[2])
                                points.append((x_index, voltage_value))
                                x_index += 1
                            except Exception:
                                continue
                if len(points) > 20:
                    graph.xmax = len(points)
            except Exception as e:
                print(f"[ERR] Ошибка чтения файла1: {e}")
                for i in range(1, 11):
                    voltage_value = i
                    x_index = i
                    points.append((x_index, voltage_value))
        else:
            print(f"[ERR] Ошибка чтения файла2")
            for i in range(1, 11):
                voltage_value = i
                x_index = i
                points.append((x_index, voltage_value))
            points = [(0, 120), (20, 220)]
        
        # Заглушка, если мотор еще не успел создать файл на чистой установке
        if not points:
            points = [(0, 120), (20, 220)]

        plot.points = points
        graph.add_plot(plot)
        return graph

    def clear_log_file(instance):
        return
        
    def g_init():
        # ГЛАВНЫЙ КОНТЕЙНЕР: Свободный слой на всё окно [↑]
        main_layout = FloatLayout()
        
        # ========================================================
        # СЛОЙ 1 (НИЖНИЙ): НАШ ГРАФИК РАСТЯНУТ НА 100% ЭКРАНА [↑]
        # ========================================================
        graph_widget = build_voltage_graph(LOG_PATH)
        # Занимает 100% ширины и 100% высоты окна [↑]
        graph_widget.size_hint = (1.0, 1.0) 
        graph_widget.pos_hint = {'x': 0, 'y': 0}
        main_layout.add_widget(graph_widget)
        
        # ========================================================
        # СЛОЙ 2 (ВЕРХНИЙ): ПОЛУПРОЗРАЧНАЯ ШАПКА ПОВЕРХ СЕТКИ [↑]
        # ========================================================
        status_label = Label(
            text="Digma R12: Мониторинг сети",
            size_hint=(0.6, 0.08),            # 60% ширины экрана, 8% высоты [↑]
            pos_hint={'x': 0.2, 'y': 0.9},     # Центрируем сверху (отступ 20% слева, 90% вверх) [↑]
            color=[1, 1, 1, 0.8],             # Белый цвет с легкой прозрачностью 80%
            font_size=16
        )
        main_layout.add_widget(status_label)
        
        # ========================================================
        # СЛОЙ 3 (ВЕРХНИЙ): КНОПКА ОЧИСТКИ ПОВЕРХ ГРАФИКА ВНИЗУ [↑]
        # ========================================================
        btn_clear = Button(
            text="Очистить лог розетки",
            size_hint=(0.5, 0.08),            # 50% ширины экрана, 8% высоты [↑]
            pos_hint={'x': 0.25, 'y': 0.05},   # Центрируем внизу (отступ 25% слева, 5% вверх) [↑]
            background_color=[1, 0, 0.2, 0.7] # Красный полупрозрачный оттенок кнопок старой школы
        )
        # Привязываем кнопку к нашей будущей функции очистки файла [↑]
        btn_clear.bind(on_release=clear_log_file)
        main_layout.add_widget(btn_clear)
        
        return main_layout
          
    
# ИМПОРТИРУЕМ ДАТЧИК ОКНА
class DigmaRecorderApp(App):
    def build(self):
        sys.stdout = MediaStoreStdout()
        sys.stderr = sys.stdout
        print('START')
        #try:
        self.mywin = g_init()
        time.sleep(10.0)
        #except: pass
        # Создаем на экране большую текстовую панель
        self.label = Label(
            text="Инициализация Python ядра...\nОжидайте.", 
            font_size='18sp',
            halign='center',
            valign='top'
        )
        self.label.bind(size=self.label.setter('text_size'))
        
        # === ТЕСТОВЫЙ ВИБРО-ПИНОК СТАРТА СЛУЖБЫ ===
      #  try:
    #        Context = autoclass('org.kivy.android.PythonActivity').mActivity
      #      vibrator = Context.getSystemService(Context.VIBRATOR_SERVICE)
       #     vibrator.vibrate(2000)
      #  except Exception as vib_err:
      #      print(f"Ошибка вибромотора: {vib_err}")
        # ==========================================
           
        try:
            # мост к Java-службам Android
            from android import AndroidService
                
            # Создаем службу. Имя должно СТРОГО совпадать с тем, что в buildozer.spec!
            service = AndroidService('digmaservice', 'fore ground')
                
            # Запускаем файл service.py в изолированном потоке памяти
            service.start('service')
            self.ttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ ПАШЕТ!\n'
        
        except Exception as e:
            self.ttext = f"Ошибка запуска службы: {e}"
                        
        #return label
        
        self.vatt_sum = 0
        self.tttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ TTT!\n'
        # ПРОИЗВОДИМ ПОДМЕНУ В ЯДРЕ PYTHON
       
        try:
            devices = tinytuya.deviceScan(None,10)
            ip_address = [ip for ip, info in devices.items() if info.get('gwId') == DEVICE_ID][0]
            print(f'Ip found: {ip_address}')
        except Exception as e:
            print(f'Can''t find ip\n{e}\nDevices={devices}\n')
            #raise SysExit
        try:               
            self.rosette = tinytuya.OutletDevice(DEVICE_ID, ip_address, LOCAL_KEY)
            self.rosette.set_version(3.3)
            self.rosette.set_socketTimeout(2)
            self.rosette.updatedps()
            time.sleep(0.1)
        
        except Exception as e:
            print(f'First interaction error:\n{e}')
            #raise SysExit
    
        self.text = f'СИСТЕМА СТАРОЙ ШКОЛЫ Ψ!\n'
        #self.ttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ tt!\n'
        self.last_time = time.time()
        self.vatt_sum = 0
        #Запускаем секундный таймер Kivy для вывода отчетов на экран
        Clock.schedule_interval(self.update_screen, 1.0)
        
#        if platform == 'android':
  #          self.start_background_service()
 #       else:
  #          self.start_background_service()
        #import tinytuya    
        
        return self.mywin
        
    def check_permissions_callback(self, permissions, grants):
        # Эта функция сама автоматически сработает, когда вы нажмете "Разрешить" на экране!
        if all(grants):
            self.label.text = "Права получены! Поджигаем фитиль..."
            try:
                from android import AndroidService
                service = AndroidService('digmaservice', 'Служба работает в фоне...')
                service.start('service.py')
                self.ttext = "СЛУЖБА ЗАПУЩЕНА!\nПроверяйте шторку телефона."
            except Exception as e:
                self.ttext = f" Ошибка старта: {e}"
        else:
            self.ttext = " Вы отказали в правах. Служба заблокирована системой!"
        return   
    def start_background_service(self):
        print('!!! -PROGRAM LUNCHED- !!!')
        
        try:
            self.tttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ НЕсбоит!\n{e}'
        except Exception as e:
            self.tttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ сбоит!\n{e}'
                
    def update_screen(self, dt):
        #current_time = time.strftime('%H:%M:%S')
        
        
        # Забираем свежий статус
        data = False
        try:
            data = self.rosette.status()
        except:
            print('line 219, probably no self.rosette')
        time_ = time.time()
        print('!!! PROGRAM LUNCHED !!!')
        printout = f"{time.strftime('%H:%M:%S')}"
        current_time = time.strftime('%H:%M:%S')    
        if data and 'dps' in data:
            dps = data['dps']
            
            # Извлекаем Ватты (19) и Счетчик кВт*ч (17)
            raw_vatt = dps.get('19', 0)
            vatt = raw_vatt / 10.0
            
            # Если 17-й параметр есть - берем его, если скрыт - пишем -1
            kwh_17 = dps.get('17', -1)
            
            self.vatt_sum += vatt*(time_-self.last_time)
            self.last_time = time_
            printout = f"{time.strftime('%H:%M:%S')} {vatt} {self.vatt_sum/3600:.3f} {kwh_17}"
            append_to_public_documents('digmaspy.log',printout)
        else:
            printout = f"{time.strftime('%H:%M:%S')}"
        
        self.tttext = printout
        # Каждую секунду выводим на экран доказательство, что Python ЖИВ
        self.label.text = f"{self.tttext}\n{self.ttext}\nТекущее время: {current_time}\n\nОкно открыто и держит фокус."
        if data:
            self.rosette.updatedps()
        time.sleep(0.1)
            
if __name__ == '__main__':
    DigmaRecorderApp().run()
