from PySide6.QtWidgets import (
    QWidget, QVBoxLayout
)
from PySide6.QtCore import Qt

from ..shared.helpers import getTheme
from .widgets.sections import RebelSection, ModSection

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.theme = getTheme()
        
        # Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        
        # Collapsible widgets
        self.mod_info = ModSection(self)
        self.rebel_info = RebelSection(self)
        
        # Add widgets to layout
        self.main_layout.addWidget(self.mod_info)
        self.main_layout.addWidget(self.rebel_info)
        
        self.main_layout.addStretch(1)

    def _setDesign(self):
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet(f"""
            MainWindow {{
                background-color: {self.theme.background.primary};
            }}
        """)
        self.setFixedSize(1000, 800)
    
    def show(self):
        self._setDesign()
        
        return super().show()