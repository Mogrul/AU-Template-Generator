from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QFrame, QLabel, QSizePolicy, QSpacerItem,
    QLineEdit
)
from PySide6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)
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
        self.main_layout.addWidget(self.submit_btn)
    
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
    
        self.header_btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 8px;
                background-color: #121314;
                color: #bfbfb0;
                border: none;
                font-weight: bold;
                border-radius: 5px;
            }
            
            QPushButton:checked {
                background-color: green;
            }
            
            QPushButton:hover {
                background-color: #252627;
            }
        """)

        self.content = QFrame()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        
        self.main_layout.addWidget(self.header_btn)
        self.main_layout.addWidget(self.content)
        
        self.content.setVisible(start_open)
    
    def toggle(self):
        if self.header_btn.isChecked():
            self.header_btn.setText("▼ " + self.title)
        else:
            self.header_btn.setText("▶ " + self.title)
        
        self.content.setVisible(self.header_btn.isChecked())
    
    def add_widget(self, widget: QWidget):
        self.content_layout.addWidget(widget)

class ModSection(Collapsible):
    def __init__(self, parent: MainWindow):
        super().__init__(parent, "Mod Information", start_open = True)
        self.add_widget(QLabel("Mod Name"))
        self.add_widget(QLineEdit())
        self.add_widget(QLabel("Author Name"))
        self.add_widget(QLineEdit())
        self.add_widget(QLabel("Author URL"))
        self.add_widget(QLineEdit())

class FactionSection(Collapsible):
    def __init__(self, parent: MainWindow):
        super().__init__(parent, "Faction Information")
        self.add_widget(QLabel("Name"))
        self.add_widget(QLineEdit())
        self.add_widget(QLabel("Description"))
        self.add_widget(QLineEdit())
        self.add_widget(QLabel("Type"))
        self.add_widget(QLineEdit())
        