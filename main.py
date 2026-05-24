import time
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock

class DebugApp(App):
    def build(self):
        # Создаем на экране большую текстовую панель
        self.label = Label(
            text="Инициализация Python ядра...\nОжидайте.", 
            font_size='18sp',
            halign='center'
        )
        
        # Запускаем секундный таймер Kivy для вывода отчетов на экран
        Clock.schedule_interval(self.update_screen, 1.0)
        return self.label

    def update_screen(self, dt):
        current_time = time.strftime('%H:%M:%S')
        # Каждую секунду выводим на экран доказательство, что Python ЖИВ
        self.label.text = f"⚙️ СИСТЕМА СТАРОЙ ШКОЛЫ ЖИВА!\nТекущее время: {current_time}\n\nОкно открыто и держит фокус."
        raise ZeroDivisionError("Тестовый взрыв интерфейса старой школы!")

if __name__ == '__main__':
    DebugApp().run()
