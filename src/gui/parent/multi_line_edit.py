from dataclasses import dataclass

from PySide6.QtWidgets import (
    QWidget, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent, QIntValidator

from ...shared.helpers import getTheme

@dataclass
class MultiLineParams:
    label: str
    stretch: int = 1
    default_value: str | int = None
    is_int: bool = False

class MultiLineController:
    def __init__(self):
        super().__init__()
        self.columns: dict[int, MultiLineColumn] = {}
    
    def get_last_rows(self) -> list[LineRow]:
        return [
            next(reversed(column.rows.values()))
            for column in self.columns.values()
            if column.rows
        ]
    
    def is_any_empty(self, rows: list[LineRow]) -> bool:
        return any(not row.text().strip() for row in rows)
    
    def add_rows(self):
        last_rows = self.get_last_rows()
        
        for column in self.columns.values():
            if self.is_any_empty(last_rows): return
            
            count = len(column.rows)
            row = LineRow(column)
            if column.is_int:
                row.setValidator(QIntValidator())
            
            column.rows[count + 1] = row
            column.main_layout.addWidget(row)
            
            # Add default value if present.
            if column.default_value:
                row.setText(str(column.default_value))
    
    def get_data(self):
        data = {}
        
        for idx, column in self.columns.items():
            label = column.label.text()
            
            for row_idx, row in column.rows.items():
                if row_idx not in data:
                    data[row_idx] = {}
                
                data[row_idx][label] = row.text().strip()
        
        return data

class MultiLineEdit(QWidget, MultiLineController):
    def __init__(self, *params: MultiLineParams):
        super().__init__()
        self.theme = getTheme()
                
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        
        count = 0
        for param in params:
            column = MultiLineColumn(
                self,
                param.label,
                param.default_value,
                param.is_int
            )
            self.main_layout.addWidget(column, param.stretch)
            self.columns[count] = column
            count += 1
        
        self.add_rows()
        self._add_design()
    
    def _add_design(self):
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet(f"""
            MultiLineEdit {{
                border: 2px solid {self.theme.button.checked};
            }}
        """)

class MultiLineLabelledEdit(QWidget, MultiLineController):
    def __init__(self, title: str, *params: MultiLineParams):
        super().__init__()
        self.theme = getTheme()
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        
        self.main_layout.addWidget(QLabel(title), alignment = Qt.AlignmentFlag.AlignCenter)
        
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(5, 5, 5, 5)
        self.content_layout.setSpacing(5)
        self.main_layout.addLayout(self.content_layout)
        
        count = 0
        for param in params:
            column = MultiLineColumn(
                self,
                param.label,
                param.default_value,
                param.is_int
            )
            self.content_layout.addWidget(column, param.stretch)
            self.columns[count] = column
            count += 1
        
        self.add_rows()
        self._add_design()
    
    def _add_design(self):
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet(f"""
            MultiLineEdit {{
                border: 2px solid {self.theme.button.checked};
            }}
        """)

class MultiLineColumn(QWidget):
    def __init__(
            self,
            parent: MultiLineEdit,
            label: str,
            default_value: str | int | None = None,
            is_int: bool = False
    ):
        super().__init__(parent)
        self.default_value = default_value
        self.is_int = is_int
        
        self.rows: dict[int, LineRow] = {}
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(5)
        
        self.label = QLabel(label, alignment = Qt.AlignmentFlag.AlignCenter)
        
        self.main_layout.addWidget(self.label)

class LineRow(QLineEdit):
    def __init__(self, parent: MultiLineColumn):
        super().__init__(parent)
    
    def is_empty(self):
        return not self.text().strip()
    
    def keyPressEvent(self, e: QKeyEvent):
        column: MultiLineColumn = self.parentWidget()
        controller: MultiLineController = column.parentWidget()
        
        match e.key():
            # If the last row in the column is empty, don't add rows to each column.
            case Qt.Key.Key_Return | Qt.Key.Key_Enter:
                last_row: LineRow = next(reversed(column.rows.values()))
                if last_row.is_empty(): return
                controller.add_rows()
        
        return super().keyPressEvent(e)