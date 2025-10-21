from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QLabel,
    QHBoxLayout,
    QSizePolicy,
    QLayout,
)

from ui.widgets.models import AbstractScrollArea


class DetailsPage(QScrollArea):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.content_widget = QWidget()
        self.centered_content = QHBoxLayout(self.content_widget)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = QLabel()
        self.title.setWordWrap(True)

        self.orig_title = QLabel()
        self.orig_title.setWordWrap(True)

        self.info_table_layout = QHBoxLayout()
        self.info_table_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.poster = QLabel()
        self.poster.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.poster.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.poster.setFixedWidth(400)

        self.info_table = QLabel()
        self.info_table.setFixedWidth(500)
        self.info_table.setWordWrap(True)
        self.info_table.setTextFormat(Qt.TextFormat.RichText)

        self.info_table_layout.addWidget(self.poster)
        self.info_table_layout.addWidget(self.info_table)

        self.description = QLabel()
        self.description.setTextFormat(Qt.TextFormat.RichText)
        self.description.setWordWrap(True)

        self.watch_also_container = QWidget()
        self.watch_also_container_layout = QVBoxLayout(self.watch_also_container)
        self.watch_also = WatchAlsoScrollArea()
        self.watch_also_container_layout.addWidget(self.watch_also)

        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.orig_title)
        self.main_layout.addLayout(self.info_table_layout)
        self.main_layout.addWidget(self.description)
        self.main_layout.addWidget(self.watch_also_container)

        self.centered_content.addStretch()
        self.centered_content.addLayout(self.main_layout)
        self.centered_content.addStretch()

        self.setWidget(self.content_widget)
        self.setWidgetResizable(True)

    def set_title(self, text: str):
        self.title.setText(text)

    def set_orig_title(self, text: str):
        self.orig_title.setText(text)

    def set_poster(self, pixmap: QPixmap):
        self.poster.setPixmap(pixmap)

    def set_description_text(self, text: str):
        self.description.setText(text)

    def set_table_text(self, text: str):
        self.info_table.setText(text)


class WatchAlsoScrollArea(AbstractScrollArea):
    def __init__(self):
        super().__init__(disable_vertical_scrollbar=True)
        self.setFixedHeight(400)

    def get_layout(self) -> QLayout:
        return QHBoxLayout()

    def add_card(self) -> Callable:
        return lambda widget: self.content_layout.addWidget(widget)
