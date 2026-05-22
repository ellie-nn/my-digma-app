import os
import time
import csv
import tinytuya

# === ВАШИ ЖЕЛЕЗНЫЕ ДАННЫЕ ===
DEVICE_ID = 'bf1a864dc80b65d878lv65'
IP_ADDRESS = '192.168.1.4'
#IP_ADDRESS = '5.187.86.185'
LOCAL_KEY = 'X@o=_T>sgCfWGeEz'
# -------------------------------------------
# =============================

# Инициализируем розетку
d = tinytuya.OutletDevice(DEVICE_ID, IP_ADDRESS, LOCAL_KEY)
d.set_version(3.3)
d.set_socketTimeout(2)

# Имя файла истории
file_path = 'power_history.csv'

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
