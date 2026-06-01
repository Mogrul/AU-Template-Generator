from PySide6.QtWidgets import (
    QWidget, QLineEdit, QLabel
)

from ..parent.collapsible import Collapsible
from ..parent.multi_line_edit import MultiLineLabelledEdit, MultiLineParams
from ..parent.file_line_edit import FileLineEdit
from ..parent.subsection import SingleColumnSubSection, MultiColumnSubSection

class RebelSection(Collapsible):
    def __init__(self, main_window: QWidget):
        super().__init__(main_window, "Rebel Information")
        self.addInfo()
        self.addVehicles()
        self._setDesign()
        
    def addInfo(self):
        identity_subsection = SingleColumnSubSection(self.tr("Identity"))
        identity_subsection.addWidgets([
            QLabel(self.tr("Name")), QLineEdit(),
            QLabel(self.tr("Type")), QLineEdit(readOnly = True, text = "Reb"),
            QLabel(self.tr("Description")), QLineEdit(),
            QLabel(self.tr("Flag File")), FileLineEdit()
        ])
        
        self.addWidget(identity_subsection)
    
    def addVehicles(self):
        vehicle_subsection = SingleColumnSubSection(self.tr("Vehicles"))
        military_subsection = MultiColumnSubSection(self.tr("Military Vehicles"), 3)
        civilian_subsection = MultiColumnSubSection(self.tr("Civilian Vehicles"), 3)
        static_subsection = MultiColumnSubSection(self.tr("Statics"), 2)
        
        military_subsection.addWidgets([
            MultiLineLabelledEdit(
                self.tr("Basic"),
                MultiLineParams(self.tr("Vehicle Classes"), 2),
                MultiLineParams(self.tr("Price"), default_value = 100, is_int = True)
            ),
            MultiLineLabelledEdit(
                self.tr("Armed"),
                MultiLineParams(self.tr("Vehicle Classes"), 2),
                MultiLineParams(self.tr("Price"), default_value = 100, is_int = True)
            ),
            MultiLineLabelledEdit(
                self.tr("Unarmed"),
                MultiLineParams(self.tr("Vehicle Classes"), 2),
                MultiLineParams(self.tr("Price"), default_value = 100, is_int = True)
            ),
            MultiLineLabelledEdit(
                self.tr("Trucks"),
                MultiLineParams(self.tr("Vehicle Classes"), 2),
                MultiLineParams(self.tr("Price"), default_value = 100, is_int = True)
            ),
            MultiLineLabelledEdit(
                self.tr("AA Vehicles"),
                MultiLineParams(self.tr("Vehicle Classes"), 2),
                MultiLineParams(self.tr("Price"), default_value = 100, is_int = True)
            ),
            MultiLineLabelledEdit(
                self.tr("AT Vehicles"),
                MultiLineParams(self.tr("Vehicle Classes"), 2),
                MultiLineParams(self.tr("Price"), default_value = 100, is_int = True)
            ),
            MultiLineLabelledEdit(
                self.tr("Boats"),
                MultiLineParams(self.tr("Vehicle Classes"), 2),
                MultiLineParams(self.tr("Price"), default_value = 100, is_int = True)
            ),
            MultiLineLabelledEdit(
                self.tr("Planes"),
                MultiLineParams(self.tr("Vehicle Classes"), 2),
                MultiLineParams(self.tr("Price"), default_value = 100, is_int = True)
            ),
            MultiLineLabelledEdit(
                self.tr("Medical"),
                MultiLineParams(self.tr("Vehicle Classes"), 2),
                MultiLineParams(self.tr("Price"), default_value = 100, is_int = True)
            ),
            QWidget() # Spacer
        ])
        
        civilian_subsection.addWidgets([
            MultiLineLabelledEdit(
                self.tr("Basic"),
                MultiLineParams(self.tr("Vehicle Classes"), 2),
                MultiLineParams(self.tr("Price"), default_value = 100, is_int = True)
            ),
            MultiLineLabelledEdit(
                self.tr("Trucks"),
                MultiLineParams(self.tr("Vehicle Classes"), 2),
                MultiLineParams(self.tr("Price"), default_value = 100, is_int = True)
            ),
            MultiLineLabelledEdit(
                self.tr("Helicopters"),
                MultiLineParams(self.tr("Vehicle Classes"), 2),
                MultiLineParams(self.tr("Price"), default_value = 100, is_int = True)
            ),
            MultiLineLabelledEdit(
                self.tr("Planes"),
                MultiLineParams(self.tr("Vehicle Classes"), 2),
                MultiLineParams(self.tr("Price"), default_value = 100, is_int = True)
            ),
            MultiLineLabelledEdit(
                self.tr("Supply Vehicles"),
                MultiLineParams(self.tr("Vehicle Classes"), 2),
                MultiLineParams(self.tr("Price"), default_value = 100, is_int = True)
            ),
            QWidget() # Spacer
        ])
        
        vehicle_subsection.addWidgets([
            military_subsection,
            civilian_subsection
        ])
        
        self.addWidget(vehicle_subsection)

class ModSection(Collapsible):
    def __init__(self, main_window: QWidget):
        super().__init__(main_window, "Mod Information")        
        self.addInfo()
        
    def addInfo(self) -> None:   
        pass