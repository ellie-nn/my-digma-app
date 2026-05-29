#import warnings
# ДАЕМ КОМАНДУ ПИТОНУ: ПОЛНОСТЬЮ ИГНОРИРОВАТЬ ЛЮБЫЕ ДЕКОРАТИВНЫЕ WARNINGS
#warnings.filterwarnings("ignore")

import tinytuya
import time
import os
import signal
import csv
import pyaes
#import tinytuya
import sys

#if 'tinytuya' in sys.modules:

from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform
from android.storage import primary_external_storage_path

from kivy.core.window import Window

from jnius import autoclass, cast

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
        
        # 1. ОЛДСКУЛЬНЫЙ ИНСПЕКТОР БАЗЫ ДАННЫХ (Ищем старый файл по имени)
        # Составляем SQL-запрос к Android: имя файла и папка Documents
        selection = f"_display_name='{filename}' AND relative_path='Documents/'"
        cursor = resolver.query(collection_uri, ["_id"], selection, None, None)
        
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
        self.tttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ TTT!\n'
        # ПРОИЗВОДИМ ПОДМЕНУ В ЯДРЕ PYTHON
        sys.stdout = MediaStoreStdout()
        sys.stderr = sys.stdout
        
        devices = tinytuya.deviceScan(None,5)
        print('devices')
        print(devices)
        ip_address = [ip for ip, info in devices.items() if info.get('gwId') == DEVICE_ID][0]
                        
        self.rosette = tinytuya.OutletDevice(DEVICE_ID, ip_address, LOCAL_KEY)
        self.rosette.set_version(3.3)
        self.rosette.set_socketTimeout(2)
        
        #import tinytuya
        try:
            append_to_public_documents('testautoclass.txt','test1')
            append_to_public_documents('testautoclass.txt','test2')
    
        except Exception as e:
            self.tttext = f'autoclass error!\n{e}'
           
        # Создаем на экране большую текстовую панель
        self.label = Label(
            text="Инициализация Python ядра...\nОжидайте.", 
            font_size='18sp',
            halign='center',
            valign='top'
        )
        self.label.bind(size=self.label.setter('text_size'))
        self.text = f'СИСТЕМА СТАРОЙ ШКОЛЫ Ψ!\n'
        self.ttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ tt!\n'
        
        #Запускаем секундный таймер Kivy для вывода отчетов на экран
        Clock.schedule_interval(self.update_screen, 1.0)
        
#        if platform == 'android':
  #          self.start_background_service()
 #       else:
  #          self.start_background_service()
        #import tinytuya    
        return self.label

    def start_background_service(self):
        print('!!! PROGRAM LUNCHED !!!')
        
        try:
            self.tttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ НЕсбоит!\n{e}'
        except Exception as e:
            self.tttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ сбоит!\n{e}'
                
    def update_screen(self, dt):
        current_time = time.strftime('%H:%M:%S')
        #time.sleep(1)
        try:
            append_to_public_documents('digmaspy.log',f"[{time.strftime('%H:%M:%S')}]")
            
            #print('!!! PROGRAM LUNCHED !!!')
            self.ttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ пишет!\n{e}'
        except:
            self.ttext = f"СИСТЕМА СТАРОЙ ШКОЛЫ ЛАЖАЕТ!\nТекущее время: {current_time}\n\nОкно открыто и держит фокус."
        # Каждую секунду выводим на экран доказательство, что Python ЖИВ
        self.label.text = f"{self.tttext}\n{self.ttext}\nТекущее время: {current_time}\n\nОкно открыто и держит фокус."
        
        self.rosette.updatedps()
        time.sleep(0.1)  # Крошечная пауза, чтобы розетка успела ответить
        
        # Забираем свежий статус
        data = self.rosette.status()
        
        if data and 'dps' in data:
            dps = data['dps']
            
            # Извлекаем Ватты (19) и Счетчик кВт*ч (17)
            raw_vatt = dps.get('19', 0)
            vatt = raw_vatt / 10.0
            
            # Если 17-й параметр есть - берем его, если скрыт - пишем -1
            kwh_17 = dps.get('17', -1)
            
            current_time = time.strftime('%H:%M:%S')
        self.tttext = f'[{current_time}] {vatt} {kwh_17}\n'
            
        
if __name__ == '__main__':
    DigmaRecorderApp().run()
#-----_---

#---------_---
  #              # ЗАПУСКАЕМ НАШ СКРЫТЫЙ СЕРВИС СЕКУНДНОГО САМОПИСЦА
   #    #         from android import AndroidService
    #            service = AndroidService('DigmaService', 'Идет сбор данных розетки...')
       #         service.start('service.py')
      #      except Exception as e:
    #            pass
            
      #  return Label(
      #      text="⚙️ БОРТОВОЙ САМОПИСЕЦ DIGMA\nМотор запущен в фоне! 🚀\n\nИстория пишется напрямую в Documents!", 
     #       font_size='16sp',
    #        halign='center'
     #   )

                
