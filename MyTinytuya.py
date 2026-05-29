import socket
import json
import time
import os

def deviceScan(tuyadevices=None, timeout=2):
    devices = {}
    
    # ОТКРЫВАЕМ НАСТОЯЩЕЕ UDP-УХО ДЛЯ СБОРА РАДИОСИГНАЛОВ РОЗЕТОК
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(timeout)
    
    try:
        # Привязываемся к официальному порту Tuya, куда розетка шлет вещание
        s.bind(('0.0.0.0', 6666))
    except:
        try:
            s.bind(('0.0.0.0', 6667))
        except:
            return devices

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Ловим сырые байты из эфира домашней сети
            data, addr = s.recvfrom(2048)
            ip = addr[0]
            
            # Ищем границы JSON внутри шифрованного пакета розетки Digma
            if b'{' in data:
                start = data.find(b'{')
                end = data.rfind(b'}') + 1
                json_str = data[start:end].decode('utf-8', errors='ignore')
                
                # Декодируем живой паспорт розетки
                payload = json.loads(json_str)
                real_gwId = payload.get('gwId')
                
                if real_gwId:
                    # УРА! Записываем в структуру ЕЁ НАСТОЯЩИЙ ЖЕЛЕЗНЫЙ ID И ВЕРСИЮ!
                    devices[ip] = {
                        'gwId': real_gwId,
                        'ip': ip,
                        'version': payload.get('version', '3.3')
                    }
        except socket.timeout:
            break
        except:
            pass
            
    s.close()
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
                  
#_-------------
                
