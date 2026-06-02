# hook.py — ОЛДСКУЛЬНЫЙ ИНЖЕКТОР ПАСПОРТА СЛУЖБЫ (100% РАБОЧИЙ ВАРИАНТ)
from pathlib import Path
from pythonforandroid.toolchain import ToolchainCL

def after_apk_build(toolchain: ToolchainCL):
    print("=== [HOOK] СТАРТ ПЕРЕХВАТА МАНИФЕСТА ===")
    
    # ЭТАЛОННЫЙ ПУТЬ К МАНИФЕСТУ ВНУТРИ СЕРВЕРА ACTIONS (По чертежам Kivy)
    manifest_file = Path(toolchain._dist.dist_dir) / "src" / "main" / "AndroidManifest.xml"
    
    if not manifest_file.exists():
        print(f"=== [HOOK] КРИТИЧЕСКАЯ ОШИБКА: Манифест не найден по пути: {manifest_file} ===")
        return

    # Читаем манифест как обычный текст
    text = manifest_file.read_text(encoding="utf-8")
    
    # ВНИМАНИЕ: Наш точный поисковый маркер Java-класса службы!
    # Замените 'org.oldschool.digmarecorder' строго на ваш package.domain + package.name из spec!
    target = 'android:name="org.oldschool.digmarecorder.ServiceDigmaservice"'
    
    # Ищем, в каком месте текста притаилась наша служба
    pos = text.find(target)
    if pos != -1:
        # Находим закрывающий тег этой службы "/>"
        end = text.find("/>", pos)
        
        # Хирургический укол: врезаем тип dataSync прямо перед закрытием тега!
        text = (text[:end] + ' android:foregroundServiceType="dataSync"' + text[end:])
        
        # Перезаписываем готовый измененный файл обратно на диск сервера
        manifest_file.write_text(text, encoding="utf-8")
        print("=== [HOOK] УСПЕХ! Атрибут foregroundServiceType добавлен в манифест! ===")
    else:
        print("=== [HOOK] ОШИБКА: Строка службы не найдена в тексте манифеста! ===")
