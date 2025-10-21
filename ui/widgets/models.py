from abc import ABCMeta, abstractmethod
from typing import Callable

from PySide6.QtCore import QObject, Qt, Signal, Slot
from PySide6.QtWidgets import QHBoxLayout, QLayout, QScrollArea, QSizePolicy, QWidget

from network.client import HDRezkaClient
from network.url_builder import URLBuilder
from ui.cards_factory import CardsFactory


class QtABCMeta(type(QObject), ABCMeta):
    pass


class AbstractScrollArea(QScrollArea, metaclass=QtABCMeta):
    card_clicked = Signal(str)

    def __init__(
            self,
            url: str = URLBuilder.build_url(),
            disable_horizontal_scrollbar: bool = False,
            disable_vertical_scrollbar: bool = False,
    ):
        super().__init__()
        self.url = url
        self.cards_factory = CardsFactory()
        self.api = HDRezkaClient()
        if disable_vertical_scrollbar:
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        if disable_horizontal_scrollbar:
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._setup_ui()
        self.connect_signals()

    def _setup_ui(self) -> None:
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout(self.main_widget)

        self.center_widget = QWidget()
        self.center_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )

        self.content_layout = self.get_layout()
        self.content_layout.setSpacing(10)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        self.center_widget.setLayout(self.content_layout)

        self.main_layout.addStretch()
        self.main_layout.addWidget(self.center_widget)
        self.main_layout.addStretch()

        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)

    @abstractmethod
    def get_layout(self) -> QLayout:
        ...

    def connect_signals(self):
        self.cards_factory.new_card.connect(self.add_card())

    @abstractmethod
    def add_card(self) -> Callable:
        ...

    @Slot(str)
    def on_card_clicked(self, url: str):
        self.card_clicked.emit(url)

    @Slot(QWidget)
    def remove_widget(self, widget: QWidget) -> None:
        self.content_layout.removeWidget(widget)
        widget.setParent(None)
        widget.deleteLater()

    def clear(self) -> None:
        while (child := self.content_layout.takeAt(0)) is not None:
            w = child.widget()
            if w:
                w.setParent(None)
                w.deleteLater()
