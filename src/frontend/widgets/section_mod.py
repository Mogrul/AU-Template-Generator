from dataclasses import dataclass

from PySide6.QtWidgets import QWidget, QLineEdit, QLabel

from .collapsible import Collapsible

class ModSection(Collapsible):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.tr("Mod Information"), start_open = True)
        self.mod_name = QLineEdit()
        self.author_name = QLineEdit(text = "Mogrul")
        self.author_url = QLineEdit(text = "https://mogrul.com")
        
        self.add_widgets([
            QLabel(self.tr("Mod Name")), self.mod_name,
            QLabel(self.tr("Author Name")), self.author_name,
            QLabel(self.tr("Author URL")), self.author_url
        ])
    
    def is_complete(self) -> bool:
        return True

    def get_data(self) -> ModSectionData:
        return ModSectionData(
            name = self.mod_name.text(),
            author_name = self.author_name.text(),
            author_url = self.author_url.text()
        )

@dataclass
class ModSectionData:
    name: str
    author_name: str
    author_url: str