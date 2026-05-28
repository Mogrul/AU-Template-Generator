from pathlib import Path
from typing import Any
import json

from PySide6.QtWidgets import QApplication

from .models import Fonts

class ThemeDict(dict):
    def __getattr__(self, key: str) -> Any:
        value = self[key]
        
        if isinstance(value, dict):
            return ThemeDict(value)

        return value

def get_fonts() -> Fonts:
    app = QApplication.instance()
    return app.fonts

def get_theme() -> ThemeDict:
    app = QApplication.instance()
    return app.theme

def load_theme(path = Path("static/theme.json")) -> ThemeDict:
    with open(path, "r") as f:
        return ThemeDict(json.load(f))