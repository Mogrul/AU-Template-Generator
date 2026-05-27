from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QResizeEvent

from .widgets.top_bar import Topbar
from .widgets.side_bar import Sidebar
from .widgets.body import Body
from .helpers import resize_to_parent

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.set_design()
        self.top_bar = Topbar(self)
        self.side_bar = Sidebar(self)
        self.body = Body(self)
    
    def set_design(self):
        self.setWindowTitle("AU Template Generator")
        self.setMinimumSize(QSize(800, 600))
        self.setStyleSheet("background-color: white")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

    def resizeEvent(self, event: QResizeEvent):
        resize_to_parent(self.top_bar, height = 0.05)
        resize_to_parent(self.side_bar, width = 0.05, height = 0.95, y = 0.05)
        resize_to_parent(self.body, width = 0.95, height = 0.95, x = 0.05, y = 0.05)
        
        return super().resizeEvent(event)