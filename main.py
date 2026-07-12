#import warnings
# ДАЕМ КОМАНДУ ПИТОНУ: ПОЛНОСТЬЮ ИГНОРИРОВАТЬ ЛЮБЫЕ ДЕКОРАТИВНЫЕ WARNINGS
#warnings.filterwarnings("ignore")
import time
from jnius import autoclass #, cast

vContext = autoclass('org.kivy.android.PythonActivity').mActivity
vibrator = vContext.getSystemService(vContext.VIBRATOR_SERVICE)
vibrator.vibrate(500) 
time.sleep(1.0)

# СТРОИМ КЛАСС-ПЕРЕХВАТЧИК
LOG_PATH=os.path.realpath(os.environ.get('EXTERNAL_STORAGE'))+'/Documents/'
READY_PATH=os.path.realpath(os.environ.get('EXTERNAL_STORAGE'))+'/Digma/'
#print(LOG_PATH)
class MediaStoreStdout:
    def __init__(self, outf = 'app_log.txt'):
      self.outfile = outf
      sys.stdout = self
      sys.stderr = sys.stdout
      return
    def write(self, message):
        # Если прилетает не пустая строка — отправляем её в наш Java-мост
        if message and message.strip():
            try:
                # Вызываем вашу отлаженную функцию дозаписи в Documents!
                #append_to_public_documents("log"+LOG_FN+".txt", message.strip())
                #append_to_public_documents(self.outfile, message.strip())
                with open(LOG_PATH+self.outfile, "a", encoding="utf-8", errors="ignore") as f:
                    f.write(message.strip()+"\n")
                    #f.flush
                    #f.close()
            except:
                pass
            f.close()
        return
    
    def flush(self):
        pass  # Системная заглушка, обязательная для потоков stdout
MediaStoreStdout()
print('START1')

import logging  # ИМПОРТИРУЕМ МОДУЛЬ ЛОГОВ
# 2. ЖЕСТКИЙ ЗАЖИМ ДЛЯ ТИНИТУИ: отключаем логирование ошибок уровня CRITICAL и ниже!
logging.disable(logging.CRITICAL)

import tinytuya
#if 'tinytuya' in sys.modules:


import os
#import signal
#import csv
import pyaes
import sys


from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform
#from android.storage import primary_external_storage_path

from kivy.core.window import Window


#from jnius import autoclass #, cast

from oscpy.server import OSCThreadServer
import inspect
import shutil
import traceback

# === СПИСОК УДАЛЕННЫХ И НЕНУЖНЫХ МОДУЛЕЙ ===
# import csv           # Больше не нужен, пишем строки через Java-стрим напрямую [↑]
# import signal        # Удален, фоновый мотор гасится штатными средствами Android [↑]
# from jnius import cast # Лишний метод, для Java-моста достаточно только autoclass [↑]
# from android.storage import primary_external_storage_path # Путь заблокирован ядром Linux [↑]

# ОСТАВЛЯЕМ ЗДЕСЬ СТРОГО ДЛЯ ГРАФИКИ И СТАРТА:
#from kivy.app import App
#from kivy.uix.label import Label
#from kivy.clock import Clock          # Чтобы раз в секунду читать лог службы
#from kivy.utils import platform       # Проверка, что мы на Android, а не на ПК
#from kivy.core.window import Window   # Наш шедевральный датчик фокуса окон

# ПЕРЕНОСИМ СЮДА ДЛЯ ЧЕРНОВОЙ РАБОТЫ В ФОНЕ:
#import os                             # Для os.getcwd() или системных проверок
#import sys                            # Для sys.stdout/sys.stderr и перехвата print()
#from jnius import autoclass           # Наш ультимативный мост к Java-базе MediaStore

#from plyer import notification
#notification.notify(title="Digma Recorder", message="Самописец успешно запущен!", timeout=3)

