from typing import Any

from PySide6.QtWidgets import QApplication

from .models import Fonts

class ThemeDict(dict):
    def __getattr__(self, key: str) -> Any:
        value = self[key]
        
        if isinstance(value, dict):
            return ThemeDict(value)

        return value

def getFonts() -> Fonts:
    app = QApplication.instance()
    return app.fonts

def getTheme() -> ThemeDict:
    app = QApplication.instance()
    return app.theme