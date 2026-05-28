from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QFrame, QSizePolicy, QScrollArea,
)
from PySide6.QtCore import Qt

from ..models import Fonts
from ..helpers import ThemeDict

class Collapsible(QWidget):    
    def __init__(
            self,
            parent: QWidget,
            title = "",
            start_open = False
    ):
        super().__init__(parent)
        self.fonts : Fonts = parent.fonts
        self.theme : ThemeDict = parent.theme
        
        self.title = title
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(5)
        
        self.header_btn = QPushButton(
            ("▼" if start_open else "▶") + " " + self.title
        )
        self.header_btn.setCheckable(True)
        self.header_btn.setChecked(start_open)
        self.header_btn.clicked.connect(self.toggle)
        self.header_btn.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.header_btn.setFont(self.fonts.bold)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setMaximumHeight(500)

        self.content = QWidget()
        self.content.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(10)
        
        self.scroll_area.setWidget(self.content)
        self.main_layout.addWidget(self.header_btn)
        self.main_layout.addWidget(self.scroll_area)
        
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        self.content.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        
        self.update_theme(self.theme)
        self.scroll_area.setVisible(start_open)
    
    def toggle(self) -> None:
        is_open = self.header_btn.isChecked()
        
        if is_open:
            self.header_btn.setText("▼ " + self.title)
            self.scroll_area.setVisible(True)
        else:
            self.header_btn.setText("▶ " + self.title)
            self.scroll_area.setVisible(False)
    
    def add_widget(self, widget: QWidget) -> None:
        self.content_layout.addWidget(widget)
    
    def add_widgets(self, widgets: list[QWidget]) -> None:
        for widget in widgets:
            self.add_widget(widget)
    
    def update_theme(self, theme: ThemeDict) -> None:
        self.header_btn.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding: 8px;
                background-color: {theme.button.normal};
                color: {theme.text.primary};
                border: none;
                border-radius: {theme.border.radius}px;
                letter-spacing: {theme.text.spacing.small}px;
            }}
            
            QPushButton:checked {{
                background-color: {theme.button.checked};
                color: {theme.text.checked};
            }}
            
            QPushButton:hover {{
                background-color: {theme.button.hovered};
            }}
            
            QPushButton:checked:hover {{
                background-color: {theme.button.hovered_checked};
            }}
        """)
        
        self.content.setStyleSheet(f"""
            QWidget {{
                background-color: {theme.background.surface};
                border-radius: {theme.border.radius}px;
            }}
            
            QLineEdit {{
                background-color: {theme.background.primary};
            }}
        """)