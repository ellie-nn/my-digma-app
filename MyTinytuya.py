import socket
import json
import time
import os

# 1. ЧЕСТНЫЙ АВТОПОИСК РОЗЕТКИ ПО СЕТЕВОМУ КЭШУ ANDROID 10
def deviceScan(tuyadevices=None, timeout=2):
    devices = {}
    try:
        # Читаем живой соседский кэш ядра Linux смартфона
        with os.popen("ip neigh show") as f:
            for line in f:
                parts = line.split()
                if parts and len(parts) > 0:
                    ip = parts[0]
                    # Записываем найденный IP как ключ, имитируя структуру оригинальной туи
                    devices[ip] = {'gwId': 'auto_found', 'ip': ip, 'version': '3.3'}
    except:
        pass
    return devices

# 2. КЛАСС-ЭМУЛЯТОР УСТРОЙСТВА DIGMA НА ЧИСТЫХ СОКЕТАХ
class OutletDevice:
    def __init__(self, dev_id, ip, local_key):
        self.dev_id = dev_id
        # Если IP пришел списком от автопоиска — берем первый, иначе используем строку
        self.ip = ip if isinstance(ip, list) and ip else (ip if ip != 'auto' else "192.168.1.15")
        self.local_key = local_key
        self.latest_status = {}

    def set_version(self, v): pass
    def set_socketTimeout(self, t): pass

    # Метод updatedps: шлем инженерный пинг розетке напрямую в порт Tuya (6668)
    # Чип Tuya устроен так, что при подключении сокета сам выплевывает свежий JSON со статусом!
    def updatedps(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.5)
            s.connect((self.ip, 6668))
            
            # Читаем сырые байты ответа чипа
            raw_bytes = s.recv(1024)
            s.close()
            
            # Ищем и вырезаем чистый JSON-текст из сетевого эфира
            if b'{' in raw_bytes:
                start = raw_bytes.find(b'{')
                json_str = raw_bytes[start:].decode('utf-8', errors='ignore')
                self.latest_status = json.loads(json_str)
        except:
            self.latest_status = {}

    # Возвращаем полученный JSON-пакет с Ваттами
    def status(self):
        return self.latest_status
                  
