import time
#from android import AndroidService  # Импортируем управление службой
import os                            # Для os.getcwd() или системных проверок
import sys       # Для sys.stdout/sys.stderr и перехвата print()
from jnius import autoclass           # Наш ультимативный мост к Java-базе MediaStore

# Объявляем Android, что наша служба — бессмертная (Foreground Service)
# В шторке телефона зажжется неудаляемое уведомление. Без этого Android прибьет процесс через минуту.
#service = AndroidService()
#service.start('DigmaService', 'Идет непрерывный сбор данных...')
def append_to_public_documents(filename, text_content):
    try:
        # ХИРУРГИЧЕСКИЙ ФИКС ДЛЯ СЛУЖБЫ:
        # Сначала пытаемся взять контекст фоновой службы, а если мы на ПК — берем окно
        try:
            Context = autoclass('org.kivy.android.PythonService').mService
        except:
            Context = autoclass('org.kivy.android.PythonActivity').mActivity
            
        ContentValues = autoclass('android.content.ContentValues')
        MediaStoreFiles = autoclass('android.provider.MediaStore$Files')
        resolver = Context.getContentResolver()
        collection_uri = MediaStoreFiles.getContentUri("external")
        
        #print(f'Collection\n{collection_uri}\n')
        # 1. ОЛДСКУЛЬНЫЙ ИНСПЕКТОР БАЗЫ ДАННЫХ (Ищем старый файл по имени)
        # Составляем SQL-запрос к Android: имя файла и папка Documents
        #selection = f"_display_name='{filename}' AND relative_path='Documents/'"
        # Ищем файл по имени, а папку — по маске "содержит слово Documents"
        selection = f"_display_name='{filename}' AND relative_path LIKE '%Documents%'"

        cursor = resolver.query(collection_uri, ["_id"], selection, None, None)
        #print(f'Cursor\n{cursortostring(Cursor)}\n{cursor.moveToFirst()}\n')
        if cursor and cursor.moveToFirst():
            # ФАЙЛ НАЙДЕН в базе! Достаем его уникальный числовой ID
            file_id = cursor.getLong(cursor.getColumnIndex("_id"))
            ContentUris = autoclass('android.content.ContentUris')
            # Превращаем ID в ту самую старую, живую ссылку Uri
            file_uri = ContentUris.withAppendedId(collection_uri, file_id)
            cursor.close()
        else:
            # ФАЙЛА ЕЩЕ НЕТ — регистрируем новую строку в Documents/
            if cursor: cursor.close()
            values = ContentValues()
            values.put("_display_name", filename)
            #values.put("mime_type", "text/plain")
            values.put("mime_type", "application/octet-stream")
            values.put("relative_path", "Documents/")
            file_uri = resolver.insert(collection_uri, values)
        
        # 2. ОТКРЫВАЕМ СИСТЕМНЫЙ СТРИМ В РЕЖИМЕ СТРОГОЙ ДОЗАПИСИ "wa"
        output_stream = resolver.openOutputStream(file_uri, "wa")
        output_stream.write(bytes(text_content + "\n", 'utf-8'))
        output_stream.close()
        
    except Exception as e:
        # Если тестируем на ПК в Pydroid — пишем обычным Си-методом дозаписи
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(text_content + "\n")
        

# СТРОИМ КЛАСС-ПЕРЕХВАТЧИК
class MediaStoreStdout:
    def write(self, message):
        # Если прилетает не пустая строка — отправляем её в наш Java-мост
        if message and message.strip():
            # Вызываем вашу отлаженную функцию дозаписи в Documents!
            append_to_public_documents("app_log.txt", message.strip())
    def flush(self):
        pass  # Системная заглушка, обязательная для потоков stdout

# АКТИВИРУЕМ ТОТАЛЬНЫЙ ПЕРЕХВАТЧИК ОШИБОК СЛУЖБЫ В ФОНЕ
sys.stdout = MediaStoreStdout()
sys.stderr = sys.stdout

print('stdouttest')

# === ТЕСТОВЫЙ ВИБРО-ПИНОК СТАРТА СЛУЖБЫ ===
try:
    # 1. Достаем контекст живой фоновой службы Kivy
    Context = autoclass('org.kivy.android.PythonService').mService
    
    # 2. Вызываем официальную системную службу вибрации Android
    vibrator = Context.getSystemService(Context.VIBRATOR_SERVICE)
    
    # 3. Трясем телефон 2000 миллисекунд (2 секунды)
    vibrator.vibrate(2000)
except Exception as vib_err:
    # Если мы упали на старте — этот принт улетит в системный Logcat
    print(f"Ошибка вибромотора: {vib_err}")
# ==========================================

# НАШ БЕСКОНЕЧНЫЙ ФОНОВЫЙ ЦИКЛ
while True:
    # --------------------------------------------------
    # ЗДЕСЬ ИДЕТ ЛЮБАЯ ВАША ФОНОВАЯ РАБОТА (Запись логов, сокеты, интегралы)
    # --------------------------------------------------
    append_to_public_documents('servicework.txt', 'text_content')
    # Железное правило: фоновый цикл ОБЯЗАН спать хотя бы секунду, 
    # чтобы не раскалять процессор телефона до 100% и не жрать батарею!
    time.sleep(1.0)
