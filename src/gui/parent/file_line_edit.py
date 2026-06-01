from PySide6.QtWidgets import (
    QWidget, QPushButton, QLineEdit,
    QHBoxLayout, QFileDialog, QApplication
)

class FileLineEdit(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.button = QPushButton("Browse")
        self.button.clicked.connect(self.openDialog)
        self.line_edit = QLineEdit()
        
        self.main_layout.addWidget(self.button)
        self.main_layout.addWidget(self.line_edit)
    
    def openDialog(self) -> None:
        QApplication.processEvents()
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            "",
            "PAA (*.paa)"
        )
        
        if file_path:
            self.line_edit.setText(file_path)
    
    def _setDesign(self) -> None:
        self.setStyleSheet("""
            QPushButton {
                border-radius: 5px;
            }
        """)