from PySide6.QtWidgets import (
    QWidget, QTextEdit, QHBoxLayout,
    QVBoxLayout, QLabel, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QFontMetrics, QColor, QTextFormat,
    QKeyEvent, QFocusEvent, QTextCursor
)

from ..helpers import ThemeDict
from ..models import Fonts

class MultiItemTextEdit(QWidget):
    def __init__(self, main_window: QWidget):
        super().__init__(main_window)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(5)
        
        self.left = RequiredFieldWidget(main_window, self)
        self.right = ControlledFieldWidget(main_window, self)
        
        self.main_layout.addWidget(self.left, 2)
        self.main_layout.addWidget(self.right)
            
    def fill_next(self, source: ExpandingTextEdit) -> None:
        if source != self.left.text_edit:
            return
        
        self.right.text_edit.appendText("100\n")
    
    def highlight_next(self, source: ExpandingTextEdit, line_number: int) -> None:
        if source == self.left.text_edit:
            self.right.text_edit.highlight_at_number(line_number)
        
        elif source == self.right.text_edit:
            self.left.text_edit.highlight_at_number(line_number)
    
    def unfocus_next(self, source: ExpandingTextEdit) -> None:
        if source == self.left.text_edit:
            self.right.text_edit._focused = False
            self.right.text_edit.setExtraSelections([])
            
        elif source == self.right.text_edit:
            self.left.text_edit._focused = False
            self.left.text_edit.setExtraSelections([])

class ExpandingTextEdit(QTextEdit):
    def __init__(self, main_window: QWidget, parent: QWidget):
        super().__init__(parent)
        self.theme : ThemeDict = main_window.theme
        self.base : MultiItemTextEdit = parent
        self._focused = False
        
        self.textChanged.connect(self.update_height)
        self.cursorPositionChanged.connect(self.highlight_line)
        
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.update_height(1)
        
    def update_height(self, lines = None) -> None:
        if not lines:
            lines = len(self.toPlainText().split("\n"))

        fm = QFontMetrics(self.font())
        f_height = fm.height()
        self.setFixedHeight(f_height * (lines + 1))
    
    def highlight_at_number(self, line_num: int) -> None:
        doc = self.document()
        line_number = max(0, min(line_num, doc.blockCount() - 1))
        
        block = doc.findBlockByLineNumber(line_number)
        if not block.isValid():
            return
        
        selections = []
        selection = QTextEdit.ExtraSelection()
        
        line_colour = QColor(self.theme.text.highlight)
        
        selection.format.setBackground(line_colour)
        selection.format.setProperty(
            QTextFormat.Property.FullWidthSelection,
            True
        )
        
        cursor = QTextCursor(block)
        cursor.clearSelection()
        selection.cursor = cursor
        
        selections.append(selection)
        self.setExtraSelections(selections)
    
    def highlight_line(self) -> None:
        if not self._focused or self.isReadOnly():
            return
        
        selections = []
        selection = QTextEdit.ExtraSelection()
        
        line_colour = QColor(self.theme.text.highlight)
        
        selection.format.setBackground(line_colour)
        selection.format.setProperty(
            QTextFormat.Property.FullWidthSelection,
            True
        )
        
        cursor = self.textCursor()
        line_number = cursor.blockNumber()
        cursor.clearSelection()
        selection.cursor = cursor
        
        selections.append(selection)
        
        self.setExtraSelections(selections)
        
        self.base.highlight_next(self, line_number)
    
    def get_line_count(self) -> int:
        return len(self.toPlainText().split("\n"))
    
    def appendText(self, text: str) -> None:
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.select(QTextCursor.SelectionType.LineUnderCursor)
        line_text = cursor.selectedText().strip()
        cursor.clearSelection()
        
        if line_text:
            cursor.insertText("\n")
        else:
            cursor.insertText(text)
        
        self.base.fill_next(self)
    
    def keyPressEvent(self, e: QKeyEvent):
        if e.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            cursor = self.textCursor()
            cursor.select(QTextCursor.SelectionType.LineUnderCursor)
            line_text = cursor.selectedText().strip()
            
            if not line_text:
                return
            else:
                self.base.fill_next(self)
        
        return super().keyPressEvent(e)
    
    def focusInEvent(self, e: QFocusEvent):
        self._focused = True
        self.highlight_line()
        return super().focusInEvent(e)
    
    def focusOutEvent(self, e: QFocusEvent):
        self._focused = False
        self.setExtraSelections([])
        self.base.unfocus_next(self)
        
        return super().focusOutEvent(e)

class RequiredFieldTextEdit(ExpandingTextEdit):
    def __init__(self, main_window: QWidget, parent: MultiItemTextEdit):
        super().__init__(main_window, parent)
    
class ControlledFieldTextEdit(ExpandingTextEdit):
    def __init__(self, main_window: QWidget, parent: MultiItemTextEdit):
        super().__init__(main_window, parent)
    
    def keyPressEvent(self, e: QKeyEvent):
        if not e.text().isdigit():
            e.ignore()
            return
        
        return super().keyPressEvent(e)

class RequiredFieldWidget(QWidget):
    def __init__(self, main_window: QWidget, parent: MultiItemTextEdit):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(5)
        
        self.label = QLabel(self.tr("Classes"), alignment = Qt.AlignmentFlag.AlignCenter)
        self.text_edit = RequiredFieldTextEdit(main_window, parent)
        
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.text_edit)
        
class ControlledFieldWidget(QWidget):
    def __init__(self, main_window: QWidget, parent: MultiItemTextEdit):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(5)
        
        self.label = QLabel(self.tr("Price"), alignment = Qt.AlignmentFlag.AlignCenter)
        self.text_edit = ControlledFieldTextEdit(main_window, parent)
        
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.text_edit)