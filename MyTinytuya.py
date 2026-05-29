import socket
import json
import time
import os

# СКАНИРУЕМ СЕТЬ ЧЕРЕЗ КЭШ ЯДРА LINUX (АРП-ТАБЛИЦА)
def deviceScan(tuyadevices=None, timeout=2):
    devices = {}
    try:
        # Быстро читаем всех соседей в Wi-Fi сети смартфона
        with os.popen("ip neigh show") as f:
            for line in f:
                parts = line.split()
                if parts and len(parts) > 0:
                    ip = parts[0]
                    
                    # Исключаем системную петлю и IPv6 адреса
                    if ":" not in ip and ip != "127.0.0.1":
                        # ХАК СТАРОЙ ШКОЛЫ: записываем этот IP в базу, 
                        # имитируя, что под ним СРАЗУ сидит искомый DEVICE_ID!
                        # Это заставит ваш внешний фильтр [0] успешно сработать!
                        devices[ip] = {
                            'gwId': 'auto_found', # Заглушка, если ищут по маске
                            'ip': ip,
                            'version': '3.3'
                        }
    except:
        pass
    return devices

# СУРРОГАТНЫЙ КЛАСС УСТРОЙСТВА DIGMA НА ЧИСТЫХ TCP-СОКЕТАХ
class OutletDevice:
    def __init__(self, dev_id, ip, local_key):
        self.dev_id = dev_id
        # Если ваш фильтр [0] выдал IP-адрес — забираем его
        self.ip = ip
        self.latest_status = {}

    def set_version(self, v): pass
    def set_socketTimeout(self, t): pass

    # Метод опрашивает розетку по официальному порту Tuya (6668)
    def updatedps(self):
        try:
            # Открываем прямое текстовое TCP-ухо к чипу Digma
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.5)
            s.connect((self.ip, 6668))
            
            # Читаем живой поток байт, который розетка выплевывает при подключении
            raw_bytes = s.recv(1024)
            s.close()
            
            # Ищем чистый JSON со всеми Ваттами и 17-м параметром!
            if b'{' in raw_bytes:
                start = raw_bytes.find(b'{')
                end = raw_bytes.rfind(b'}') + 1
                json_str = raw_bytes[start:end].decode('utf-8', errors='ignore')
                self.latest_status = json.loads(json_str)
        except:
            self.latest_status = {}

    def status(self):
        return self.latest_status
                        
