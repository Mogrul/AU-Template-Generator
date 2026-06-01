from dataclasses import dataclass

from PySide6.QtGui import QFont

@dataclass
class Fonts:
    regular: QFont = None
    bold: QFont = None
    light: QFont = None