DEVICE_ID = 'bf1a864dc80b65d878lv65'
LOCAL_KEY = 'X@o=_T>sgCfWGeEz'
FILE_CSV = 'power_history.csv'
#SUB_DIR = "digma/" if os.android.get('ANDROID_ARGUMENT','')=='digmarecorderok' else ''
SUB_DIR = ''
#LOG_FN = 'app_aaf' #loogg'
LOG_FNw = str(time.time()//300)
LOG_FN = str(time.time()//300)
LOG_FN = 'logapp.txt'
#FILE_CSV = 'power_history.csv'
#SUB_TIME = os.path.getmtime(__file__) # Узнаем точное время создания/изменения нашего файла
SUB_TIME = int(time.time())
ADD_TIME = 0
GRAPH_WIDGET = None
# 1. Глобальная ячейка памяти для оригинального Си-метода Kivy
ORIGINAL_KIVY_UPDATER = None
GRAPH_INITED_FLAG=None
X_SYMBOLS_LENGTH=35
HOLD_LEFT=True
IN_LIVEDATA=False
MODE1=False

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
# Импортируем легальный Kivy-движок для графиков
from kivy_garden.graph import Graph, LinePlot
# если layout вертикальный:
# (from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
        
# Точный путь к файлу данных нашего бессмертного 12-го релиза
#LOG_PATH = 'Documents/'+SUB_DIR+'servicework.txt'
#LOG_PATH = "/Documents/servicework.txt"
#LOG_PATH = "/storage/emulated/0/Documents/"
#from jnius import autoclass, cast

from kivy.graphics import Mesh

def trace_opengl_indices(graph_instance):
    print("\n--- GRAPH OVERFLOW TRACE ---")
    
    # Kivy garden graph stores plots internally here
    #for i, plot in enumerate(graph_instance.plots):
        #print(i)
        #python_points = len(plot.points)
        #print(python_points)
        #gpu_indices = 0
        #gpu_vertices = 0
        
        # Look directly inside the low-level drawing instructions
        # where Kivy compiles Python lists into hardware buffers
        #for instr in plot.ask_draw_trigger.func.__self__.children:
    for i, plot in enumerate(graph_instance.plots):
        points_len = len(plot.points) if hasattr(plot, 'points') else 0
        print(f"  -> Plot #{i} ({type(plot).__name__}) Python points: {points_len}", flush=True)
    if True: return
        
    for instr in graph_instance.canvas.children:
        print('146 instr', instr)
        if isinstance(instr, Mesh):
            print('148 ok')
            mesh_counter += 1
            print('150 mesh:',mesh_counter)
            indices_count = len(instr.indices)
            print('152 indices_count:',indices_count)
            total_indices += indices_count
            #print(f"  [Mesh Object #{mesh_counter}] Indices inside GPU: {indices_count}", flush=True)
            print('155 total_indices',total_indices)
    
    #print('153 total ind:',total_indices)
           # if isinstance(instr, Mesh):
            #    print('ok')
            #    # This reads the actual array length sent to the GPU VRAM
            #    gpu_indices += len(instr.indices)
             #   print(gpu_indices)
             #   gpu_vertices += len(instr.vertices) // 8  # 8 floats per vertex block
             #   print(gpu_vertices)
                
        #print(f"Plot #{i} ({type(plot).__name__}):")
        #print(f"  -> Points in Python array: {python_points}")
        #print(f"  -> Vertices in GPU buffer: {gpu_vertices}")
        #print(f"  -> INDICES IN OPENGL:      {gpu_indices} / 65535 limit")
        
        #if gpu_indices > 60000:
            #print(" CRITICAL: This specific plot is causing the overflow!")
            
    return

def count_instructions(canvas_group):
    count = 0
    # canvas_group can be self.canvas, self.canvas.before, etc.
    for instr in canvas_group.children:
        count += 1
        # If it's a nested Canvas or InstructionGroup, look deeper
        if hasattr(instr, 'children'):
            count += count_instructions(instr)
    return count

def is_full_storage_allowed():
    try:
        Environment = autoclass('android.os.Environment')
        return Environment.isExternalStorageManager()    
    except Exception:
        return False
    return
        
def read_alie(fn):
    # Родной андроидный хак для новичков:
    # На Android 10 переменная 'EXTERNAL_STORAGE' всегда намертво знает 
    # правильный абсолютный путь к вашей внутренней памяти (уже со всеми нужными слэшами!
    base_dir = os.environ.get('EXTERNAL_STORAGE', '/storage/emulated/0')

    # Собираем путь в лоб, без ручных слэшей
    #file_path = os.path.join(base_dir, 'Documents', 'work.txt')
    with open("/storage/emulated/0/Documents/"+fn, "r", encoding="utf-8", errors="ignore") as f:
        tmpl='10 20 30 40'
        ret=f.read()
        #f.flush
        f.close()
    return ret
def freadln_range(uri,min,max):
    # Подключаем официальные Java-инструменты Android
    context = autoclass('org.kivy.android.PythonActivity').mActivity
    content_resolver = context.getContentResolver()
    # Предположим, у вас есть URI-ссылка на наш текстовый лог розетки
    # uri = ... (полученный от системы Android URI)

    try:
        # 1. Открываем легальный андроидный поток чтения по URI
        input_stream = content_resolver.openInputStream(uri)
        # 2. Оборачиваем его в быстрый Java-буфер, который умеет читать ПОСТРОЧНО
        InputStreamReader = autoclass('java.io.InputStreamReader')
        BufferedReader = autoclass('java.io.BufferedReader')
        reader = BufferedReader(InputStreamReader(input_stream, "UTF-8"))
        # ПОСТРОЧНЫЙ ПЕРЕБОР:
        # Память телефона не нагружается, файл не блокируется для фонового мотора!
        line_count = 0
        retline = ""
        #target_line = min  # Допустим, нам нужна строго 50-я строка
        while True:
            line = reader.readLine()
            if line is None: 
                break  # Файл закончился
            if line_count >= min:
                if retline: retline+='\n'
                retline += line
            if line_count == max:
                #print(f"[LOG] Найдена нужная строка: {line}")
                # ... здесь отдаем строку на наш график ...
                break
            line_count += 1
        # Обязательно закрываем шлюз за собо
        reader.close()
    except Exception as e:
        print(f"[ERR] Ошибка чтения через URI-поток: строка {line_count}\n{e}")
    return retline[:-1]

def append_to_public_documents(filename, text_content, min = None, max = None):
    #if filename[:3] != "log": return
    if text_content and not filename == 'mock.txt': text_content = filename+" "+text_content
    vContext = autoclass('org.kivy.android.PythonActivity').mActivity
    vibrator = vContext.getSystemService(vContext.VIBRATOR_SERVICE)
    #if min == 1: vibrator.vibrate(500) 
    #time.sleep(1.0)
    
    #if text_content: range = False
    range = str(min).isdigit() and str(max).isdigit() and not text_content
    if not (range or text_content): return
    vContext = autoclass('org.kivy.android.PythonActivity').mActivity
    vibrator = vContext.getSystemService(vContext.VIBRATOR_SERVICE)
    if min == 1: vibrator.vibrate(500); time.sleep(1.0)
    if is_full_storage_allowed():
        if text_content:
            
            with open(LOG_PATH+filename, "a", encoding="utf-8", errors="ignore") as f:
                #vContext = autoclass('org.kivy.android.PythonActivity').mActivity
                #vibrator = vContext.getSystemService(vContext.VIBRATOR_SERVICE)
                #vibrator.vibrate(500) 
                #time.sleep(1.0)
    
                #tmpl='10 20 30 40'
                f.write(text_content+"\n")
                f.flush
                f.close()
                return
        else:
            traceback.print_stack()
            print('filename:',filename,inspect.currentframe().f_lineno)
            print('282 traceback')
            traceback.print_stack()
            with open(LOG_PATH+filename, "r", encoding="utf-8", errors="ignore") as f:
                ret=f.read()
                f.close()
                return ret
    try:
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
        relpath = "Documents/"+SUB_DIR
        
        #selection = f"_display_name='{filename}' AND relative_path LIKE '%Documents/"+SUB_DIR+"%'"
        # 1. Зажимаем жесткий, универсальный фильтр:
        # Ищем файл СТРОГО по его имени и текстовому пути к папке Documents.
        # Символ '?' — это легальные SQL-заглушки, которые защищают запрос от синтаксических сбоев.
        #selection = "display_name = ? AND relative_path = ?"
        selection = f"_display_name='{filename}' AND relative_path LIKE '%Documents/"+SUB_DIR+"%' AND is_pending >= 0"
        
        # 2. Передаем точные значения для наших SQL-заглушек '?'
        # Важно: relative_path обязан заканчиваться косым слэшем '/'!
        selection_args = ["app_log.txt", "Documents/"]

        cursor = resolver.query(collection_uri, ["_id"], selection, None, None)
        # 3. ВЫЗЫВАЕМ ЗРЯЧИЙ SQL-ЗАПРОС:
        # Передаем обновленный selection и selection_args в вашresolver.query()
        #cursor = resolver.query(collection_uri, ["_id"], selection, selection_args, None)

        #print(f'Cursor\n{cursortostring(Cursor)}\n{cursor.moveToFirst()}\n')
        
        if cursor and cursor.moveToFirst():
            
            vContext = autoclass('org.kivy.android.PythonActivity').mActivity
            vibrator = vContext.getSystemService(vContext.VIBRATOR_SERVICE)
            if min == 1: vibrator.vibrate(500); time.sleep(1.0)
    
            # ФАЙЛ НАЙДЕН в базе! Достаем его уникальный числовой ID
            file_id = cursor.getLong(cursor.getColumnIndex("_id"))
            ContentUris = autoclass('android.content.ContentUris')
            # Превращаем ID в ту самую старую, живую ссылку Uri
            file_uri = ContentUris.withAppendedId(collection_uri, file_id)
            # Наш ContentValues у вас уже присвоен в начале функции.

            # Как только query() нашел старый _id файла после переустановки:
            #values = ContentValues()
       #     #values.clear()
            #values.put("is_pending", 0) # Принудительно открываем файл

            # ГЕНИАЛЬНЫЙ СЛИВ: Обновляем строку файла в базе данных через егоfile_uri.
            # Android 10 автоматически перепишет поле Owner UID на наше НОВОЕ приложение, 
            # и вызов openOutputStream("wa") мгновенно начнет дописывать логи без всяких капризов прав!
            #resolver.update(file_uri, values, None, None)

            # НАШ ПОБЕДНЫЙ ПЕРЕХВАТ ПРАВ ДЛЯ ANDROID 10:
            # Мы силой забираем у системы вечные флаги на ЧТЕНИЕ и ЗАПИСЬ этого старого файла.
            # Цифры 1 и 2 — это системные бинарные константы Intent.FLAG_GRANT_READ_URI_PERMISSION 
            # и Intent.FLAG_GRANT_WRITE_URI_PERMISSION.
            #try:
            #    resolver.takePersistableUriPermission(file_uri, 1 | 2)
            #except: pass
            #cursor.close()

                    # === МЫ ВНУТРИ БЛОКА, КОГДА QUERY УСПЕШНО НАШЁЛ СУЩЕСТВУЮЩИЙ ФАЙЛ ===
            cursor.close()
        
            vContext = autoclass('org.kivy.android.PythonActivity').mActivity
            vibrator = vContext.getSystemService(vContext.VIBRATOR_SERVICE)
            if min == 1: vibrator.vibrate(500); time.sleep(1.0)
    
        else:
            vContext = autoclass('org.kivy.android.PythonActivity').mActivity
            vibrator = vContext.getSystemService(vContext.VIBRATOR_SERVICE)
            if min == 1: vibrator.vibrate(2000); time.sleep(3.0)
    
            if not text_content: return
            # ФАЙЛА ЕЩЕ НЕТ — регистрируем новую строку в Documents/
            if cursor: cursor.close()
            values = ContentValues()
            values.put("_display_name", filename)
            values.put("mime_type", "application/octet-stream")
            values.put("relative_path", "Documents/"+SUB_DIR)
            file_uri = resolver.insert(collection_uri, values)
            try:
                values.clear(); 
                values.put("is_pending", 0)
                resolver.update(file_uri, values, None, None)
            except:
                pass
            
        
        if text_content:
            if True:
                # 2. ОТКРЫВАЕМ СИСТЕМНЫЙ СТРИМ В РЕЖИМЕ СТРОГОЙ ДОЗАПИСИ "wa"
                output_stream = resolver.openOutputStream(file_uri, "wa")
                output_stream.write(bytes(text_content + "\n", 'utf-8'))
                output_stream.close()
        else:
            vContext = autoclass('org.kivy.android.PythonActivity').mActivity
            vibrator = vContext.getSystemService(vContext.VIBRATOR_SERVICE)
            if min == 1: vibrator.vibrate(500); time.sleep(1.0)
    
            if not range: return
            vContext = autoclass('org.kivy.android.PythonActivity').mActivity
            vibrator = vContext.getSystemService(vContext.VIBRATOR_SERVICE)
            if min == 1: vibrator.vibrate(500); time.sleep(1.0)
    
            return freadln_range(file_uri,min,max)
        
    except Exception as e:
        # Если тестируем на ПК в Pydroid — пишем обычным Си-методом дозаписи
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(text_content + "\n")
        

def scale_func(v):
    ret=10**(v)
    #ret=v
    #print(f'v={v} f={ret}')
    return ret #int(ret)
def scale_revfunc(ret):
    v=math.log10(ret)
    #v=ret
    #print(f'f={ret} v={v}')
    return v #int(v)
    
if True:
    def apply_vertical_minutes_hack():
        """
        Трёхступенчатый хак: вычищает секунды, ставит бинарный семафор 
        от рекурсии и выстраивает минуты в вертикальные столбики! [↑]
        """
        global GRAPH_INITED_FLAG
        global GRAPH_WIDGET  # Ваш глобальный указатель на сетку my_graph
        #if GRAPH_WIDGET is None: return
        # Зрячий перебор скрытого списка детей графического холста [↑]
        for child in GRAPH_WIDGET.children:
            # Запускаем зрячий обыск всех внутренних переменных внутри my_graph [↑]
            # key — это текстовое имя переменной, val — ссылка на объект в памяти [↑]
            if False: # Перечисление дочерних классов и имён
                found_name = "Безымянный"
                for key, val in GRAPH_WIDGET.__dict__.items():
                    if val is child:
                        found_name = key  # Мы нашли, под каким именем этот ребенок привязан к графику!
                        break    
                    print(f"Класс: {child.__class__.__name__} | Служебное имя в коде: '{found_name}'")
     
            # Шпионский фильтр: отсекаем всё, что не является текстовым блоком Label
            if child.__class__.__name__ == 'GraphRotatedLabel': # or child.__class__.__name__ == 'Label':
                
                # ТОЧКА УДАРА №1: Проверяем наш бинарный семафор от рекурсии!
                # Если на конце строки уже стоит наш секретный пробел — значит, 
                # мы этот блок уже обрабатывали. Мгновенно уходим, разрывая петлю! [↑]
                try:
                    #child.text = '444'
                    child.text=str(int(child.text))
                    if not child.text: child.text = '444'
                    if str(child.text)[-1]==".":
                        child.text +='.'
                        #print(f'endswithdot: {child.text}')
                        continue
                except:
                    child.text = '222.'
                if True:
                    #if True:
                    try:
                        #child.text = "#."  
                        # Извлекаем чистые секунды, отбрасывая маркерный хвост
                        raw_seconds = float(child.text) #int(child.text.replace("SEC", ""))
                        # Переносим секунды в минуты (округляем до целого)
                        minutes = int(raw_seconds / 60)
                        # Строим узкий вертикальный столбик через \n
                        #vertical_minutes = "\n".join(list(str(minutes)))
                    
                        # ПРИСВАИВАНИЕ С МЕТКОЙ:
                        # Вшиваем пробел на конце! Kivy обновит экран, вызовет перерисовку,
                        # но на следующем круге ТОЧКА УДАРА №1 намертво заблокирует цикл! [↑]
                        #child.text = vertical_minutes + " "
                        #child.text = "-"
                        #child.texture_update()
                        if GRAPH_WIDGET.xlabel=="Минуты": 
                            child.text = str(minutes)
                        if GRAPH_WIDGET.xlabel=="Часы": 
                            child.text = str(int(minutes/60))
                        dt=(raw_seconds)-int(GRAPH_WIDGET.xmin)
                        child.text=str(int(raw_seconds%60))
                        if int(raw_seconds)==int(GRAPH_WIDGET.xmin):
                            child.text=f'\n{int(raw_seconds/3600)}h{(int(raw_seconds/60)-int(raw_seconds/3600)*60)}m\n{int(raw_seconds)-int(raw_seconds/60)*60}s'
                        if not int(raw_seconds)==int(GRAPH_WIDGET.xmin) and (dt%60==0): 
                            child.text=f'{int(raw_seconds//60-(raw_seconds//3600)*60)}m' #{int(raw_seconds%60)}s'
                        if not int(raw_seconds)==int(GRAPH_WIDGET.xmin) and (dt%3600==0): 
                            child.text=f'{int((raw_seconds//3600))}h{int(raw_seconds//60-(raw_seconds//3600)*60)}m' #{int(raw_seconds%60)}s'
                        #if not ("." in str(dt/3600)): 
                            #child.text=f'{int({(int(dt/60)}m{int(dt)-int(raw_seconds/60)*60}s'
                        
                        #print(f'raw/xmin: {int(raw_seconds)}=={int(GRAPH_WIDGET.xmin)}')
                        child.text += " "
                        #child.text = "-."  
                    except Exception as e:# ValueError:
                        #if not child.text and GRAPH_INITED_FLAG: GRAPH_WIDGET.x_ticks_major=120
                        #if not GRAPH_INITED_FLAG is None: GRAPH_INITED_FLAG+=1
                        print(f'label change error\n{child.text}\n{e}')
                        child.text = "=."
                        # Железобетонная страховка — если прилетел мусор, просто идем дальше
                        return
                        pass
        
        GRAPH_INITED_FLAG=True
        return
    # end if True

# 2. Наша чистая плоская базовая функция перерисовки осей
def custom_update_labels(*args, **kwargs):
    global ORIGINAL_KIVY_UPDATER
    global GRAPH_WIDGET
        
    # Страховка: если ссылки не прошиты — мгновенно выходим
    if ORIGINAL_KIVY_UPDATER is None or GRAPH_WIDGET is None:
        return

    # А) Принудительно вызываем родной Си-метод Kivy. 
    # Он снесёт старый холст и сгенерирует свежий секундный список _labels [↑]
    ret=ORIGINAL_KIVY_UPDATER(*args, **kwargs)
    
    # Б) ТОТАЛЬНЫЙ ЗАЖИМ: Мгновенно перехватываем свежесозданный список _labels
    # до того, как кадр улетит на отрисовку в видеочип OpenGL! [↑]
    apply_vertical_minutes_hack()
    #for label in GRAPH_WIDGET._labels:
    return ret

def update_points_from_file(graph,fn):
    global ADD_TIME
    print('456 update points start')
    tcut=append_to_public_documents(fn, "", 1,100)
    if True:
        if fn:
            m1 = [[float(w[1]), float(w[2])] for line in tcut.splitlines() if len(w := line.split())>3 and w[0][0]=='.']
            #print('522 m1:', m1)
            m1A = [[float(w[1])*5, float(w[3])] for line in tcut.splitlines() if len(w := line.split())>3 and w[0][0]=='.']
            #m1=m1[2500:5000]
            #m1A=m1A[2500:5000]
            #u = time.mktime(time.strptime(s, "%H:%M:%S"))

            ADD_TIME=str(m1[-1][0])        
            graph.mainclass.firstStamp=float(m1[0][0])
            
            step=int(len(m1)/1000+1)
            xm1=[]
            for i in range(0,step): xm1.append(m1[i::step]) 
            m1 = [[sum(values)/step for values in zip(*matrix)] for matrix in zip(*xm1)]
            #m1=result
            #print('533 xm1:', xm1)
            
            #print('535 m1:', m1)
            
            xm1A=[]
            for i in range(0,step): xm1A.append(m1A[i::step]) 
            m1A = [[sum(values)/step/5 for values in zip(*matrix)] for matrix in zip(*xm1A)]
            #m1=result
            
            #print('m1A:',m1A,inspect.currentframe().f_lineno)
            #if os.path.isfile(file_path)
            #mainclass.datafn=f'data_{int(m1[0][1])}.txt'
            m=[[0.0,0.0]]
            mA=m
            for x in reversed(m1): x[0]+=-m1[0][0]+m[-1][0]+1
            for x in reversed(m1A): x[0]+=-m1A[0][0]+m[-1][0]+1
            mA=mA+m1A
            m=m+m1
            #for x in m: x[0]/=60
            #for x in mA: x[0]/=60
        else:
            m=[[0.0,0.0]]
            mA=m
        #print(inspect.currentframe().f_lineno,'460 m:',m)
        #print(m1[0][0])
        
            
        #graph.parent.mainclass.tmax = m[-1][0]
        #print('552 mainclass.tmax,graph.xmax)',mainclass.tmax,graph.xmax)
        #graph.xmax=max(graph.parent.mainclass.tmax,graph.xmax)
        graph.xmax=max( m[-1][0],graph.xmax)
        #print('554 mainclass.tmax,graph.xmax)',mainclass.tmax,graph.xmax)
         
        #import os

        #time.sleep(10.0)
        #for x in m: points.append(x)
        #for x in mA: pointsA.append(x)
        print('573 m,mA [0,-1]:',m[0],m[-1],mA[0],mA[-1])
        print('573 m:',m)
        graph.plot.points=m
        graph.plotA.points=mA
        
    return
    
if True:

    def build_voltage_graph(file_path,mainclass):
        #"""
        #ФУНКЦИЯ-ПРОЖЕКТОР: Читает файл, собирает вольтаж и строит график.
        #"""
        print('518 build voltage start')
        global MODE1
        print('521 file_path',file_path,'-')
        if not MODE1: # or MODE1=='Продолжение':
            print('535 new graph widget')
            graph = Graph(
                xlabel='Время', ylabel='Ватты  &  Джоули',
                x_ticks_minor=6, x_ticks_major=60,
                y_ticks_minor=5, y_ticks_major=10,
                y_grid_label=True, x_grid_label=True,
                padding=10, x_grid=True, y_grid=True,
                xmin=0, xmax=120,  
                ymin=0, ymax=300
            )
            graph.mainclass=mainclass
        if not MODE1:
            return graph
        elif GRAPH_WIDGET:
            graph=GRAPH_WIDGET
        if False: #file_path:
            #tcut=append_to_public_documents("mock.txt", "", 1,100)
            tcut=append_to_public_documents(file_path, "", 1,100)
            #try:# Grabs indices 2 and 4 from each line
            #print(inspect.currentframe().f_lineno,'414 tcut:',tcut)
            #m = [(w[2], w[4]) for line in tcut.splitlines() if len(w := line.split()) > 3]
            #print(m)
            # Grabs indices 2 and 4 from each line
            m = [[float(w[1]), float(w[2])] for line in tcut.splitlines() if len(w := line.split())>3 and w[0][0]=='.' or w[0][0]==',']
            mA=m
            #u = time.mktime(time.strptime(s, "%H:%M:%S"))

            #print(inspect.currentframe().f_lineno,'422 m:',m)
            for x in reversed(m): x[0]-=m[0][0]
            #print(inspect.currentframe().f_lineno,'424 m:',m)
            print(inspect.currentframe().f_lineno,'425 m[0][0]:',m[0][0])
        else:
            m=[[0.0,0.0]]
            mA=m
            print('555 m00',inspect.currentframe().f_lineno,'490 m[0][0]:',m[0][0])
            
        if file_path:
            try:
                #tcut=append_to_public_documents(f"service_work_{int(SUB_TIME)}.txt", "", 1,100)              #tcut=append_to_public_documents(mainclass.datafn, "", 1,100)
                tcut=append_to_public_documents(file_path, "", 1,100)
                print(mainclass.datafn,inspect.currentframe().f_lineno)
                #print(tcut,inspect.currentframe().f_lineno)
                #tcut=append_to_public_documents("svcdata1782698598.txt", "", 1,100)
                #g=open(f'/storage/emulated/0/Documents/svcdata.txt','a', encoding="utf-8", errors="ignore")
                #m1 = [g.write("."+w+"\n") for line in tcut.splitlines() if len(w := line)>3 and w[0] in "0123456789"]
                #g.close()
                #sys.exit()
            except Exception as e:     
            
                print(f"line 505 Could not read {file_path}",f"service_work_{int(SUB_TIME)}.txt\n{e}")
                mainclass.datafn=""
                #tcut=append_to_public_documents("mock.txt", "", 1,100)
        
        #try:# Grabs indices 2 and 4 from each line
        #if mainclass.datafn:
        print('589 new plot widget')
        #plot = LinePlot(color=[0, 0.6, 1, 1], line_width=2.5)
        #plotA = LinePlot(color=[0, 1, 0.6, 1], line_width=2.5)
        #points = []
        #pointsA = []
        #plot.points = points
        #plotA.points = pointsA
        #graph.add_plot(plot)
        #graph.add_plot(plotA)
        #graph.plot=plot
        #graph.plotA=plotA

        graph.plot = LinePlot(color=[0, 0.6, 1, 1], line_width=2.5)
        graph.plotA = LinePlot(color=[0, 1, 0.6, 1], line_width=2.5)
        graph.add_plot(graph.plot)
        graph.add_plot(graph.plotA)
        
        if file_path:
            print('591 build voltage calls update points')
            update_points_from_file(graph,file_path)
            #graph.parent.mainclass.tmax = graph.plot.points[-1][0]
            mainclass.tmax = graph.plot.points[-1][0]
            print('889 ret from update points to build voltage')
        else:
            mainclass.firstStamp=0
            
        if False:
            print(inspect.currentframe().f_lineno,'438 настоящая история:')
            #print(inspect.currentframe().f_lineno,'439 tcut:',tcut)
            print(inspect.currentframe().f_lineno,'440 - /настоящая история')
      
            #m = [(w[2], w[4]) for line in tcut.splitlines() if len(w := line.split()) > 3]
            #print(m)
            # Grabs indices 2 and 4 from each line
            m1 = [[float(w[1]), float(w[2])] for line in tcut.splitlines() if len(w := line.split())>3 and w[0][0]=='.']
            print('522 m1:', m1)
            m1A = [[float(w[1])*5, float(w[3])] for line in tcut.splitlines() if len(w := line.split())>3 and w[0][0]=='.']
            #m1=m1[2500:5000]
            #m1A=m1A[2500:5000]
            #u = time.mktime(time.strptime(s, "%H:%M:%S"))

            step=int(len(m1)/2500+1)
            xm1=[]
            for i in range(0,step): xm1.append(m1[i::step]) 
            m1 = [[sum(values)/step for values in zip(*matrix)] for matrix in zip(*xm1)]
            #m1=result
            print('533 xm1:', xm1)
            
            print('535 m1:', m1)
            
            xm1A=[]
            for i in range(0,step): xm1A.append(m1A[i::step]) 
            m1A = [[sum(values)/step/5 for values in zip(*matrix)] for matrix in zip(*xm1A)]
            #m1=result
            
            #print('m1A:',m1A,inspect.currentframe().f_lineno)
            #if os.path.isfile(file_path)
            #mainclass.datafn=f'data_{int(m1[0][1])}.txt'
            for x in reversed(m1): x[0]+=-m1[0][0]+m[-1][0]+1
            for x in reversed(m1A): x[0]+=-m1A[0][0]+m[-1][0]+1
            mA=mA+m1A
            m=m+m1
            #for x in m: x[0]/=60
            #for x in mA: x[0]/=60
            
        #print(inspect.currentframe().f_lineno,'460 m:',m)
        #print(m1[0][0])
        
        #mainclass.tmax = m[-1][0]

        print('552 mainclass.tmax,graph.xmax)',mainclass.tmax,graph.xmax)
        graph.xmax=max(mainclass.tmax,graph.xmax)
        print('554 mainclass.tmax,graph.xmax)',mainclass.tmax,graph.xmax)
        
        
        #import os

        #time.sleep(10.0)
        #for x in m: points.append(x)
        #for x in mA: pointsA.append(x)
       
        if False:                        
            file_path = os.path.join(base_dir, 'Documents', 'servicework.txt')
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        x_index = 0
                        for line in f:
                            if True:
                                try:
                                    # Хирургический вырез значения вольтажа из строки лога
                                    voltage_value = float(line.split()[2])
                                
                                    points.append((x_index, voltage_value))
                                    x_index += 1
                                except Exception:
                                    continue
                    if len(points) > 20:
                        graph.xmax = len(points)
                except Exception as e:
                    print(inspect.currentframe().f_lineno,f"506 [ERR] Ошибка чтения файла1: {e}")
                    for i in range(1, 11):
                        voltage_value = i
                        x_index = i
                        points.append((x_index, voltage_value))
            
            else:
                print(inspect.currentframe().f_lineno,f"513 [ERR] Ошибка чтения файла2")
                for i in range(1, 11):
                    voltage_value = i
                    x_index = i
                    points.append((x_index, voltage_value))
                points = [(0, 120), (20, 220)]
                # end path exists
            # end False os file method
            # Заглушка, если мотор еще не успел создать файл на чистой установке
        #if not points:
            #points = [(0, 120), (20, 220)]
        #print(inspect.currentframe().f_lineno,'524 points:',points)
        mainclass.histtmax = mainclass.tmax #m[-1][0]
        return graph

    def hold_left_btn(instance):
        global HOLD_LEFT 
        HOLD_LEFT=not HOLD_LEFT         
        instance.background_color=[0.3, int(HOLD_LEFT),0.2,0.7]
        return


    #from kivy_garden.graph import Graph

    def format_x_axis(graph, value):
        # Returns the value formatted as a string (e.g. $10.00, Date, etc.)
            
        return f"${value:.2f}" 

    # Каждый раз, когда вы тащите бегунок, Kivy АВТОМАТИЧЕСКИ вызовет 
    # нашу микро-функцию move_window и сдвинет сетку!
    def scale_window(instance, val, hf = False):
        #with instance.gw as q:
        value=scale_func(val)
        #instance.value = value
        if not HOLD_LEFT or not IN_LIVEDATA: instance.gw.xmin = int((instance.gw.xmax - value))
        instance.mov.min = value-0.1
            
        #apply_vertical_minutes_hack()

        #log=math.log((instance.gw.xmax-instance.gw.xmin)/(X_SYMBOLS_LENGTH/int(math.log10(instance.gw.xmax)+1)),60)
        log=math.log((instance.gw.xmax-instance.gw.xmin)/(X_SYMBOLS_LENGTH/5),60)
        frac=0
        global X_MESURE
        instance.gw.xlabel="Секунды"
        if (log-int(log))>math.log(2,60): frac+=1
        if (log-int(log))>math.log(5,60): frac+=1
        if (log-int(log))>math.log(10,60): frac+=1
        if (log-int(log))>math.log(20,60): frac+=1
        if (log-int(log))>math.log(30,60): frac+=1; instance.gw.xlabel="Минуты"
        if (log-int(log))>math.log(1800,60): instance.gw.xlabel="Часы"
        instance.gw.x_ticks_major=int(60**int(log)*[2,5,10,20,30,60][int(frac)])
        return  
        
    def move_window(instance, value):
        # Допустим, ширина видимого окна графика на экране — всегда 60 секунд
        #with instance.gw as q:
        #instance.gw.xmin = (value - (instance.gw.xmax-instance.gw.xmin))
        print(f'{HOLD_LEFT} {IN_LIVEDATA} {not HOLD_LEFT or not IN_LIVEDATA}')
        if not HOLD_LEFT or not IN_LIVEDATA: instance.gw.xmin = int((value - scale_func(instance.scl.value)))
        instance.gw.xmax = max(value,120)
        #apply_vertical_minutes_hack()
        return
            
    # 4. НАШ ЗРЯЧИЙ ПЕРЕХВАТЧИК ВВОДА (Триггер на нажатие Enter на клавиатуре телефона):
        # Как только вы вбили данные и нажали "Готово/Enter" — Kivy сам выполнит эту микро-функцию!
    def on_text_submitted(instance):
        #if instance.mainclass.kilometers == instance.text: return
        print(f"[ВВОД] Пользователь вбил пробег: '{instance.text}'")
        instance.mainclass.kilometers = instance.text
        #apply_vertical_minutes_hack()
        return
            
    def on_text_submitted2(instance):
        #if instance.mainclass.kilometers == instance.text: return
        print(f"[ВВОД] Пользователь вбил вольтаж: '{instance.text}'")
        instance.mainclass.StartV = instance.text
        #apply_vertical_minutes_hack()
        return
            
    # ФАЗА 1: КАСАНИЕ (Палец опустился на график)
    def graph_touch_down(touch):
    # Проверяем, что палец попал именно в границы сетки графика, а не мимо
        if GRAPH_WIDGET.collide_point(*touch.pos):
            # Запоминаем физическую икс-координату пикселя, где палец коснулся экрана
            GRAPH_WIDGET.touch_start_x = touch.x
            # Переводим тач в режим фокуса (чтобы Kivy знал, кто держит экран)
            touch.grab(GRAPH_WIDGET)
            #apply_vertical_minutes_hack()
            return True
        #apply_vertical_minutes_hack()
        ret=super(GRAPH_WIDGET.__class__, GRAPH_WIDGET).on_touch_down(touch)
        #apply_vertical_minutes_hack()
        return ret
        
    # ФАЗА 2: ДВИЖЕНИЕ (Палец скользит по синусоиде)
    def graph_touch_move(touch):
        # Проверяем, что этот тач был захвачен именно нашим графиком
        if touch.grab_current is GRAPH_WIDGET:
            # ВЫЧИСЛЯЕМ ДЕЛЬТУ СДВИГА В ПИКСЕЛЯХ:
            # Сколько пикселей прошел палец от точки старта.
            # Если дельта положительная — палец тащит вправо, если отрицательная — влево.
            delta_pixels = touch.x - GRAPH_WIDGET.touch_start_x
        
            # МАСШТАБНЫЙ КОЭФФИЦИЕНТ:
            # Переводим пиксели экрана Самсунга в виртуальные секунды вашей истории!
            # Допустим, каждые 10 пикселей сдвига пальца = 1 секунда прокрутки истории.
            shift_seconds = delta_pixels * ((GRAPH_WIDGET.xmax-GRAPH_WIDGET.xmin)/GRAPH_WIDGET.parent.size[0]) #+/10.0
        
            # ИМИТАЦИЯ SLIDER.VALUE (Ваша готовая обработка!):
            # Мы берем текущее значение сдвига и силой сдвигаем его на дельту пальца.
            # Замените self.current_scroll_value на имя вашей переменной сдвига!
        
            new_fake_slider_value = GRAPH_WIDGET.scroll_bar.value - shift_seconds
        
            # Ограничиваем сдвиг в жесткие рамки истории (от 0 до xmax), чтобы не улететь в пустоту
            new_fake_slider_value = max(GRAPH_WIDGET.scroll_bar.min, min(new_fake_slider_value, GRAPH_WIDGET.scroll_bar.max))
            GRAPH_WIDGET.scroll_bar.value=new_fake_slider_value
            # ВЫЗЫВАЕМ ВАШУ ГОТОВУЮ ФУНКЦИЮ ОБРАБОТКИ СДВИГА:
            # Ей глубоко плевать, откуда пришла цифра — от бегунка Slider или от пальца!
            #self.ваша_процедура_отрисовки_сдвига(new_fake_slider_value)
        
            # Обновляем стартовую точку, чтобы скроллинг был непрерывным и шелковистым
            GRAPH_WIDGET.touch_start_x = touch.x
            #apply_vertical_minutes_hack()
            return True
        #apply_vertical_minutes_hack()
        ret=super(GRAPH_WIDGET.__class__, GRAPH_WIDGET).on_touch_move(touch)
        #apply_vertical_minutes_hack()
        return ret
        
    # ФАЗА 3: ОТПУСКАНИЕ (Палец оторвался от экрана)
    def graph_touch_up(touch):
        if touch.grab_current is GRAPH_WIDGET:
            # Освобождаем тач из захвата памяти Android
            touch.ungrab(GRAPH_WIDGET)
        
            # ЗДЕСЬ МОЖНО ЗАФИКСИРОВАТЬ РЕЖИМ ОКНА!
            # Автоматически переключаем тумблер в режим "застыть", 
            # раз пользователь сам руками полез листать историю назад во времени!
            #self.current_mode = "застыть"
            #apply_vertical_minutes_hack()
            return True
        #apply_vertical_minutes_hack()
        ret=super(GRAPH_WIDGET.__class__, GRAPH_WIDGET).on_touch_up(touch)
        #apply_vertical_minutes_hack()
        return ret
            
    def graph_update_ticks():
        ret=super(GRAPH_WIDGET.__class__, GRAPH_WIDGET).update_ticks()
        #apply_vertical_minutes_hack()
        return ret
def test_btn(instance):
    global MODE1
    if MODE1: return
    MODE1=instance.text
    instance.unbind(on_release=test_btn)
    instance.bro.unbind(on_release=test_btn)
    GRAPH_WIDGET.parent.remove_widget(instance.bro)
    GRAPH_WIDGET.parent.remove_widget(instance)
    GRAPH_WIDGET.opacity=0.5
    print('834 button calls build')
    GRAPH_WIDGET.parent.mainclass.build(mode=MODE1)
    print('837 ret from build to button')
    print('838 build done')
    return
    
def question(main_layout):
    if main_layout.mainclass.service_is_running: return
    global MODE1
    if MODE1:
        return
    btn_test = Button(
        text="Тест",
        size_hint=(0.25, 0.1),            # 50% ширины экрана, 8% высоты [↑]
        pos_hint={'x':0.1, 'center_y': 0.5},   # Центрируем внизу (отступ 25% слева, 5% вверх) [↑]
        background_color=[0.3, int(HOLD_LEFT), 0.2, 0.7] # Красный полупрозрачный оттенок кнопок старой школы
        )
        # Привязываем кнопку к нашей будущей функции очистки файла [↑]
    btn_test.bind(on_release=test_btn)
    main_layout.add_widget(btn_test)
    
    btn_work = Button(
        text="Работа",
        size_hint=(0.25, 0.1),            # 50% ширины экрана, 8% высоты [↑]
        pos_hint={'right': 0.9, 'center_y': 0.5},   # Центрируем внизу (отступ 25% слева, 5% вверх) [↑]
        background_color=[int(HOLD_LEFT), 0.3, 0.2, 0.7] # Красный полупрозрачный оттенок кнопок старой школы
        )
        # Привязываем кнопку к нашей будущей функции очистки файла [↑]
    btn_work.bind(on_release=test_btn)
    main_layout.add_widget(btn_work)
    #Window.canvas.ask_update()
    btn_test.bro=btn_work
    btn_work.bro=btn_test
    btn_test.parent=main_layout
    btn_work.parent=main_layout
    return
    
def btn_refresh_data_f(instance):
    print('874 refresh btn calls build update points')   
    update_points_from_file(GRAPH_WIDGET,GRAPH_WIDGET.parent.mainclass.datafn)
    print('877 ret from update points to refresh btn')
    return
    
def btn_StopSave_act(instance):
    print('957 btn_StopSave presseed')  
    mainclass.service.stop()
    shutil.copy(LOG_PATH+'svc'+mainclass.datafn,READY_PATH+'svc'+mainclass.datafn)
    print('959 ret from StopSave')
    return
def btn_StopSave_cr(main_layout):
    btn_StopSave = Button(
        text="Stop&Save",
        size_hint=(0.25, 0.1),            # 50% ширины экрана, 8% высоты [↑]
        pos_hint={'x':0.2, 'top': 0.5},   # Центрируем внизу (отступ 25% слева, 5% вверх) [↑]
        background_color=[0.3, int(HOLD_LEFT), 0.2, 0.7] # Красный полупрозрачный оттенок кнопок старой школы
        )
        # Привязываем кнопку к нашей будущей функции очистки файла [↑]
    btn_StopSave.bind(on_release=btn_StopSave_act)
    main_layout.add_widget(btn_StopSave)
    btn_StopSave.parent=main_layout
    return
        
def g_init(mainclass):
    print('869 ginit start')
    if True:
        global MODE1
        global GRAPH_WIDGET
        # ГЛАВНЫЙ КОНТЕЙНЕР: Свободный слой на всё окно [↑]
        if not MODE1: # or MODE1=='Продолжение':
            print('897 new floatlayout')
            main_layout = FloatLayout()
            main_layout.mainclass=mainclass
            mainclass.mywin=main_layout
            #mainclass.kilometers = ""
            #question(main_layout)
        # ========================================================
        # СЛОЙ 1 (НИЖНИЙ): НАШ ГРАФИК РАСТЯНУТ НА 100% ЭКРАНА [↑]
        # ========================================================
            #graph_widget = build_voltage_graph('mock.txt',mainclass)
            print('887 ginit calls build voltage')
            if True: #MODE1!='Продолжение':
                graph_widget = build_voltage_graph('',mainclass)
            #else:
             #   graph_widget = build_voltage_graph(mainclass.datafn,mainclass)
                
            print('889 ret from build voltage to ginit')
            
            # Занимает 100% ширины и 100% высоты окна [↑]
            graph_widget.size_hint = (1.0, 0.90) 
            graph_widget.pos_hint = {'center_x': 0.5, 'y':0.05}
        
            main_layout.add_widget(graph_widget)
            #graph_widget=main_layout.graph_widget
            main_layout.graph_widget=graph_widget
            #global GRAPH_WIDGET
            GRAPH_WIDGET = graph_widget
            graph_widget.opacity=0
        
            question(main_layout)
        if not MODE1:
            return main_layout
       # elif not MODE1=='Продолжение':
        #else:
        if True:
            #build_voltage_graph('mock.txt',mainclass)
            print('908 ginit calls build voltage')
            build_voltage_graph(mainclass.datafn,mainclass)
            print('910 ret from build voltage to ginit')
            graph_widget=GRAPH_WIDGET    
        try:
            main_layout=mainclass.mywin
        except:
            pass
            
            #mainclass.kilometers = ""
            #question(main_layout)
        # ========================================================
        # СЛОЙ 1 (НИЖНИЙ): НАШ ГРАФИК РАСТЯНУТ НА 100% ЭКРАНА [↑]
        # ========================================================
        graph_widget=main_layout.graph_widget
        
            # Занимает 100% ширины и 100% высоты окна [↑]
            #graph_widget.size_hint = (1.0, 0.90) 
            #graph_widget.pos_hint = {'center_x': 0.5, 'y':0.05}
        
            #main_layout.add_widget(graph_widget)
            #graph_widget.parent=main_layout
        
            #GRAPH_WIDGET = graph_widget
        graph_widget.opacity=1
        
            #question(main_layout)
            #return main_layout
        
        #main_layout.graph_widget=graph_widget
        from kivy.uix.label import Label

        # =====================================================================
        # НАШ ТОТАЛЬНЫЙ СКВОЗНОЙ ЛОГ-МОНИТОР
        # Вставляем этот блок внутрь вашего FloatLayout
        # =====================================================================

        log_screen = Label(
            text="[SYSTEM] Монитор лога активирован...\nОжидание данных розетки...",
    
            size_hint=(1.0, 1.0),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
    
            color=(0.2, 1.0, 0.2, 0.8),
            font_size='14sp',          # Размер шрифта, масштабируемый под экраны телефонов
            font_name='Roboto',        # Стандартный читаемый системный шрифт Android
    
            halign='left',
            valign='top'
            )
        # Без этой строчки Kivy проигнорирует valign, так как текстовая коробка внутри Label 
        # по умолчанию имеет нулевой размер. Мы принудительно заставляем внутренний 
        # текстовый блок строго совпадать с физическими размерами самого виджета!
        log_screen.bind(size=log_screen.setter('text_size'))
        #main_layout.add_widget(log_screen) 

        print('869 mainclass.tmax,xmax-xmin',mainclass.tmax,graph_widget.xmax-graph_widget.xmin)
        scroll_bar_scale = Slider(min=scale_revfunc(10), max=scale_revfunc(max(mainclass.tmax,graph_widget.xmax)), value=scale_revfunc(graph_widget.xmax-graph_widget.xmin), orientation='horizontal')
        scroll_bar_scale.gw = graph_widget
        scroll_bar_scale.bind(value=scale_window)

        scroll_bar_scale.size_hint = (1, 0.015) # Ширина 80%, высота 5% от экрана
        scroll_bar_scale.pos_hint = {'center_x': 0.5, 'top': 0.98} # Верхний край бегунка утыкается в низ графика!

        main_layout.add_widget(scroll_bar_scale) # Бегунок послушно встанет строго под графиком!
        main_layout.sbars=scroll_bar_scale
        

        # range - это пределы прокрутки (например, от 0 до 3600 секунд истории)
        # value - стартовая позиция ползунка
        scroll_bar = Slider(min=scale_func(scroll_bar_scale.value), max=mainclass.tmax, value=mainclass.tmax, orientation='horizontal')
        scroll_bar.gw = graph_widget
        scroll_bar.bind(value=move_window)
        # Наш график занимает 80% ширины экрана, 60% высоты и приподнят на 20% снизу

        scroll_bar.size_hint = (1, 0.015) # Ширина 80%, высота 5% от экрана
        scroll_bar.pos_hint = {'center_x': 0.5, 'y': 0.02} # Верхний край бегунка утыкается в низ графика!
      
        # Если у вас BoxLayout(orientation='vertical'), то:
        # main_layout.add_widget(my_graph)
        main_layout.add_widget(scroll_bar) # Бегунок послушно встанет строго под графиком!
        main_layout.sbarm=scroll_bar
            
        scroll_bar.scl=scroll_bar_scale
        scroll_bar_scale.mov=scroll_bar
        
        # ========================================================
        # СЛОЙ 2 (ВЕРХНИЙ): ПОЛУПРОЗРАЧНАЯ ШАПКА ПОВЕРХ СЕТКИ [↑]
        # ========================================================
        status_label = Label(
            text="Digma R12: Мониторинг сети",
            size_hint=(0.6, 0.08),            # 60% ширины экрана, 8% высоты [↑]
            pos_hint={'x': 0.2, 'y': 0.9},     # Центрируем сверху (отступ 20% слева, 90% вверх) [↑]
            color=[1, 1, 1, 0.8],             # Белый цвет с легкой прозрачностью 80%
            font_size=16
        )
        main_layout.add_widget(status_label)
        
        # ========================================================
        # СЛОЙ 3 (ВЕРХНИЙ): КНОПКА ОЧИСТКИ ПОВЕРХ ГРАФИКА ВНИЗУ [↑]
        # ========================================================
        btn_holdleft = Button(
            text="Д\nе\nр\nж\nа\nт\nь",
            size_hint=(0.06, 0.17),            # 50% ширины экрана, 8% высоты [↑]
            pos_hint={'x':0.0, 'y': 0.10},   # Центрируем внизу (отступ 25% слева, 5% вверх) [↑]
            background_color=[0.3, int(HOLD_LEFT), 0.2, 0.7] # Красный полупрозрачный оттенок кнопок старой школы
        )
        # Привязываем кнопку к нашей будущей функции очистки файла [↑]
        btn_holdleft.bind(on_release=hold_left_btn)
        main_layout.add_widget(btn_holdleft)
        from kivy.uix.textinput import TextInput
# =====================================================================
# НАШЕ ИНТЕРАКТИВНОЕ ПОЛЕ ВВОДА
# Вставляем этот блок строго ВНУТРИ вашего FloatLayout
# =====================================================================

        user_input2 = TextInput(
            # 1. Стартовый невидимый текст-подсказка (исчезает, когда вы тапаете пальцем)
            hint_text="Нач.Вольтаж",
            text=f'{mainclass.StartV}',                         # По умолчанию поле абсолютно пустое
            multiline=False,                 # Ввод строго в одну строку (удобно для ввода цифр)
    
            # 2. ЖЕСТКИЙ ПРОПОРЦИОНАЛЬНЫЙ ЗАЖИМ В ВОЗДУХЕ OVER GRAPH:
            # Задаем элементу фиксированную высоту (40 пикселей) под палец, 
            # но плавающую ширину (30% от ширины экрана Самсунга) [↑]
            size_hint=(0.3, None),
            height=100,
    
            # Прижимаем поле, например, к правому верхнему углу экрана поверх графика! [↑]
            # 'right': 0.95 оставляет изящный отступ в 5% справа, 'top': 0.95 — отступ сверху
            pos_hint={'right': 0.95, 'top': 0.8},
    
            # 3. ДИЗАЙН И ЧАСТИЧНАЯ ПРОЗРАЧНОСТЬ:
            # Сделаем задний фон поля полупрозрачным темно-серым (RGBA), 
            # чтобы сквозь него были зряче видны пики пролетающей синусоиды!
            background_color=(0.1, 0.1, 0.1, 0.5), 
            foreground_color=(0.2, 1.0, 0.2, 1.0),   # Текст ввода — неоново-зеленый
            hint_text_color=(0.5, 0.5, 0.5, 0.8),    # Цвет подсказки — тускло-серый
    
            font_size='16sp',                        # Крупный шрифт под палец
            cursor_color=(0.2, 1.0, 0.2, 1.0)        # Мигающий курсор тоже делаем зеленым
            )
        main_layout.add_widget(user_input2)
        main_layout.user_input=user_input2
        user_input2.mainclass=mainclass
        user_input2.bind(on_text_validate=on_text_submitted2)

        user_input = TextInput(
            # 1. Стартовый невидимый текст-подсказка (исчезает, когда вы тапаете пальцем)
            hint_text="Километры",
            text=f'{mainclass.kilometers}',                         # По умолчанию поле абсолютно пустое
            multiline=False,                 # Ввод строго в одну строку (удобно для ввода цифр)
    
            # 2. ЖЕСТКИЙ ПРОПОРЦИОНАЛЬНЫЙ ЗАЖИМ В ВОЗДУХЕ OVER GRAPH:
            # Задаем элементу фиксированную высоту (40 пикселей) под палец, 
            # но плавающую ширину (30% от ширины экрана Самсунга) [↑]
            size_hint=(0.3, None),
            height=100,
    
            # Прижимаем поле, например, к правому верхнему углу экрана поверх графика! [↑]
            # 'right': 0.95 оставляет изящный отступ в 5% справа, 'top': 0.95 — отступ сверху
            pos_hint={'right': 0.95, 'top': 0.90},
    
            # 3. ДИЗАЙН И ЧАСТИЧНАЯ ПРОЗРАЧНОСТЬ:
            # Сделаем задний фон поля полупрозрачным темно-серым (RGBA), 
            # чтобы сквозь него были зряче видны пики пролетающей синусоиды!
            background_color=(0.1, 0.1, 0.1, 0.5), 
            foreground_color=(0.2, 1.0, 0.2, 1.0),   # Текст ввода — неоново-зеленый
            hint_text_color=(0.5, 0.5, 0.5, 0.8),    # Цвет подсказки — тускло-серый
    
            font_size='16sp',                        # Крупный шрифт под палец
            cursor_color=(0.2, 1.0, 0.2, 1.0)        # Мигающий курсор тоже делаем зеленым
            )
        main_layout.add_widget(user_input)
        main_layout.user_input=user_input
        user_input.mainclass=mainclass
        user_input.bind(on_text_validate=on_text_submitted)
   
        # ДОБАВЛЕНИЕ В КОРЕНЬ ИНТЕРФЕЙСА:
        # Важно! Добавляйте user_input САМЫМ ПОСЛЕДНИМ в ваш FloatLayout (даже после Label лога),
        # чтобы Android положил его самым верхним, приоритетным слоем для тапов пальца!
        # main_layout.add_widget(my_graph)
        # main_layout.add_widget(scroll_bar)
        # main_layout.add_widget(user_input) 
        
        # НАМЕРТВО ПРИКЛЕИВАЕМ НАШИ ФУНКЦИИ ВНУТРЬ ОБЪЕКТА MY_GRAPH:
        graph_widget.touch_start_x = 0.0
        graph_widget.scroll_bar=scroll_bar
        graph_widget.on_touch_down = graph_touch_down
        graph_widget.on_touch_move = graph_touch_move
        graph_widget.on_touch_up = graph_touch_up
        graph_widget.update_ticks = graph_update_ticks
        # АКТИВИРУЕМ ТОТАЛЬНЫЙ ПЕРЕХВАТ БАЗОВОГО МЕТОДА:
        # Заменяем оригинальный _update_labels на наш контролируемый custom_update_labels
        global ORIGINAL_KIVY_UPDATER
        print('992 mode;',MODE1,ORIGINAL_KIVY_UPDATER,graph_widget._update_labels,custom_update_labels)
        ORIGINAL_KIVY_UPDATER=graph_widget._update_labels
        graph_widget._update_labels = custom_update_labels
        global GRAPH_INITED_FLAG
        #GRAPH_INITED_FLAG=0
        # Attach the formatting function to the graph
        #graph_widget.x_ticks_func = format_x_axis         
        btn_refresh_data = Button(
            text="Обновить",
            size_hint=(0.2, 0.1),            # 50% ширины экрана, 8% высоты [↑]
            pos_hint={'x':0.1, 'top': 0.9},   # Центрируем внизу (отступ 25% слева, 5% вверх) [↑]
            background_color=[0.3, int(HOLD_LEFT), 0.2, 0.7] # Красный полупрозрачный оттенок кнопок старой школы
            )
        # Привязываем кнопку к нашей будущей функции очистки файла [↑]
        btn_refresh_data.bind(on_release = btn_refresh_data_f)
        main_layout.add_widget(btn_refresh_data)
        
        btn_StopSave_cr(mainclass)
        
    return main_layout
          
import math
import time

def generate_mock_log_stream(duration_seconds=120, step_seconds=1.0):
    """
    Генерирует искусственную историю вольтажа/мощности розетки.
    duration_seconds - общая глубина лога в секундах.
    step_seconds - шаг между записями (например, раз в секунду).
    """
    try:
        open(LOG_PATH+"mock.txt", "r", encoding="utf-8", errors="ignore").close
        return
    except:
        pass
    # Стартовая точка отсчета времени (текущий штамп эпохи Linux)
    start_time = time.time()
    
    # Накопитель энергии (Джоули = Ватт * Секунды)
    total_joules = 0.0
    
    # Количество строк, которое нужно сгенерировать
    total_lines = int(duration_seconds / step_seconds)
    append_to_public_documents('mock.txt','№ Time Pow ΣPow HardPow')
    for i in range(1, total_lines+2):
        # Вычисляем текущее виртуальное время от старта
        elapsed = (i - 1) * step_seconds
        current_timestamp = start_time + elapsed
        
        # ФИЗИКА ПРИПОДНЯТОЙ СИНУСОИДЫ (Диапазон 0...200, Период 60 сек):
        # math.sin(2 * math.pi * elapsed / 60.0) дает колебания от -1 до 1 каждые 60 секунд.
        # + 1.0 сдвигает диапазон в 0...2. Умножение на 100.0 дает ровно 0...200 Вт!
        current_power = 100.0 * (math.sin(2 * math.pi * elapsed / 60.0) + 1.0)
        
        # Интегрируем джоули (Прибавляем энергию, набежавшую за текущий шаг)
        if elapsed > 0:
            total_joules += current_power * step_seconds
            
        # СБОРКА ТЕКСТОВОЙ МАТРИЦЫ СТРОКИ С ТОЧНОСТЬЮ ДО СОТЫХ ДОЛЕЙ:
        log_line = f".{i} {current_timestamp:.2f} {current_power:.2f} {total_joules:.2f} -1"
        
        # ЖЕСТКИЙ ПРИКАЗ ЗАПИСИ (Передаем готовую строку в ваш внешний шлюз):
        append_to_public_documents("mock.txt",log_line)
    return
def thelastfile(path,mask):
    from pathlib import Path

    # Define directory and mask
    directory = Path(path)
    #mask = 'data*.txt'

    # 1. Get matching files recursively (use .glob() if not searching subfolders)
    files = list(directory.rglob(mask))
    print('1075 files:',files)
    # 2. Sort by modification time
    files.sort(key=lambda x: x.stat().st_mtime)
    return files[-1]

#for file in files:
    #print(file)

# ИМПОРТИРУЕМ ДАТЧИК ОКНА
class DigmaRecorderApp(App):
    def build(self,mode=None):
        print('1179 main build start')
        global MODE1
        global SUB_TIME
        #self.mywin=False
        MediaStoreStdout(LOG_FN)
        
        import shutil
        print(SUB_TIME)
        if not MODE1:
            #from oscpy.server import OSCThreadServer
            import socket # Всего одна короткая строчка в самом верху файла!
            check_server =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #OSCThreadServer()
            try:
                # Окно пытается нагло встать на чужой OSC-порт (на порт 3001) [↑]:
                check_server.bind(("127.0.0.1", 3001))
                #listen(address='127.0.0.1', port=3001, default=True)
    
                # порт СВОБОДЕН,
                # сервис спит в темноте. Нам нужно его будить! [↑]
                check_server.close() # Сразу гасим наш проверочный сервер, освобождая порт обратно
                self.service_is_running = False
                self.datafn=''
                
            except:
            
                # OSC-порт 3001 уже занят сервисом,
                # библиотека oscpy выкинет официальный крэш RuntimeError (Address already in use)! [↑]
                # Наш блок except ловит этот сигнал и выдает зрячий вердикт: мотор жив! [↑]
                self.service_is_running = True
                print('1209 thelastfile: ',LOG_PATH[:-1])
                self.datafn=f'{thelastfile(LOG_PATH[:-1],'svcdata*.txt').name}'
                self.datafn=self.datafn[3:]
                SUB_TIME=int(self.datafn[4:-4])
                print(self.datafn)
                shutil.copy(LOG_PATH+'svc'+self.datafn, LOG_PATH+self.datafn) 
                #shutil.copy('/storage/emulated/0/Documents/svcdata1782698598.txt', '/storage/emulated/0/Documents/'+self.datafn) 
                #self.datafn='svcdata1782698598.txt'
                         #svcdata1782698598.txt
        if True: #not self.service_is_running:
            #print('1200 service not running')
            if not MODE1:
                print('1202 MODE1 is False',MODE1)
                print('1235 main build calls ginit')
                self.mywin = g_init(self)
                print('1238 ret from ginit to main build')
                if self.service_is_running:
                    MODE1='Продолжение'
                    self.build()
                return self.mywin
            elif MODE1=="Тест":
                print('1206 MODE1 is set to TEST',MODE1)
                self.datafn=f'data{SUB_TIME}.txt'
                shutil.copy(LOG_PATH+'svcdata1782698598.txt', LOG_PATH+f'svcdata{SUB_TIME}.txt') 
                shutil.copy(LOG_PATH+'svcdata1782698598.txt', LOG_PATH+self.datafn) 
        #elif not MODE1:
        #    print('1211 service is running')
         #   MODE1="Продолжение"
            
        print('1221 self.datafn',self.datafn)    
        if True:
            self.kilometers=''
            self.StartV=''
            #sys.stderr = sys.stdout
            self.tmax = 120
            #self.datafn=''
            #append_to_public_documents("servrk.txt","dfvhjggyjj")
            #print('.﻿1 20:29:10 11.4 0.001 -1')
            #print('.2 20:29:11 0.0 0.001 -1')
            #print('.3 20:29:13 11.1 0.006 -1')
            #print('.4 20:29:15 11.1 0.011 -1')
            #print('.5 20:29:11 0.0 0.001 -1')
            #print(read_alien("service_work.txt"))
            #print(append_to_public_documents("service_work.txt","",1,2))

            #from oscpy.server import OSCThreadServer
            import socket # Всего одна короткая строчка в самом верху файла!

        # =====================================================================
        # НАШ УЛЬТИМАТИВНЫЙ OSC-РАДАР (Без импорта socket!)
        # Допустим, ваш фоновый мотор держит OSC-порт 3001
        # =====================================================================

            #import shutil
            
            
        # =====================================================================
        # ИТОГОВЫЙ ТУМБЛЕР ПЕРЕКЛЮЧЕНИЯ ОСЕЙ:
        # =====================================================================
            if self.service_is_running:
                # ПОВТОРНЫЙ ВХОД: Мотор уже пашет, просто подключаемся к его эфиру! [↑]
                print("[РАДАР] Фоновый OSC-сервер на порту 3001 обнаружен. Подключение...")
            else:
                # ХОЛОДНЫЙ СТАРТ: В памяти пусто, официально запускаем службу! [↑]
                print("[РАДАР] Порт 3001 пуст. Запуск фонового сервиса...")
                # Здесь вызываем ваш запуск службы через mActivity [↑]

            #generate_mock_log_stream()
        
            print('START2')
            try:
                f = open(LOG_PATH+"ini.txt","r",encoding="utf-8", errors="ignore")
                run = f.read()
                f.close()
                try:
                    exec(run)
                    print(f'ini found,\n{run}executed, self.kilometers is set to {self.kilometers}')
                except Exception as e: print(f'Could not run\n{run}{e}')
            except: print('no file or could not open ini.txt')
        
            print('START3')
            print('START4')
            print('START5')
            print('START6')
            print('SUB TIME:',SUB_TIME)
        
            #sys.exit()
            #self.mywin = g_init(self)
            #return self.mywin
        print('1272 self.service_is_running',self.service_is_running)
        if not GRAPH_WIDGET:
            print('1310 main build calls ginit')
            self.mywin=g_init(self)
            print('1312 ret from ginit to main build')
        else:
            print('1314 main build calls ginit')
            g_init(self)
            print('1316 ret from ginit to main build')
        self.mywin.graph_widget.opacity=1
        if not self.service_is_running and self.datafn=='':
            self.datafn=f'data{SUB_TIME}.txt'
            
        print('self.histtmax:',self.histtmax)
        #print(append_to_public_documents('servicework.txt', '', 1,2))
        #time.sleep(10.0)
        #except: pass
        # Создаем на экране большую текстовую панель
        self.label = Label(
            text="Инициализация Python ядра...\nОжидайте.", 
            font_size='18sp',
            halign='center',
            valign='top'
        )
        self.label.bind(size=self.label.setter('text_size'))
        
        # === ТЕСТОВЫЙ ВИБРО-ПИНОК СТАРТА СЛУЖБЫ ===
      #  try:
    #        Context = autoclass('org.kivy.android.PythonActivity').mActivity
      #      vibrator = Context.getSystemService(Context.VIBRATOR_SERVICE)
       #     vibrator.vibrate(2000)
      #  except Exception as vib_err:
      #      print(f"Ошибка вибромотора: {vib_err}")
        # ==========================================
        self.launchtime=time.time()
        self.ttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ ПАШЕТ!\n'
            
        #time.sleep(30.0)                
        #return label
        
        self.vatt_sum = 0
        self.tttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ TTT!\n'
        # ПРОИЗВОДИМ ПОДМЕНУ В ЯДРЕ PYTHON
       
        try:
            devices = [] #tinytuya.deviceScan(None,10)
            ip_address = [ip for ip, info in devices.items() if info.get('gwId') == DEVICE_ID][0]
            print(f'Ip found: {ip_address}')
        except Exception as e:
            print(f'Can''t find ip\n{e}\nDevices={devices}\n')
            #raise SysExit
        try:               
            self.rosette = tinytuya.OutletDevice(DEVICE_ID, ip_address, LOCAL_KEY)
            self.rosette.set_version(3.3)
            self.rosette.set_socketTimeout(2)
            self.rosette.updatedps()
            time.sleep(0.1)
        
        except Exception as e:
            print(f'First interaction error:\n{e}')
            #raise SysExit
    
        self.text = f'СИСТЕМА СТАРОЙ ШКОЛЫ Ψ!\n'
        #self.ttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ tt!\n'
        self.last_time = time.time()
        self.vatt_sum = 0
        #Запускаем секундный таймер Kivy для вывода отчетов на экран
        #Запускаем секундный таймер Kivy для вывода отчетов на экран
        #Clock.schedule_interval(self.update_screen, 5.0)

        # мост к Java-службам Android
        from android import AndroidService
                
        #Создаем службу. Имя должно СТРОГО совпадать с тем, что в buildozer.spec!
        self.service = AndroidService('digmaservice', 'fore ground')
        
        # 1. Включаем наш внутренний радиоприемник
        self.server = OSCThreadServer()
        self.server.listen(address='127.0.0.1', port=3000, default=True)

        # 2. Намертво привязываем нашу волну к функции обновления экрана
        self.server.bind(b'/rosette_packet', self.display_live_data)
        
        try:       
            # Запускаем файл service.py в изолированном потоке памяти
            self.service.start(f'{int(SUB_TIME)}_{ADD_TIME}_{self.firstStamp}')
            #service.start(f'{int(SUB_TIME)}')
            print(f'{int(SUB_TIME)}_{ADD_TIME}')
            print(f'{int(SUB_TIME)}_{self.mywin.graph_widget.plot.points[-1][0]}_{int(SUB_TIME) - self.firstStamp - self.mywin.graph_widget.plot.points[-1][0]}'.split('_')[2])
            
            
            print('Успех запуска службы')  
        except Exception as e:
            self.ttext = f"Ошибка запуска службы: {e}"
            print(self.ttext)
        
        ###########
        #Clock.schedule_interval(self.update_screen, 1.0)
        
#        if platform == 'android':
  #          self.start_background_service()
 #       else:
  #          self.start_background_service()
        #import tinytuya    
        print('1370 self.datafn',self.datafn)
        return self.mywin
        
    def display_live_data(self,count,tstamp, vatt, integral,kwh):
        print('1374 self.datafn',self.datafn)
        try:
            print('1504 time points before:',self.mywin.graph_widget.plot.points[-2])
            print('1505 time points before:',self.mywin.graph_widget.plot.points[-1])
        except:
            pass
        if not self.datafn: return
        #print('1424 instructions:',count_instructions(Window))
        #trace_opengl_indices(GRAPH_WIDGET)
        #if self.histtmax>1000: return
        global IN_LIVEDATA
        IN_LIVEDATA=True
        xmn=GRAPH_WIDGET.xmin
        q=2
        print(f'1523 q2 1 xmin -- {xmn}')
        vContext = autoclass('org.kivy.android.PythonActivity').mActivity
        vibrator = vContext.getSystemService(vContext.VIBRATOR_SERVICE)
        #vibrator.vibrate(200); time.sleep(0.5)

        # Эта функция сама мгновенно сработает в ту же миллисекунду, 
        # когда служба пришлет свежий замер розетки!
        #current_time=time.strftime('%H:%M:%S', time.localtime(tstamp))
        #tstamp += SUB_TIME
        tstamp += self.firstStamp
        #if not self.datafn:
            #self.datafn=f'data{int(tstamp)}.txt'
        f=open(f'{LOG_PATH}{self.datafn}','a', encoding="utf-8", errors="ignore")
        if self.kilometers:
            #self.mywin.user_input.unbind(on_text_validate=on_text_submitted) 
          
            f.write(f'-{self.kilometers} -\n')   
            g=open(f'{LOG_PATH}ini.txt','a', encoding="utf-8", errors="ignore")
            g.write(f'self.kilometers = {self.kilometers}\n')
            g.close()
            #if self.mywin.user_input.text != self.kilometers:
                # 2. Спокойно меняем текст в полной бинарной темноте. Событие физически не может вызваться!
                #self.mywin.user_input.text = self.kilometers
                #user_input.hint_text = self.kilometers
                #pass
            
            self.kilometers = ""
            #self.mywin.user_input.bind(on_text_validate=on_text_submitted) 
        if self.StartV:
            #self.mywin.user_input.unbind(on_text_validate=on_text_submitted) 
            f.write(f'-{StartV} -\n')   
            g=open(f'{LOG_PATH}ini.txt','a', encoding="utf-8", errors="ignore")
            g.write(f'self.StartV = {self.StartV}\n')
            g.close()
            #if self.mywin.user_input.text != self.kilometers:
                # 2. Спокойно меняем текст в полной бинарной темноте. Событие физически не может вызваться!
                #self.mywin.user_input.text = self.kilometers
                #user_input.hint_text = self.kilometers
                #pass
            
            self.StartV = ""
            #self.mywin.user_input.bind(on_text_validate=on_text_submitted) 
                      
        if False:#self.kilometers:
            f.write(f'-{self.kilometers} -\n')   
            g=open(f'/storage/emulated/0/Documents/ini.txt','a', encoding="utf-8", errors="ignore")
            g.write(f'self.kilometers = {self.kilometers}\n')
            g.close()
                
            # 1. Намертво отвязываем нашу функцию от события валидации текста
            self.user_input.unbind(on_text_validate=on_text_submitted) 
            #if not self.user_input.text and self.user_input.text != self.kilometers:
                # 2. Спокойно меняем текст в полной бинарной темноте. Событие физически не может вызваться!
                #self.user_input.text = self.kilometers
                #user_input.hint_text = self.kilometers
                #pass
            self.kilometers = ""
            # 3. Возвращаем железную привязку обратно на место 
            self.user_input.bind(on_text_validate=on_text_submitted)
                
            #time.sleep(700)
            #if not self.kilometers:
            #vContext = autoclass('org.kivy.android.PythonActivity').mActivity
            #vibrator = vContext.getSystemService(vContext.VIBRATOR_SERVICE)
            #vibrator.vibrate(200); time.sleep(0.5)
          
        f.write(f'.{count} {tstamp} {vatt} {integral} {kwh} -\n')
        f.close()
        #self.label.text = f"N = {count}\n{time_}\nP = {vatt}\nΣP = {integral}\nP alternate = {kwh}"
        #self.label.text = f"N = {count}\n{tstamp}\nP = {vatt}\nΣP = {integral}\nP alternate = {kwh}"
        text = f"N = {count}\n{tstamp}\nP = {vatt}\nΣP = {integral}\nP alternate = {kwh}"
        print(text)
        #print(f'>>{self.mywin.graph_widget.plot.points}')
        print(f'1596 q2 {q} xmin > {GRAPH_WIDGET.xmin}'); q+=1
            
        if False:    
            tmax = tstamp-self.launchtime+self.histtmax
            if True: # (self.mywin.sbarm.max-self.mywin.sbarm.value)^2 <=4:
                self.mywin.xmax = tmax
                #self.mywin.sbars.value = tmax
            self.mywin.sbarm.max = tmax
            self.mywin.sbars.max = tmax
            if True:
                self.mywin.sbarm.value = tmax
            print(f'{tmax} {self.mywin.sbarm.value} {(self.mywin.sbarm.max-self.mywin.sbarm.value)^2}')
            self.mywin.graph_widget.plot.points.append([ tmax, tstamp-self.launchtime])
            self.mywin.graph_widget.plotA.points.append([ tmax, vatt]) 
            self.mywin.graph_widget.plot=self.mywin.graph_widget.plot
            self.mywin.graph_widget.plotA=self.mywin.graph_widget.plotA
        
        if True:
            #self.mywin.sbarm.unbind(value=move_window)
            #self.mywin.sbars.unbind(value=scale_window)
            
            #tmax = tstamp-self.launchtime+self.histtmax
            #tmax = tstamp-self.launchtime #+self.histtmax
            tmax = tstamp-self.firstStamp #self.launchtime #+self.histtmax
            print(f'1620 q3 {q} xmin > {GRAPH_WIDGET.xmin}'); q+=1
            self.mywin.sbarm.max = tmax
            print(f'1622 q4 {q} xmin > {GRAPH_WIDGET.xmin}'); q+=1
            print(f'{tmax}') #{self.mywin.sbarm.value}')# {tmax} {(self.mywin.sbarm.max-self.mywin.sbarm.value)^2}')
            self.mywin.sbars.max = scale_revfunc(max(tmax,120))
            print(f'1625 q5 {q} xmin > {GRAPH_WIDGET.xmin}'); q+=1
            if abs(tmax-self.mywin.sbarm.value) <=5:
                print(f'{q} if xmin -> {GRAPH_WIDGET.xmin}'); q+=1
                self.mywin.sbarm.value = tmax
                print(f'{q} if xmin > {GRAPH_WIDGET.xmin}'); q+=1
                 
                if HOLD_LEFT: self.mywin.sbars.value = scale_revfunc(max(tmax-self.mywin.graph_widget.xmin,120))
       #        self.mywin.xmax = tmax
                
            #self.mywin.xmax = self.mywin.xmax 
            #self.mywin.sbarm.value = self.mywin.sbarm.value
     #       self.mywin.sbars.max = tmax
            #self.mywin.sbarm.bind(value=move_window)
            #self.mywin.sbars.bind(value=scale_window)
            #self.mywin.sbarm.value=self.mywin.sbarm.value
            #self.mywin.sbars.value=self.mywin.sbars.value
            print('1617 points[-1]',tmax) 
            self.mywin.graph_widget.plot.points.append([ tmax, vatt])
            self.mywin.graph_widget.plotA.points.append([ tmax, integral])
            #self.mywin.graph_widget.plot=self.mywin.graph_widget.plot
            #self.mywin.graph_widget.plotA=self.mywin.graph_widget.plotA
            self.mywin.graph_widget.plot.points=self.mywin.graph_widget.plot.points
            self.mywin.graph_widget.plotA.points=self.mywin.graph_widget.plotA.points
            print(f'{q} xmin > {GRAPH_WIDGET.xmin}'); q+=1
              #if (tmax-self.mywin.sbarm.value)**2 <=3 and HOLD_LEFT: 
             #   self.mywin.sbars.value = tmax-self.mywin.xmin
               # scale_window(self.mywin.sbars, value = tmax-self.mywin.xmin, hf=True)
            print(f'{q} end xmin > {GRAPH_WIDGET.xmin}'); q+=1
          #print(f'3 xmin > {self.mywin.graph_widget.xmin}')
        
        IN_LIVEDATA=False    
        return 
     
    def check_permissions_callback(self, permissions, grants):    
    #def check_permissions_callback(self, permissions, grants):
        # Эта функция сама автоматически сработает, когда вы нажмете "Разрешить" на экране!
        if all(grants):
            self.label.text = "Права получены! Поджигаем фитиль..."
            try:
                from android import AndroidService
                service = AndroidService('digmaservice', 'Служба работает в фоне...')
                service.start('service.py')
                self.ttext = "СЛУЖБА ЗАПУЩЕНА!\nПроверяйте шторку телефона."
            except Exception as e:
                self.ttext = f" Ошибка старта: {e}"
        else:
            self.ttext = " Вы отказали в правах. Служба заблокирована системой!"
        return   
    def start_background_service(self):
        print('!!! -PROGRAM LUNCHED- !!!')
        
        try:
            self.tttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ НЕсбоит!\n{e}'
        except Exception as e:
            self.tttext = f'СИСТЕМА СТАРОЙ ШКОЛЫ сбоит!\n{e}'
                
    def update_screen(self, dt):
        #current_time = time.strftime('%H:%M:%S')
        
        
        # Забираем свежий статус
        data = False
        try:
            data = self.rosette.status()
        except:
            print('line 219, probably no self.rosette')
        time_ = time.time()
        print('!!! PROGRAM LUNCHED !!!')
        printout = f"{time.strftime('%H:%M:%S')}"
        current_time = time.strftime('%H:%M:%S')    
        if data and 'dps' in data:
            dps = data['dps']
            
            # Извлекаем Ватты (19) и Счетчик кВт*ч (17)
            raw_vatt = dps.get('19', 0)
            vatt = raw_vatt / 10.0
            
            # Если 17-й параметр есть - берем его, если скрыт - пишем -1
            kwh_17 = dps.get('17', -1)
            
            self.vatt_sum += vatt*(time_-self.last_time)
            self.last_time = time_
            printout = f"{time.strftime('%H:%M:%S')} {vatt} {self.vatt_sum/3600:.3f} {kwh_17}"
            append_to_public_documents('digmaspy.log',printout)
        else:
            printout = f"{time.strftime('%H:%M:%S')}"
        
        self.tttext = printout
        # Каждую секунду выводим на экран доказательство, что Python ЖИВ
        self.label.text = f"{self.tttext}\n{self.ttext}\nТекущее время: {current_time}\n\nОкно открыто и держит фокус."
        if data:
            self.rosette.updatedps()
        time.sleep(0.1)
        return
        
if __name__ == '__main__':
    DigmaRecorderApp().run()
