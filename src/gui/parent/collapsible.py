import logging

from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout,
    QLabel, QScrollArea, QHBoxLayout,
    QLayout, QSizePolicy
)
from PySide6.QtCore import (
    Qt, QSize
)

from ...shared.helpers import getTheme, getFonts

class Collapsible(QWidget):
    def __init__(
            self,
            main_window: QWidget,
            title = "Title",
            start_collapsed = True
        ):
        super().__init__(main_window)
        self.theme = getTheme()
        self.fonts = getFonts()
        self.title = title
        
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        
        # Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(1, 1, 1, 1)
        self.main_layout.setSpacing(2)
        
        # Widgets
        self.scroll_area = CollapsibleScrollArea(self)
        
        self.toggle_button = QPushButton(
            ("▼ " if not start_collapsed else "▶ ") + self.title.upper()
        )
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(not start_collapsed)
        self.toggle_button.clicked.connect(self.scroll_area.toggle)
        self.toggle_button.setFont(self.fonts.bold)
        
        # Adding widgets to layout
        self.main_layout.addWidget(self.toggle_button)
        self.main_layout.addWidget(self.scroll_area, 2)
        
        if start_collapsed:
            self.scroll_area.hide()
        
        self._setDesign()
    
    def _setDesign(self):
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme.button.normal};
                color: {self.theme.text.primary};
                text-align: left;
                padding: 8px;
                border: none;
                border-radius: {self.theme.border.radius};
            }}
            
            QPushButton:checked {{
                background-color: {self.theme.button.checked};
            }}
            
            QPushButton:hover {{
                background-color: {self.theme.button.hovered};
            }}
            
            QPushButton:checked:hover {{
                background-color: {self.theme.button.hovered_checked};
            }}
        """)
    
    def sizeHint(self):
        button_h = self.toggle_button.sizeHint().height()
        button_w = self.toggle_button.sizeHint().width()
        
        if self.scroll_area.isVisible():
            body = self.scroll_area.widget().sizeHint()
            
            return QSize(
                max(button_w, body.width()),
                button_h + body.height()
            )
        
        return super().sizeHint()

    def minimumSizeHint(self):
        h = self.toggle_button.sizeHint().height()
        w = self.toggle_button.sizeHint().width()
        
        return QSize(w, h)

    def addWidget(self, widget: QWidget):
        self.scroll_area.content.addWidget(widget)
    
    def addWidgets(self, widgets: list[QWidget]):
        for widget in widgets:
            self.addWidget(widget)

class CollapsibleScrollArea(QScrollArea):
    def __init__(self, parent: Collapsible):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        
        self.content = CollapsibleSplitContent(self)
        
        self.setWidget(self.content)
        self.setWidgetResizable(True)
        
        self.setDesign()
        
    def toggle(self):
        current : Collapsible = self.parentWidget()
        main_window = current.parentWidget()
        is_open = self.isVisible()     
           
        for collapsible in main_window.findChildren(Collapsible):
            collapsible : Collapsible = collapsible
            
            if collapsible is current:
                current.toggle_button.setText(
                    "▶ " + collapsible.title.upper() if is_open
                    else "▼ " + collapsible.title.upper()
                )
                
                self.setVisible(not self.isVisible())
                self.parentWidget().updateGeometry()
                continue
            
            if collapsible.scroll_area.isVisible():
                collapsible.toggle_button.setText(
                    "▶ " + collapsible.title.upper()
                )
                
                collapsible.scroll_area.setVisible(False)
                collapsible.toggle_button.setChecked(False)

        self.logger.info(f"{'Collapsing' if is_open else 'Expanding'} '{collapsible.title.lower()}'")
    
    def setDesign(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)

class CollapsibleSplitContent(QWidget):
    def __init__(self, parent: CollapsibleScrollArea):
        super().__init__(parent)
        self.theme = getTheme()
        self.columns: list[QVBoxLayout] = []
        
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
    
    def setDesign(self):
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet(f"""
            CollapsibleContent {{
                background-color: {self.theme.background.surface};
                border-radius: {self.theme.border.radius};
            }}
        """)
    
    def addWidget(self, widget: QWidget):
        self.main_layout.addWidget(widget)