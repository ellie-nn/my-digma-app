#requirements = python3,tinytuya,plyer
#from plyer import notification
#notification.notify(title="Digma Recorder", message="Самописец успешно запущен! 🚀", timeout=3)
import os
import signal
# Железный стоп-кран: отправляет самому себе системный сигнал SIGKILL (убить процесс)
os.kill(os.getpid(), signal.SIGKILL)

# Этот бред принудительно вызовет Fatal Crash на экране телефона
raise ZeroDivisionError("Тестовый взрыв интерфейса старой школы!")

from kivy.app import App
from kivy.utils import platform
from kivy.uix.label import Label

class DigmaRecorderApp(App):
    def build(self):
        # Проверяем, что мы запустились именно на телефоне, а не на ПК
        #if platform == 'android' or 1:

        # Вместо рискованного if platform == 'android' or 1:
        try:
            from android import AndroidService
            # Запускаем наш фоновый движок, который мы прописали в buildozer.spec!
            service = AndroidService('DigmaService', 'Running...')
            service.start('service.py')
        except Exception as e:
            # Если импорт упал (например, на ПК или при инициализации среды), 
            # код не вылетит, а тихо запишет причину
            print(f"Сервис не запущен через мост: {e}")
            
        # Выводим на экран простую заглушку, чтобы Java-окно не падало
        return Label(text="Бортовой самописец Digma\nУспешно запущен в фоне!")

if __name__ == '__main__' or 1:
    DigmaRecorderApp().run()
