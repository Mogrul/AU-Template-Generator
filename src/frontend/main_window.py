from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QFrame, QLabel, QSizePolicy, QSpacerItem,
    QLineEdit, QFileDialog, QHBoxLayout, QScrollArea,
    QApplication, QLayout
)
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QKeyEvent

from .helpers import get_fonts

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.fonts = get_fonts()
        
        self.setFixedSize(800, 1000)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet("background-color: #191a1b")
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        
        self.mod_section = ModSection(self)
        self.faction_section = FactionSection(self)
        
        self.main_layout.addWidget(self.mod_section)
        self.main_layout.addWidget(self.faction_section)
        
        self.main_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )
    
        self.submit_btn = QPushButton("Submit")
        self.submit_btn.setStyleSheet("""
            QPushButton {
                text-align: center;
                padding: 8px;
                background-color: #121314;
                color: #bfbfb0;
                border: none;
                font-weight: bold;
                border-radius: 5px;
                letter-spacing: 5px;
            }

            QPushButton:hover {
                background-color: #252627;
            }
            
            QPushButton:pressed {
                background-color: #bfbfb0;
                color: #252627;
            }
        """)
        self.submit_btn.setFixedWidth(200)
        
        self.main_layout.addWidget(self.submit_btn, alignment = Qt.AlignmentFlag.AlignCenter)
    
    def submit(self):
        pass

class Collapsible(QWidget):
    def __init__(
            self,
            parent: MainWindow,
            title = "",
            start_open = False
    ):
        super().__init__(parent)
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
        self.header_btn.setFont(parent.fonts.bold)
            
        self.header_btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 8px;
                background-color: #121314;
                color: #bfbfb0;
                border: none;
                font-weight: bold;
                border-radius: 5px;
                letter-spacing: 2px;
            }
            
            QPushButton:checked {
                background-color: #1f88b5;
                color: #092735;
            }
            
            QPushButton:hover {
                background-color: #252627;
            }
            
            QPushButton:checked:hover {
                background-color: #166182;
            }
        """)
        
        self.setStyleSheet("""
            QLineEdit {
                background-color: #252627;
                border: none;
                border-radius: 5px;
            }
        """)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setMaximumHeight(500)

        self.content = QWidget()
        
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(10)
        
        self.scroll_area.setWidget(self.content)
        self.main_layout.addWidget(self.header_btn)
        self.main_layout.addWidget(self.scroll_area)
        
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        self.content.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        
        self.scroll_area.setVisible(start_open)
    
    def toggle(self):
        is_open = self.header_btn.isChecked()
        
        if is_open:
            self.header_btn.setText("▼ " + self.title)
            self.scroll_area.setVisible(True)
        else:
            self.header_btn.setText("▶ " + self.title)
            self.scroll_area.setVisible(False)
    
    def add_widget(self, widget: QWidget):
        self.content_layout.addWidget(widget)

class ModSection(Collapsible):
    def __init__(self, parent: MainWindow):
        super().__init__(parent, "Mod Information", start_open = True)
        self.add_widget(QLabel("Mod Name"))
        self.add_widget(QLineEdit())
        self.add_widget(QLabel("Author Name"))
        self.add_widget(QLineEdit(text = "Mogrul"))
        self.add_widget(QLabel("Author URL"))
        self.add_widget(QLineEdit(text = "https://mogrul.com"))

class FactionSection(Collapsible):
    def __init__(self, parent: MainWindow):
        super().__init__(parent, "Rebel Information")
        self.rebel_name = QLineEdit()
        self.rebel_description = QLineEdit()
        self.rebel_type = QLineEdit(readOnly = True, placeholderText = "Reb")

        # File Row
        self.file_path = QLineEdit(placeholderText = "No file selected...")
        self.file_btn = QPushButton("Browse")
        self.file_btn.clicked.connect(self.open_file)
        self.file_row = QWidget()
        self.file_layout = QHBoxLayout(self.file_row)
        self.file_layout.setContentsMargins(0, 0, 0, 0)
        self.file_layout.setSpacing(0)
        self.file_layout.addWidget(self.file_btn)
        self.file_layout.addWidget(self.file_path)
        
        self.add_widget(QLabel("Rebel Name"))
        self.add_widget(self.rebel_name)
        self.add_widget(QLabel("Description"))
        self.add_widget(self.rebel_description)
        self.add_widget(QLabel("Type"))
        self.add_widget(self.rebel_type)
        self.add_widget(QLabel("Flag"))
        self.add_widget(self.file_row)
    
    def open_file(self):
        QApplication.processEvents()
        
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            "PAA Files (*.paa)"
        )
        
        if path:
            self.file_path.setText(path)