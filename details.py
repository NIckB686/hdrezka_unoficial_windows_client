from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea


class ViewPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.header = QWidget()
        self.scroll_body = _ScrollBody()


class _ScrollBody(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        self.content_widget = QWidget()
        self.info = QWidget()
        self.attrs = QWidget()
        self.description = QWidget()
        self.trailer = ...
        self.watch = QWidget()
        self.also_watch_widget = QWidget()

        self.setWidget(self.content_widget)