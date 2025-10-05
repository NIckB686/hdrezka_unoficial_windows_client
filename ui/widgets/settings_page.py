from PySide6.QtWidgets import QScrollArea, QWidget, QHBoxLayout


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self.layout = QHBoxLayout(self)

        self.settings_menu_scroll_area = QScrollArea(self)
        self.settings_menu_content = QWidget(self)
        self.settings_menu_scroll_area.setWidget(self.settings_menu_content)
        self.layout.addWidget(self.settings_menu_scroll_area)

        self.settings_body_scroll_area = QScrollArea(self)
        self.settings_body_content = QWidget(self)
        self.settings_body_scroll_area.setWidget(self.settings_body_content)
        self.layout.addWidget(self.settings_body_scroll_area)
