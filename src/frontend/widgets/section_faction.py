from dataclasses import dataclass

from PySide6.QtWidgets import (
    QWidget, QLineEdit, QPushButton,
    QHBoxLayout, QLabel, QFileDialog,
    QApplication
)
from PySide6.QtCore import Qt

from .collapsible import Collapsible
from .multi_item_text_edit import MultiItemTextEdit

class FactionSection(Collapsible):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.tr("Rebel Information"))
        self.name = QLineEdit()
        self.description = QLineEdit()
        self.type = QLineEdit(readOnly = True, placeholderText = "Reb")
        self.faces = QLineEdit()
        self.voices = QLineEdit()
        self.get_file_selection()
        
        self.vehicles_basic = MultiItemTextEdit(parent)
        self.vehicles_unarmed = MultiItemTextEdit(parent)
        self.vehicles_armed = MultiItemTextEdit(parent)
        self.vehicles_truck = MultiItemTextEdit(parent)
        self.vehicles_aa = MultiItemTextEdit(parent)
        self.vehicles_at = MultiItemTextEdit(parent)
        self.vehicles_boat = MultiItemTextEdit(parent)
        self.vehicles_planes = MultiItemTextEdit(parent)
        self.vehicles_medical = MultiItemTextEdit(parent)
        
        self.add_widgets([
            QLabel(self.tr("Name")), self.name,
            QLabel(self.tr("Description")), self.description,
            QLabel(self.tr("Type")), self.type,
            QLabel(self.tr("Flag")), self.file_row,
            QLabel(self.tr("Identity"), alignment = Qt.AlignmentFlag.AlignCenter, font = parent.fonts.bold),
            QLabel(self.tr("Faces")), self.faces,
            QLabel(self.tr("Voices")), self.voices,
            QLabel(self.tr("Military Vehicles"), alignment = Qt.AlignmentFlag.AlignCenter, font = parent.fonts.bold),
            QLabel(self.tr("Basic")), self.vehicles_basic,
            QLabel(self.tr("Unarmed")), self.vehicles_unarmed,
            QLabel(self.tr("Armed")), self.vehicles_armed,
            QLabel(self.tr("Trucks")), self.vehicles_truck,
            QLabel(self.tr("Anti Aire")), self.vehicles_aa,
            QLabel(self.tr("Anti Tank")), self.vehicles_at,
            QLabel(self.tr("Boats")), self.vehicles_boat,
            QLabel(self.tr("Planes")), self.vehicles_planes,
            QLabel(self.tr("Medical")), self.vehicles_medical
        ])
    
    def get_file_selection(self):
        self.file_path = QLineEdit(placeholderText = self.tr("No file selected..."))
        self.file_btn = QPushButton(self.tr("Browse"))
        self.file_btn.clicked.connect(self.open_file)
        self.file_row = QWidget()
        self.file_layout = QHBoxLayout(self.file_row)
        self.file_layout.setContentsMargins(0, 0, 0, 0)
        self.file_layout.setSpacing(0)
        self.file_layout.addWidget(self.file_btn)
        self.file_layout.addWidget(self.file_path)

    def open_file(self):
        QApplication.processEvents()
        
        path, _ = QFileDialog.getOpenFileName(
            self,
            self.tr("Select File"),
            "",
            "PAA Files (*.paa)"
        )
        
        if path:
            self.file_path.setText(path)
    
    def _str_to_lst(self, text: str) -> list[str]:
        return [item.strip() for item in text.split(",")]
    
    def is_complete(self) -> bool:
        return True
    
    def get_data(self) -> FactionSectionData:
        return FactionSectionData(
            name = self.name.text(),
            description = self.description.text(),
            type = self.type.text(),
            faces = self._str_to_lst(self.faces.text()),
            voices = self._str_to_lst(self.voices.text()),
            flag_file_path = self.file_path.text()
        )

@dataclass
class FactionSectionData:
    name: str
    description: str
    type: str
    faces: list[str]
    voices: list[str]
    flag_file_path: str