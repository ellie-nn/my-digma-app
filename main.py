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
#from kivy.utils import platform

# НАШ СКОПИПАЩЕННЫЙ КОРРЕКТНЫЙ ИНСТРУМЕНТ ПРОВЕРКИ КНОПКИ "ЗАПРЕТИТЬ"
def should_show_rationale(permission_string):
    tmp = 'mystring0'
    if platform == 'android':
        try:
            # Вызываем низкоуровневый Java-класс активности нашего приложения
            from jnius import autoclass
            
            try:
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                try:
                    current_activity = PythonActivity.mActivity
                except:
                    tmp = 'mystring1'
            except:
                tmp = 'mystring2'
            
            # Напрямую дергаем родной метод ядра Android, который Kivy забыли импортировать
            return current_activity.shouldShowRequestPermissionRationale(permission_string)
        except Exception as e:
            tmp = 'mystring3'
            #print(f"Ошибка низкоуровневого вызова Java: {e}")
 #   return False 
    else:
        tmp = 'mystring4'
    return tmp
 
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
            # ВЫЗЫВАЕМ СТАНДАРТНОЕ ОКНО ЗАПРОСА ПРАВ НА ПАМЯТЬ
            from android.permissions import request_permissions, Permission
#request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
            Clock.schedule_interval(self.check_permissions_loop, 1.0)
            # Запускаем секундный таймер Kivy для вывода отчетов на экран
        self.text = f'СИСТЕМА СТАРОЙ ШКОЛЫ Ψ!\n'
        self.ttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ tt!\n'
        self.tttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ TTT!\n'
                        
        Clock.schedule_interval(self.update_screen, 1.0)
        return self.label
        
    def check_permissions_loop(self, dt):
        #from android.permissions import check_permission, Permission
        # 1. Проверяем: выданы ли права прямо сейчас?
        #if check_permission(Permission.WRITE_EXTERNAL_STORAGE):
           # Clock.unschedule(self.check_permissions_loop)
        #self.label.text = "ПРАВА ПОЛУЧЕНЫ!\nЗапускаю фоновый мотор..."
        self.tttext = should_show_rationale(Permission.WRITE_EXTERNAL_STORAGE)
        #    self.start_service()
            
        # 2. Проверяем: нажал ли пользователь кнопку "ЗАПРЕТИТЬ"?
     #   elif should_show_rationale(Permission.WRITE_EXTERNAL_STORAGE):
       #     Clock.unschedule(self.check_permissions_loop)
            # Шлюз закрыт, пользователь явно нажал "Отклонить" в окошке
        #    self.label.text = "ОШИБКА ДОСТУПА!\nВы нажали 'Запретить'.\nФоновый мотор заблокирован операционной системой."
            
    def start_service(self):
        #try:
            try:
                base_path = primary_external_storage_path()
                sys.stdout = open(base_path+'/Download/app_log.txt', 'a', encoding='utf-8')
                self.tttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ НЕсбоит!\n{e}'
            except Exception as e:
                self.tttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ сбоит!\n{e}'
                #sys.stderr = sys.stdout  
        
           # except Exception as e:
             #   self.ttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ без разрешений!\n{e}'
                
        

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

                
