from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QLineEdit, QSizePolicy, QWidget, QScrollArea, \
    QGridLayout, QVBoxLayout

from ui.card_frame_widget import CardFrameWidget


class MainHeaderWidget(QFrame):
    menu_clicked = Signal()
    continue_clicked = Signal()
    profile_clicked = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        self.main_layout.setSpacing(6)

        self.menu_btn = QPushButton(self)
        self.menu_btn.setText('Меню')
        self.menu_btn.clicked.connect(self.menu_clicked)

        self.searchbar = QLineEdit(self)
        self.searchbar.setPlaceholderText('Поиск')
        self.searchbar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.bookmarks_btn = QPushButton(self)
        self.bookmarks_btn.setText('Закладки')

        self.continue_btn = QPushButton(self)
        self.continue_btn.setText('Досмотреть')
        self.continue_btn.clicked.connect(self.continue_clicked)

        self.profile_btn = QPushButton(self)
        self.profile_btn.setText('Профиль')
        self.profile_btn.clicked.connect(self.profile_clicked)

        self.center_box = QWidget()
        self.center_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.center_layout = QHBoxLayout(self.center_box)
        self.center_layout.setContentsMargins(0, 0, 0, 0)
        self.center_layout.addStretch()
        self.center_layout.addWidget(self.searchbar)
        self.center_layout.addStretch()

        self.main_layout.addWidget(self.menu_btn)
        self.main_layout.addWidget(self.center_box, 1)
        self.main_layout.addWidget(self.bookmarks_btn)
        self.main_layout.addWidget(self.continue_btn)
        self.main_layout.addWidget(self.profile_btn)


class MainBodyScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.row = 0
        self.col = 0
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout(self.main_widget)

        self.center_widget = QWidget()

        self.content_layout = QGridLayout(self.center_widget)
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        self.main_layout.addStretch()
        self.main_layout.addWidget(self.center_widget)
        self.main_layout.addStretch()

        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)

    def add_card(self, card: CardFrameWidget) -> None:
        card.clicked.connect(self.connect_card_clicked_signal)
        self.content_layout.addWidget(card, self.row, self.col)
        self.col += 1
        if self.col == 4:
            self.row += 1
            self.col = 0

    def connect_card_clicked_signal(self):
        ...

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


class MainPage(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.layout = QVBoxLayout(self)

        self.header = MainHeaderWidget(self)

        self.body_widget = QWidget()
        self.body_layout = QHBoxLayout(self.body_widget)
        self.body_layout.setContentsMargins(0, 0, 0, 0)

        self.side_menu = SideMenu()
        self.cards_container = MainBodyScrollArea(self)
        self.cards_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.body_layout.addWidget(self.side_menu)
        self.body_layout.addWidget(self.cards_container)

        self.layout.addWidget(self.header)
        self.layout.addWidget(self.body_widget)


class SideMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.settings_btn = QPushButton('Настройки')

        layout.addWidget(self.settings_btn, alignment=Qt.AlignmentFlag.AlignLeft)

