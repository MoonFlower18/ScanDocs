import os
import sys


def resource_path(relative_path: str) -> str:
    """
    Возвращает абсолютный путь к ресурсу.

    • При запуске из исходников: путь относительно корня проекта.
    • При запуске из .exe (PyInstaller): путь относительно временной
      папки _MEIPASS, куда PyInstaller распаковывает --add-data.
    """
    if hasattr(sys, "_MEIPASS"):
        # Режим .exe: PyInstaller распаковывает ресурсы в _MEIPASS
        base = sys._MEIPASS
    else:
        # Режим разработки: корень проекта — папка, где лежит core/
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_path)


def get_template_path(name: str) -> str:
    """Путь к шаблону в папке templates/."""
    return resource_path(os.path.join("templates", name))