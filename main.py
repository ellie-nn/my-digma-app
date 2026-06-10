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
        selection = f"_display_name='{filename}' AND relative_path LIKE '%Documents%'"

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
            values.put("relative_path", "Documents/")
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
        
# ИМПОРТИРУЕМ ДАТЧИК ОКНА
class DigmaRecorderApp(App):
    def build(self):
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
        sys.stdout = MediaStoreStdout()
        sys.stderr = sys.stdout

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
        Clock.schedule_interval(self.update_screen, 5.0)
        
#        if platform == 'android':
  #          self.start_background_service()
 #       else:
  #          self.start_background_service()
        #import tinytuya    
        
        return self.label
        
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
            
        if data and 'dps' in data:
            dps = data['dps']
            
            # Извлекаем Ватты (19) и Счетчик кВт*ч (17)
            raw_vatt = dps.get('19', 0)
            vatt = raw_vatt / 10.0
            
            # Если 17-й параметр есть - берем его, если скрыт - пишем -1
            kwh_17 = dps.get('17', -1)
            
            current_time = time.strftime('%H:%M:%S')
            
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
