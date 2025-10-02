from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QApplication, QHBoxLayout, QLabel, QFormLayout


class ViewPage(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.scroll_body = _ScrollBody()

        self.layout.addWidget(self.scroll_body)


class _ScrollBody(QScrollArea):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self.content_widget = QWidget()
        self.main_layout = QVBoxLayout(self.content_widget)

        self.info_widget = QWidget()
        self.info_layout = QHBoxLayout(self.info_widget)
        self.poster = QLabel()
        self.attrs_layout = QFormLayout()
        self.info_layout.addWidget(self.poster)
        self.info_layout.addLayout(self.attrs_layout)

        self.description_widget = QWidget()

        self.trailer_widget = QWidget()

        self.watch_widget = QWidget()

        self.also_watch_widget = QWidget()

        self.main_layout.addWidget(self.info_widget)
        self.main_layout.addWidget(self.description_widget)
        self.main_layout.addWidget(self.trailer_widget)
        self.main_layout.addWidget(self.watch_widget)
        self.main_layout.addWidget(self.also_watch_widget)

        self.setWidget(self.content_widget)


if __name__ == '__main__':
    app = QApplication()
    window = ViewPage()
    window.show()
    app.exec()
