import time
import os
import signal
import sys

from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform
from android.storage import primary_external_storage_path

from kivy.core.window import Window

from jnius import autoclass, cast

# СТРОИМ КЛАСС-ПЕРЕХВАТЧИК
class MediaStoreStdout:
    def write(self, message):
        # Если прилетает не пустая строка — отправляем её в наш Java-мост
        if message and message.strip():
            # Вызываем вашу отлаженную функцию дозаписи в Documents!
            append_to_public_documents("app_log.txt", message.strip())
            
    def flush(self):
        pass  # Системная заглушка, обязательная для потоков stdout

def append_to_public_documents(filename, text_content):
    # 1. Импортируем официальные Java-классы Android
    Context = autoclass('org.kivy.android.PythonActivity').mActivity
    ContentValues = autoclass('android.content.ContentValues')
    # К вложенным классам Android в pyjnius всегда обращаются через знак $ !
    MediaStoreFiles = autoclass('android.provider.MediaStore$Files')
    #MediaStore = autoclass('android.provider.MediaStore')
    Uri = autoclass('android.net.Uri')
    
    # 2. Создаем структуру параметров (ContentValues)
    values = ContentValues()
    values.put("_display_name", filename)        # Имя файла
    values.put("mime_type", "text/plain")         # Тип (текст)
    values.put("relative_path", "Documents/")     # Куда кладем [↑]
    
    # 3. Отправляем запрос в базу данных Android через ContentResolver
    resolver = Context.getContentResolver()
    collection_uri = MediaStoreFiles.getContentUri("external")
    file_uri = resolver.insert(collection_uri, values)
    
    # 4. Открываем системный Java-поток на запись по полученной ссылке
    output_stream = resolver.openOutputStream(file_uri)
    
    # 5. Превращаем наш Python-текст в байты и пишем напрямую в корень!
    output_stream.write(bytes(text_content, 'utf-8'))
    output_stream.close()
    
# ИМПОРТИРУЕМ ДАТЧИК ОКНА
class DigmaRecorderApp(App):
    def build(self):
        self.tttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ TTT!\n'
        # ПРОИЗВОДИМ ПОДМЕНУ В ЯДРЕ PYTHON
        sys.stdout = MediaStoreStdout()
        sys.stderr = sys.stdout

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
        
        if platform == 'android':
            self.start_background_service()
        else:
            self.start_background_service()
            
        return self.label

    def start_background_service(self):
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

                
