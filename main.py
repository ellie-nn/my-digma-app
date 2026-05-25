import time
import os
import signal
import sys

from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform
from android.storage import primary_external_storage_path
    #PUBLIC_DIR = os.path.join(base_path, 'Documents')


class DebugApp(App):
    def build(self):
        self.ttext = 'СИСТЕМА СТАРОЙ ШКОЛЫ ЖИВА!\n'
        
        # Создаем на экране большую текстовую панель
        self.label = Label(
            text="Инициализация Python ядра...\nОжидайте.", 
            font_size='18sp',
            halign='center'
        )
        
        if platform == 'android':
            try:
                # ВЫЗЫВАЕМ СТАНДАРТНОЕ ОКНО ЗАПРОСА ПРАВ НА ПАМЯТЬ
                from android.permissions import request_permissions, Permission
                request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
            except Exception as e:
                self.ttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ без разрешений!\n{e}'
        
        try:
            base_path = primary_external_storage_path()
            sys.stdout = open(base_path+'/app_log.txt', 'a', encoding='utf-8')
            self.tttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ НЕсбоит!\n{e}'
        
        except Exception as e:
            self.tttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ сбоит!\n{e}'
        #sys.stderr = sys.stdout  
        # Запускаем секундный таймер Kivy для вывода отчетов на экран
        Clock.schedule_interval(self.update_screen, 1.0)
        return self.label

    def update_screen(self, dt):
        current_time = time.strftime('%H:%M:%S')
        #time.sleep(1)
        try:
            print('!!! PROGRAM LUNCHED !!!')
            self.ttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ пишет!\n{e}'
        except:
            self.ttext = f"СИСТЕМА СТАРОЙ ШКОЛЫ ЛАЖАЕТ!\nТекущее время: {current_time}\n\nОкно открыто и держит фокус."
        # Каждую секунду выводим на экран доказательство, что Python ЖИВ
        self.label.text = f"{self.tttext}\n{self.ttext}\nТекущее время: {current_time}\n\nОкно открыто и держит фокус."
        
if __name__ == '__main__':
    DebugApp().run()
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

                
