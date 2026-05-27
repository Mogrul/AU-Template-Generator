from PySide6.QtWidgets import QApplication

from .models import Fonts

def get_fonts() -> Fonts:
    app = QApplication.instance()
    return app.fonts