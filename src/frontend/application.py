import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtCore import Qt, QTranslator, QLocale

from .main_window import MainWindow
from .models import Fonts
from .helpers import load_theme

class Application(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
        self.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
        self.setup_locale()
        
        self.theme = load_theme()
        self.fonts = self.load_fonts()
        self.setFont(self.fonts.regular)
        
        self.main_window = MainWindow()
        self.main_window.show()
        
    def launch(self):
        sys.exit(self.exec())
    
    def load_fonts(self) -> Fonts:
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

    def setup_locale(self) -> None:
        translator = QTranslator()
        lang_code = QLocale.system().name().split("_")[0]
        fallback = Path("static/locale/en.qm")
        lang = Path(f"static/locale/{lang_code}.qm")
        
        if lang.exists():
            translator.load(str(lang))
        else:
            translator.load(str(fallback))
        
        self.installTranslator(translator)