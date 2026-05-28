from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import Qt

from ..models import Fonts

class TopBar(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.fonts : Fonts = parent.fonts
        
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet("""
            QWidget {
                text-align: center;
                padding: 8px;
                background-color: #121314;
                color: #bfbfb0;
                border: none;
                font-weight: bold;
                border-radius: 5px;
                letter-spacing: 2px;
            }
        """)
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.title = QLabel("AU Template Generator", alignment = Qt.AlignmentFlag.AlignCenter)
        
        self.main_layout.addWidget(self.title)
        
        self.setLayout(self.main_layout)