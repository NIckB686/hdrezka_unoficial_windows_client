import sys

from PySide6.QtWidgets import QWidget, QStackedWidget, QApplication, QVBoxLayout

from ui.main_page import MainPage


class Ui_MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.stackedWidget = StackedWidget()

        self.layout.addWidget(self.stackedWidget)


class StackedWidget(QStackedWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self.main_page = MainPage(self)
        self.addWidget(self.main_page)

        self.setCurrentIndex(0)

    def change_page(self, widget: QWidget) -> None:
        self.setCurrentWidget(widget)


def main():
    app = QApplication([])
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
