from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout
)
from PySide6.QtCore import Qt

from ...shared.helpers import getFonts, getTheme

class SubSection(QWidget):
    def __init__(self, title: str):
        super().__init__()
        self.fonts = getFonts()
        self.theme = getTheme()
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(5)
        
        self.title = QLabel(title, font = self.fonts.bold)
        self.main_layout.addWidget(self.title, alignment = Qt.AlignmentFlag.AlignCenter)

        self._setDesign()
    
    def _setDesign(self):
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet(f"""
            SubSection {{
                border-radius: {self.theme.border.radius};
                background-color: {self.theme.background.primary};
            }}
        """)

class SingleColumnSubSection(SubSection):
    def __init__(self, title: str):
        super().__init__(title)
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(5)
        
        self.main_layout.addWidget(self.content)
    
    def addWidget(self, widget: QWidget):
        self.content_layout.addWidget(widget)
    
    def addWidgets(self, widgets: list[QWidget]):
        for widget in widgets:
            self.addWidget(widget)

class MultiColumnSubSection(SubSection):
    def __init__(self, title: str, columns = 1):
        super().__init__(title)
        self.columns: dict[int, QVBoxLayout] = {}
        
        self.content = QWidget()
        self.content_layout = QHBoxLayout(self.content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(5)
    
        for x in range(columns):
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(5)
            
            self.content_layout.addLayout(layout)
            self.columns[x] = layout
        
        self.main_layout.addWidget(self.content)
    
    def addWidget(self, widget: QWidget):
        column = min(self.columns.values(), key = lambda c: c.count())
        column.addWidget(widget)
    
    def addWidgets(self, widgets: list[QWidget]):
        for widget in widgets:
            self.addWidget(widget)