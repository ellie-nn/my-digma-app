#requirements = python3,tinytuya,plyer
#from plyer import notification
#notification.notify(title="Digma Recorder", message="Самописец успешно запущен! 🚀", timeout=3)

from kivy.app import App
from kivy.utils import platform
from kivy.uix.label import Label

class DigmaRecorderApp(App):
    def build(self):
        # Проверяем, что мы запустились именно на телефоне, а не на ПК
        if platform == 'android':
            from android import AndroidService
            # Запускаем наш фоновый движок, который мы прописали в buildozer.spec!
            service = AndroidService('DigmaService', 'Running...')
            service.start('service.py')
            
        # Выводим на экран простую заглушку, чтобы Java-окно не падало
        return Label(text="Бортовой самописец Digma\nУспешно запущен в фоне! 🚀")

if __name__ == '__main__':
    DigmaRecorderApp().run()
