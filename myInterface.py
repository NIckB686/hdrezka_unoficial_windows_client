import sys

from PySide6.QtWidgets import QWidget, QStackedWidget, QHBoxLayout, QScrollArea, \
    QApplication, QVBoxLayout

from main_page import MainPage


class Ui_MainWindow(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.layout = QVBoxLayout(self)
        self.stackedWidget = StackedWidget()

        self.layout.addWidget(self.stackedWidget)


class StackedWidget(QStackedWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.main_page = MainPage(self)
        self.addWidget(self.main_page)

        self.setCurrentIndex(0)

    def change_page(self, index: int) -> None:
        self.setCurrentIndex(index)


class SettingsPage(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.layout = QHBoxLayout(self)

        self.settings_menu_scroll_area = QScrollArea(self)
        self.settings_menu_content = QWidget(self)
        self.settings_menu_scroll_area.setWidget(self.settings_menu_content)
        self.layout.addWidget(self.settings_menu_scroll_area)

        self.settings_body_scroll_area = QScrollArea(self)
        self.settings_body_content = QWidget(self)
        self.settings_body_scroll_area.setWidget(self.settings_body_content)
        self.layout.addWidget(self.settings_body_scroll_area)


def main() -> None:
    app = QApplication([])
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
