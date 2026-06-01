from typing import Any
from pathlib import Path
import json
import logging

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QFont

from .shared.helpers import getTheme, getFonts
from .gui.main_window import MainWindow
from .shared.models import Fonts

class ThemeDict(dict):
    def __getattr__(self, key: str) -> Any:
        value = self[key]
        
        if isinstance(value, dict):
            return ThemeDict(value)

        return value

class Application(QApplication):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        self.theme = self._loadTheme()
        self.fonts = self._loadFonts()
        self.setFont(self.fonts.regular)
        
        self.main_window = MainWindow()
        self.logger.info("Launching main window...")
        self.main_window.show()
    
    def _loadTheme(self, path: str = None) -> ThemeDict:
        if not path:
            path = Path("static/theme.json")
    
        with open(path, "r") as f:
            return ThemeDict(json.load(f))
    
    def _loadFonts(self) -> Fonts:
        font_id = None
        base_dir = "static/font/"
        fonts = [
            base_dir + self.theme.font.bold,
            base_dir + self.theme.font.light,
            base_dir + self.theme.font.regular
        ]

        font_id = None

        for font_file in fonts:
            current_id = QFontDatabase.addApplicationFont(font_file)

            if font_id is None:
                font_id = current_id
        
        family = QFontDatabase.applicationFontFamilies(font_id)[0]
        
        regular = QFont(family, 12)
        regular.setStyleName("Condensed")
        
        bold = QFont(family, 13)
        bold.setStyleName("Condensed Bold")
        
        light = QFont(family, 11)
        light.setStyleName("Condensed Light")
        
        for f in [regular, bold, light]:
            f.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
            f.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        
        return Fonts(regular, bold, light)