# hook.py — ТОТАЛЬНЫЙ ПЕРЕХВАТЧИК МАНИФЕСТОВ ДЛЯ СЕРВЕРА ACTIONS
import os
from pythonforandroid.toolchain import ToolchainCL

def after_apk_build(toolchain: ToolchainCL):
    print("=== [HOOK] ТОТАЛЬНАЯ ЗАЧИСТКА МАНИФЕСТОВ ЗАПУЩЕНА! ===")
    
    # 1. Задаем корень поиска — всю папку сборки python-for-android
    search_root = toolchain.build_dir
    print(f"=== [HOOK] Сканируем папку: {search_root} ===")
    
    # Наш точный поисковый маркер Java-класса службы
    # (Замените 'org.oldschool.digmarecorder' на ваш package.domain + name)
    target = 'android:name="org.oldschool.digmarecorder.ServiceDigmaservice"'
    
    modified_count = 0
    
    # 2. Обходим абсолютно все папки на сервере в поисках Manifest файлов
    for root, dirs, files in os.walk(search_root):
        for file in files:
            if file == "AndroidManifest.xml":
                manifest_path = os.path.join(root, file)
                try:
                    # Читаем каждый найденный манифест
                    with open(manifest_path, "r", encoding="utf-8") as f:
                        text = f.read()
                    
                    # Если внутри этого файла живет наша служба
                    if target in text and 'android:foregroundServiceType' not in text:
                        print(f"=== [HOOK] Нашли совпадение в: {manifest_path}! Модифицируем...")
                        
                        pos = text.find(target)
                        end = text.find("/>", pos)
                        
                        # Врезаем тип dataSync прямо перед закрытием тега
                        text = text[:end] + ' android:foregroundServiceType="dataSync"' + text[end:]
                        
                        # Перезаписываем файл
                        with open(manifest_path, "w", encoding="utf-8") as f:
                            f.write(text)
                            
                        modified_count += 1
                except Exception as e:
                    pass

    print(f"=== [HOOK] ТОТАЛЬНАЯ ЗАЧИСТКА ЗАВЕРШЕНА! Успешно изменено файлов: {modified_count} ===")
