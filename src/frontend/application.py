from dataclasses import dataclass
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtCore import Qt

from .main_window import MainWindow
from .models import Fonts

class Application(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
        self.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
        
        self.fonts = self.load_fonts()
        self.setFont(self.fonts.regular)
        
        self.main_window = MainWindow()
        self.main_window.show()
        
    def launch(self):
        sys.exit(self.exec())
    
    def load_fonts(self) -> Fonts:
        font_files = [
            "static/font/BarlowCondensed-Bold.ttf",
            "static/font/BarlowCondensed-Light.ttf",
            "static/font/BarlowCondensed-Regular.ttf"
        ]
        font_id = None

        for font_file in font_files:
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