from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

from ..models.app_params import AppParams

class Body(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.set_design()
    
    def set_design(self):
        self.setStyleSheet(f"background-color: {AppParams.body_background.colour}")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)