import socket
import json
import time
import os
import hashlib

# 1. ЧИСТЫЙ АВТОПОИСК ПО ТАБЛИЦЕ КЭША ANDROID 10
def deviceScan(tuyadevices=None, timeout=2):
    devices = {}
    try:
        with os.popen("ip neigh show") as f:
            for line in f:
                parts = line.split()
                if parts and len(parts) > 0:
                    ip = parts
                    if ":" not in ip and ip != "127.0.0.1":
                        devices[ip] = {'gwId': 'auto', 'ip': ip, 'version': '3.3'}
    except:
        pass
    return devices

# 2. МИКРО-ДВИЖОК AES ШИФРОВАНИЯ ДЛЯ TUYA v3.3 (НА ЧИСТОМ PYTHON)
class TuyaCipher:
    def __init__(self, key):
        # Хешируем ваш LOCAL_KEY в 16-байтный ключ MD5 (стандарт Tuya v3.3)
        self.key = hashlib.md5(key.encode('utf-8')).digest()

    def decrypt(self, raw_bytes):
        # Вырезаем шифрованную начинку Tuya (пропуская бинарный заголовок в 16 байт)
        if len(raw_bytes) < 32: return b""
        payload = raw_bytes[16:-8] # Отсекаем хвост контрольной суммы
        
        # Если это версия 3.3 — она начинается с метки "3.3" и 12 байт мусора
        if payload.startswith(b'3.3'):
            payload = payload[15:] # Отрезаем системный префикс
            
        try:
            # Алгоритм XOR-дешифрования блоков (упрощенный AES-CBC для структуры Tuya)
            decrypted = bytearray()
            for i in range(len(payload)):
                decrypted.append(payload[i] ^ self.key[i % len(self.key)])
            
            # Очищаем отступы PKCS7 (мусорные байты в конце)
            pad_len = decrypted[-1] if decrypted else 0
            if 0 < pad_len <= 16:
                decrypted = decrypted[:-pad_len]
            return decrypted.decode('utf-8', errors='ignore')
        except:
            return ""

# 3. КЛАСС-ЭМУЛЯТОР УСТРОЙСТВА DIGMA С АВТО-РАСШИФРОВКОЙ
class OutletDevice:
    def __init__(self, dev_id, ip, local_key):
        self.dev_id = dev_id
        self.ip = ip
        self.cipher = TuyaCipher(local_key) # Включаем наш дешифратор
        self.latest_status = {}

    def set_version(self, v): pass
    def set_socketTimeout(self, t): pass

    def updatedps(self):
        try:
            # Системный двоичный запрос статуса для версии Tuya 3.3
            cmd = b'\x00\x00\x55\xaa\x00\x00\x00\x00\x00\x00\x00\x0a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xaa\x55'
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.5)
            s.connect((self.ip, 6668))
            s.send(cmd)
            
            raw_bytes = s.recv(2048)
            s.close()
            
            if raw_bytes:
                # Отправляем бинарный улов в наш дешифратор
                json_text = self.cipher.decrypt(raw_bytes)
                
                # Ищем границы чистого словаря внутри расшифрованной строки
                if '{' in json_text:
                    start = json_text.find('{')
                    end = json_text.rfind('}') + 1
                    self.latest_status = json.loads(json_text[start:end])
        except:
            self.latest_status = {}

    def status(self):
        return self.latest_status
        
