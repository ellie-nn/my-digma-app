# hook.py — ЗРЯЧИЙ КОВРОВЫЙ ПЕРЕХВАТЧИК МАНИФЕСТОВ
import os
from pythonforandroid.toolchain import ToolchainCL

def after_apk_build(toolchain: ToolchainCL):
    print("=== [HOOK] ТОТАЛЬНАЯ ЗАЧИСТКА МАНИФЕСТОВ СТАРТОВАЛА ===")
    
    try:
        # 1. Задаем корень поиска — всю папку сборки python-for-android
        search_root = toolchain.build_dir
        print(f"=== [HOOK] Корень сканирования: {search_root} ===")
        
        # Наш поисковый маркер Java-класса службы
        # ВНИМАНИЕ: Проверьте, что здесь написан именно ваш package.domain + package.name
        target = 'android:name="org.oldschool.digmarecorder.ServiceDigmaservice"'
        
        modified_count = 0
        
        # 2. Обходим все папки на сервере
        for root, dirs, files in os.walk(search_root):
            for file in files:
                # Фильтруем жестко: ищем ТОЛЬКО файлы манифеста, игнорируя бинарный мусор! [↑]
                if file == "AndroidManifest.xml":
                    manifest_path = os.path.join(root, file)
                    
                    try:
                        # Открываем файл в безопасном режиме 'r', игнорируя любые ошибки кодировок
                        with open(manifest_path, "r", encoding="utf-8", errors="ignore") as f:
                            text = f.read()
                        
                        # Если нашли нашу службу и в ней ЕЩЕ НЕТ типа foregroundServiceType
                        if target in text and 'android:foregroundServiceType' not in text:
                            print(f"=== [HOOK] МАРКЕР НАЙДЕН в файле: {manifest_path} ===")
                            
                            pos = text.find(target)
                            end = text.find("/>", pos)
                            
                            if end != -1:
                                # Врезаем тип dataSync прямо перед закрытием тега />
                                text = text[:end] + ' android:foregroundServiceType="dataSync"' + text[end:]
                                
                                with open(manifest_path, "w", encoding="utf-8") as f:
                                    f.write(text)
                                    
                                print(f"=== [HOOK] УСПЕХ: Файл {manifest_path} успешно модифицирован! ===")
                                modified_count += 1
                                
                    except Exception as file_err:
                        # Если конкретный файл занят или не читается — выводим ошибку и идем дальше
                        print(f"=== [HOOK] Предупреждение по файлу {file}: {file_err} ===")
                        
        print(f"=== [HOOK] ЗАЧИСТКА СЕРВЕРА ЗАВЕРШЕНА. Изменено файлов: {modified_count} ===")
        
    except Exception as global_err:
        # ЕСЛИ СКРИПТ ПАДАЛ — теперь эта строчка ЖЕЛЕЗНО прольется в логи сборки на GitHub!
        print(f"=== [HOOK] КРИТИЧЕСКАЯ ОШИБКА ВСЕГО ХУКА: {global_err} ===")
