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
# ИМПОРТИРУЕМ ДАТЧИК ОКНА
class DigmaRecorderApp(App):
    def build(self):
        #self.label = Label(text="⚙️ ОЖИДАНИЕ КЛИКА...", font_size='16sp', halign='center', valign='top')
        #self.label.bind(size=self.label.setter('text_size'))
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
        self.tttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ TTT!\n'
        
        #Запускаем секундный таймер Kivy для вывода отчетов на экран
        Clock.schedule_interval(self.update_screen, 1.0)
        
        if platform == 'android':
            # ВЫЗЫВАЕМ СТАНДАРТНОЕ ОКНО ЗАПРОСА ПРАВ НА ПАМЯТЬ
            from android.permissions import check_permission, request_permissions, Permission
            #from android.permissions import request_permissions, Permission
        
            if check_permission(Permission.WRITE_EXTERNAL_STORAGE):
                self.start_background_service()
            else:
                # ЗАПОМИНАЕМ, ЧТО ОКНО СЕЙЧАС ПОТЕРЯЕТ ФОКУС
                self.window_was_unfocused = False
                # Вешаем системный перехватчик фокуса Kivy
                Window.bind(on_flip=self.check_window_focus)
                request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        else:
            self.start_background_service()
            
        return self.label

# ЭТОТ МЕТОД КИВИ ВЫЗЫВАЕТ АВТОМАТИЧЕСКИ ПРИ КАЖДОМ КАДРЕ И ОБНОВЛЕНИИ ЭКРАНА!
    def check_window_focus(self, window):
        from android.permissions import check_permission, Permission
        
        # Шаг 1: Фиксируем момент, когда всплыло белое окно и наше приложение "уснуло"
        # (В этот момент Window.focus становится равным False)
        if not Window.focus:
            self.window_was_unfocused = True
            
        # Шаг 2: Фиксируем момент, когда белое окно ИСЧЕЗЛО (вы нажали кнопку),
        # и наше приложение снова вернулось на передний план!
        elif Window.focus and self.window_was_unfocused:
            # Сразу отвязываем перехватчик, чтобы не зацикливать
            Window.unbind(on_flip=self.check_window_focus)
            
            # А вот теперь ДЕЛАЕМ СИНХРОННЫЙ ИТОГОВЫЙ ДОСМОТР ПРАВ:
            if check_permission(Permission.WRITE_EXTERNAL_STORAGE):
                self.label.text = "⚙️ ПРАВА ПОЛУЧЕНЫ!\nЗапускаю фоновый мотор..."
                self.start_background_service()
            else:
                # Если фокус вернулся, но права все еще False — 
                # значит пользователь ТОЛЬКО ЧТО железно нажал кнопку "ЗАПРЕТИТЬ"!
                self.label.text = (
                    "❌ ВЫ НАЖАЛИ 'ЗАПРЕТИТЬ'!\n\n"
                    "Вы отклонили запрос. Мотор не запущен.\n"
                    "Перезапустите приложение, чтобы попробовать снова."
                    ) 
#-----------
    #PUBLIC_DIR = os.path.join(base_path, 'Documents')
#from kivy.utils import platform        
 #       request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
    # Clock.schedule_interval(self.check_permissions_loop, 1.0)
        
#        
       #return self.label
        
 #   def check_permissions_loop(self, dt):
 #       from android.permissions import check_permission, Permission
 #       # 1. Проверяем: выданы ли права прямо сейчас?
  #      #if check_permission(Permission.WRITE_EXTERNAL_STORAGE):
  #         # Clock.unschedule(self.check_permissions_loop)
  #      #self.label.text = "ПРАВА ПОЛУЧЕНЫ!\nЗапускаю фоновый мотор..."
   #     self.tttext = f'{check_permission(Permission.WRITE_EXTERNAL_STORAGE)}\n{should_show_rationale(Permission.WRITE_EXTERNAL_STORAGE)}'
  #      #    self.start_service()
            
   #     # 2. Проверяем: нажал ли пользователь кнопку "ЗАПРЕТИТЬ"?
  #   #   elif should_show_permission_rationale(Permission.WRITE_EXTERNAL_STORAGE):
  #     #     Clock.unschedule(self.check_permissions_loop)
   #         # Шлюз закрыт, пользователь явно нажал "Отклонить" в окошке
  #      #    self.label.text = "ОШИБКА ДОСТУПА!\nВы нажали 'Запретить'.\nФоновый мотор заблокирован операционной системой."
            
    def start_background_service(self):
        #try:
            try:
                base_path = primary_external_storage_path()
                #sys.stdout = open(base_path+'/Documents/app_log.txt', 'a', encoding='utf-8')
                self.flog = open(base_path+'/Documents/app_log.txt', 'w', encoding='utf-8')
                
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
            self.flog.write(f"[{time.strftime('%H:%M:%S')}]")
                
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

                
