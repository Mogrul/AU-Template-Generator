from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QSizePolicy, QLabel,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor

from ..models.app_params import AppParams

class Sidebar(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.set_design()
        
        layout = QVBoxLayout(self)
        
        self.logo = Logo(self)
        layout.addWidget(self.logo)
        layout.addStretch()

    def set_design(self):
        self.setStyleSheet(f"""Sidebar {{
            background-color: {AppParams.bar_background.colour};
            border: {AppParams.border.size}px solid {AppParams.border.colour};
        }}""")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

class Logo(QLabel):
    def __init__(self, parent: Sidebar):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent")
        self.setPixmap(QPixmap("data/assets/uac_logo.png"))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Maximum
        )
        self.setMaximumHeight(75)
        self.setScaledContents(True)
        
        # Drop shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 3)
        shadow.setColor(QColor(0, 0, 0, 160))
        
        self.setGraphicsEffect(shadow)