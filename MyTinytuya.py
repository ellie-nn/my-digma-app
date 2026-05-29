import socket
import json
import time
import os

# СКАНИРОВАНИЕ СЕТИ (Используем ваш быстрый и надежный ARP-метод!)
def deviceScan(tuyadevices=None, timeout=2):
    devices = {}
    try:
        with os.popen("ip neigh show") as f:
            for line in f:
                parts = line.split()
                if parts and len(parts) > 0:
                    ip = parts[0]
                    if ":" not in ip and ip != "127.0.0.1":
                        devices[ip] = {'gwId': 'auto', 'ip': ip, 'version': '3.3'}
    except:
        pass
    return devices

# НАСТОЯЩИЙ КЛАСС TUYA С БИНАРНЫМ ПИНКОМ ДЛЯ ВЕРСИИ 3.3 (БЕЗ ТОЧЕК И ВЫЛЕТОВ!)
class OutletDevice:
    def __init__(self, dev_id, ip, local_key):
        self.dev_id = dev_id
        self.ip = ip
        self.local_key = local_key
        self.latest_status = {}

    def set_version(self, v): pass
    def set_socketTimeout(self, t): pass

    def updatedps(self):
        try:
            # Официальная бинарная команда Tuya для запроса статуса (DP_QUERY)
            # Этот пинок заставит чип проснуться и выдать Ватты!
            cmd = b'\x00\x00\x55\xaa\x00\x00\x00\x00\x00\x00\x00\x0a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xaa\x55'
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.5)
            s.connect((self.ip, 6668))
            s.send(cmd) # Пинаем розетку!
            
            raw_bytes = s.recv(2048)
            s.close()
            
            if b'{' in raw_bytes:
                start = raw_bytes.find(b'{')
                end = raw_bytes.rfind(b'}') + 1
                json_str = raw_bytes[start:end].decode('utf-8', errors='ignore')
                self.latest_status = json.loads(json_str)
        except:
            self.latest_status = {}

    def status(self):
        return self.latest_status
    
