from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt

from .helpers import get_fonts, get_theme, ThemeDict
from .widgets.top_bar import TopBar
from .widgets.footer import Footer
from .widgets.section_mod import ModSection
from .widgets.section_faction import FactionSection

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AU Template Generator")
        self.fonts = get_fonts()
        self.theme = get_theme()
        
        self.setFixedSize(800, 1000)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        
        self.top_bar = TopBar(self)
        self.mod_section = ModSection(self)
        self.faction_section = FactionSection(self)
        
        self.main_layout.addWidget(self.top_bar)
        self.main_layout.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        )
        self.main_layout.addWidget(self.mod_section)
        self.main_layout.addWidget(self.faction_section)
        
        self.main_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
    
        self.submit_btn = QPushButton(self.tr("Submit"))
        self.submit_btn.setFixedWidth(200)
        self.submit_btn.clicked.connect(self.submit)
        self.main_layout.addWidget(self.submit_btn, alignment = Qt.AlignmentFlag.AlignCenter)
        
        self.main_layout.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        )
        self.footer = Footer(self)
        self.main_layout.addWidget(self.footer)
        
        self.update_theme(self.theme)
    
    def update_theme(self, theme: ThemeDict) -> None:
        self.setStyleSheet(f"background-color: {theme.background.primary}")
        self.submit_btn.setStyleSheet(f"""
            QPushButton {{
                text-align: center;
                padding: 8px;
                background-color: {theme.button.normal};
                color: {theme.text.primary};
                border: none;
                font-weight: bold;
                border-radius: {theme.border.radius}px;
                letter-spacing: {theme.text.spacing.large}px;
            }}

            QPushButton:hover {{
                background-color: {theme.button.hovered};
            }}
            
            QPushButton:pressed {{
                background-color: {theme.button.pressed};
                color: {theme.text.pressed};
            }}
        """)
    
    def submit(self):
        if (not self.mod_section.is_complete()
            or not self.faction_section.is_complete()):
            return
        
        mod_data = self.mod_section.get_data()
        rebel_data = self.faction_section.get_data()
        
        print(mod_data, rebel_data)