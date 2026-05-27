from PySide6.QtWidgets import QWidget

def resize_to_parent(
        widget: QWidget,
        width: float = 1,
        height: float = 1,
        x: float = 0,
        y: float = 0
):
    parent = widget.parentWidget()
    widget.setGeometry(
        int(parent.width() * x),
        int(parent.height() * y),
        int(parent.width() * width),
        int(parent.height() * height)
    )