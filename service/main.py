import logging  # ИМПОРТИРУЕМ МОДУЛЬ ЛОГОВ
# 2. ЖЕСТКИЙ ЗАЖИМ ДЛЯ ТИНИТУИ: отключаем логирование ошибок уровня CRITICAL и ниже!
logging.disable(logging.CRITICAL)

import time
import os                            # Для os.getcwd() или системных проверок
import sys       # Для sys.stdout/sys.stderr и перехвата print()
#from jnius import autoclass           # Наш ультимативный мост к Java-базе MediaStore

import tinytuya
#if 'tinytuya' in sys.modules:

import pyaes

from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform

from kivy.core.window import Window

FDATA_NAME = "servicework"+str(time.time()//60)+".txt"
FSVC_LOG = "srv_log"+str(time.time()//60)+".txt"
DEVICE_ID = "bf1a864dc80b65d878lv65"
LOCAL_KEY = "X@o=_T>sgCfWGeEz"
#SUB_DIR = "digma/" if os.android.get('ANDROID_ARGUMENT','')=='digmarecorderok' else ''
SUB_DIR=''

def append_to_public_documents(filename, text_content):
    from jnius import autoclass
    try:
        # ХИРУРГИЧЕСКИЙ ФИКС ДЛЯ СЛУЖБЫ:
        # Сначала пытаемся взять контекст фоновой службы, а если мы на ПК — берем окно
        try:
            Context = autoclass('org.kivy.android.PythonService').mService
        except:
            Context = autoclass('org.kivy.android.PythonActivity').mActivity
            
        ContentValues = autoclass('android.content.ContentValues')
        MediaStoreFiles = autoclass('android.provider.MediaStore$Files')
        resolver = Context.getContentResolver()
        collection_uri = MediaStoreFiles.getContentUri("external")
        
        # Ищем файл по имени, а папку — по маске "содержит слово Documents"
        selection = f"_display_name='{filename}' AND relative_path LIKE '%Documents/"+SUB_DIR+"%'"

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
            append_to_public_documents(FSVC_LOG, message.strip())
    def flush(self):
        pass  # Системная заглушка, обязательная для потоков stdout

class DigmaServiceEngine:
    def __init__(self):
        append_to_public_documents(FDATA_NAME,'№ Time Pow ΣPow HardPow)
        
        from jnius import autoclass
        self.count = 0
        self.ttext = 'ttext'
        sys.stdout = MediaStoreStdout()
        sys.stderr = sys.stdout
        
        print('srvstdoutstart')
        
        print('srvstdoutstart')
        if False:
        # === ТЕСТОВЫЙ ВИБРО-ПИНОК СТАРТА СЛУЖБЫ ===
            try:
            # 1. Достаем контекст живой фоновой службы Kivy
                Context = autoclass('org.kivy.android.PythonService').mService
            
            # 2. Вызываем официальную системную службу вибрации Android
                vibrator = Context.getSystemService(Context.VIBRATOR_SERVICE)
    
            # 3. Трясем телефон 2000 миллисекунд (2 секунды)
                vibrator.vibrate(500)
            except Exception as vib_err:
            # Если мы упали на старте — этот принт улетит в системный Logcat
                print(f"Ошибка вибромотора: {vib_err}")
        # ==========================================
        
        #append_to_public_documents(FDATA_NAME, 'start')
        # АКТИВИРУЕМ ТОТАЛЬНЫЙ ПЕРЕХВАТЧИК ОШИБОК СЛУЖБЫ В ФОНЕ
        
    
        try:
            devices = tinytuya.deviceScan(None,5)
            ip_address = [ip for ip, info in devices.items() if info.get('gwId') == DEVICE_ID][0]
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
        time.sleep(2.0)
        time.sleep(30.0)
        #print('stdouttestend')
        self.last_time = time.time()
        self.vatt_sum = 0
        while True:
            #append_to_public_documents(FDATA_NAME, 'loop')
            self.update_data()
            time.sleep(1.0)
        return

    def update_data(self):
        self.count +=1
        #current_time = time.strftime('%H:%M:%S')
        
        # Забираем свежий статус
        data = False
        try:
            data = self.rosette.status()
        except:
            print('line 140, probably no self.rosette')
        time_ = time.time()
        #print('!!! SERVICE LUNCHED !!!')
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
                
            printout = f".{self.count} {time.strftime('%H:%M:%S')} {vatt} {self.vatt_sum/3600:.3f} {kwh_17}"
        else:
            printout = f".{self.count} {time.strftime('%H:%M:%S')} -1 -1 -1"
        append_to_public_documents(FDATA_NAME,printout)
        
        self.tttext = printout
        # Каждую секунду выводим на экран доказательство, что Python ЖИВ
        #self.label.text = 
        #print(f"{self.tttext}\n{self.ttext}\nТекущее время: {current_time}\n\nОкно открыто и держит фокус.")
        if data:
            self.rosette.updatedps()
        return
if __name__ == '__main__':
    engine = DigmaServiceEngine()
    
#-----------

        
# НАШ БЕСКОНЕЧНЫЙ ФОНОВЫЙ ЦИКЛ
#while True:
    # --------------------------------------------------
    # ЗДЕСЬ ИДЕТ ЛЮБАЯ ВАША ФОНОВАЯ РАБОТА (Запись логов, сокеты, интегралы)
    # --------------------------------------------------
    # Железное правило: фоновый цикл ОБЯЗАН спать хотя бы секунду, 
    # чтобы не раскалять процессор телефона до 100% и не жрать батарею!
  #  time.sleep(1.0)
