from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout, QLabel


class CardFrameWidget(QFrame):
    clicked = Signal()

    def __init__(self, name: str, text: str, link: str) -> None:
        super().__init__()
        self._setup_ui(name, text)
        self.url = link

    def _setup_ui(self, name: str, text: str) -> None:
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)
        self.setFixedWidth(171)
        self.setContentsMargins(5, 5, 5, 5)
        self.layout = QVBoxLayout(self)

        self._poster = QLabel()
        self._poster.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self._poster.setFixedSize(166, 250)

        self._title = QLabel(name)
        self._title.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        self._title.setWordWrap(True)

        self._attrs = QLabel(text)
        self._attrs.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.layout.addWidget(self._poster, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self._title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self._attrs, alignment=Qt.AlignmentFlag.AlignCenter)

    def set_pixmap(self, pixmap: QPixmap):
        self._poster.setPixmap(pixmap)

    def set_error(self):
        self._poster.setText('❌')