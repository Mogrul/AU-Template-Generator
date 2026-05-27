import sys

from PySide6.QtWidgets import QApplication

from .main_window import MainWindow

class Application(QApplication):
    def __init__(self):
        super().__init__()
        self.main_window = MainWindow()
        self.main_window.show()
        
    def launch(self):
        sys.exit(self.exec())