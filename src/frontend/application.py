import sys

from PySide6.QtWidgets import QApplication

from .main_window import MainWindow

class Application(QApplication):
    def __init__(self):
        super().__init__()
        self.main = MainWindow()
        
        self.main.setGeometry(self.screens()[1].availableGeometry())
        
        self.main.showMaximized()