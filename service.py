import os
import time
import csv
import tinytuya
import sys

# Перенаправляем весь вывод и ошибки в файл лога в режиме дозаписи (append)

from plyer import notification

notification.notify(title="Digma Recorder", message="Самописец успешно запущен!", timeout=3)

time.sleep(10)
raise SystemExit
sys.stdout = open('/storage/emulated/0/Documents/app_log.txt', 'a', encoding='utf-8')
sys.stderr = sys.stdout  
print('!!! PROGRAM LUNCHED !!!')
#print(f'Не удалось найти IP адрес розетки.')
#raise SystemExit

# Ошибки полетят туда же, куда и обычный print

# === ВАШИ ЖЕЛЕЗНЫЕ ДАННЫЕ ===
DEVICE_ID = 'bf1a864dc80b65d878lv65'
#IP_ADDRESS = '192.168.1.4'
#IP_ADDRESS = '5.187.86.185'
#MAC_ADDRESS = '42:4d:fe:8f:04:be'

LOCAL_KEY = 'X@o=_T>sgCfWGeEz'

try:
    # Сканируем эфир 2 секунды и ищем устройство с нашим ID
    devices = tinytuya.deviceScan(None,4)
    ip_address = [ip for ip, info in devices.items() if info.get('gwId') == DEVICE_ID][0]
   
except:
     print(f'Не удалось найти IP адрес розетки.')
     print(devices)
     raise SystemExit

# ------------------------------------------# ============================

# Инициализируем розетку
d = tinytuya.OutletDevice(DEVICE_ID, ip_address, LOCAL_KEY)
d.set_version(3.3)
d.set_socketTimeout(2)

# Имя файла истории
file_path = '/storage/emulated/0/power_history.csv'

# Создаем файл с заголовками, если его еще нет
if not os.path.isfile(file_path):
    with open(file_path, mode='a', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow(['Время', 'Мощность_Вт', 'Счетчик_17'])

print(">>> Бортовой самописец запущен и ждет нагрузку... <<<\n")

# Флаг для отслеживания нулевой мощности
was_last_zero = False

while True:
    try:
        # Быстрый пингующий запрос к чипу розетки
        d.updatedps()
        time.sleep(0.1)  # Крошечная пауза, чтобы розетка успела ответить
        
        # Забираем свежий статус
        data = d.status()
        
        if data and 'dps' in data:
            dps = data['dps']
            
            # Извлекаем Ватты (19) и Счетчик кВт*ч (17)
            raw_vatt = dps.get('19', 0)
            vatt = raw_vatt / 10.0
            
            # Если 17-й параметр есть - берем его, если скрыт - пишем -1
            kwh_17 = dps.get('17', -1)
            
            current_time = time.strftime('%H:%M:%S')
            
            # ЛОГИКА ФИЛЬТРАЦИИ НУЛЕЙ
            if raw_vatt == 0:
                if not was_last_zero:
                    # Записываем ТОЛЬКО ПЕРВЫЙ ноль, чтобы зафиксировать выключение
                    with open(file_path, mode='a', newline='', encoding='utf-8') as f:
                        csv.writer(f).writerow([current_time, vatt, kwh_17])
                    print(f"[{current_time}] Прибор отключен (0.0 Вт). Запись приостановлена.")
                    was_last_zero = True
                else:
                    # Если ноль продолжается - просто пропускаем секунду, не забивая файл
                    pass
            else:
                # Нагрузка есть (или появилась) — пишем данные каждую секунду
                was_last_zero = False
                with open(file_path, mode='a', newline='', encoding='utf-8') as f:
                    csv.writer(f).writerow([current_time, vatt, kwh_17])
                print(f"[{current_time}] Мощность: {vatt:<5} Вт | Параметр_17: {kwh_17}")
                
    except Exception as e:
        print(f"Ошибка связи: {e}")
        
    time.sleep(0.9)  # Добиваем шаг цикла ровно до 1 секунды
