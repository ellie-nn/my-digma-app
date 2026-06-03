import time
import sys

# Перенаправляем потоки ошибок в Documents, чтобы видеть работу
sys.stdout = open("app_log.txt", "a", encoding="utf-8")
sys.stderr = sys.stdout

class BackgroundMotor:
    def __init__(self):
        print("=== [PYTHON] БЕССМЕРТНЫЙ МОТОР ИНИЦИАЛИЗИРОВАН ===")
        sys.stdout.flush()

    def run_forever(self):
        while True:
            # Наш тестовый цикл: пишем время в файл лога
            print(f"[{time.strftime('%H:%M:%S')}] Фоновый процесс дышит в фоне!")
            sys.stdout.flush() # Принудительно выталкиваем строку на диск!
            time.sleep(1.0)

if __name__ == '__main__':
    BackgroundMotor().run_forever()
