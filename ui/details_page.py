import asyncio

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QHBoxLayout, QGridLayout, QApplication

from network_layer import gateway


class DetailsPageScrollArea(QScrollArea):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.gw = gateway
        self._setup_ui()


    def _setup_ui(self):
        self.content_widget = QWidget()
        self.wrapper_layout = QHBoxLayout(self.content_widget)
        self.main_layout = QVBoxLayout()

        self.info_table_layout = QGridLayout()

        self.poster = QLabel()
        asyncio.create_task(self._load_poster())

        self.info_table_layout.addWidget(self.poster, 1, 1)

        self.main_layout.addLayout(self.info_table_layout)
        self.wrapper_layout.addLayout(self.main_layout)

        self.setWidget(self.content_widget)

    async def _load_poster(self):
        data = await self.gw.request(self.url)
        pix = QPixmap()
        pix.loadFromData(data)
        self.poster.setPixmap(pix)

if __name__ == '__main__':
    app = QApplication()
    window = DetailsPageScrollArea('https://rezka.ag/films/thriller/79790-poyman-s-polichnym-2025-latest.html')
    window.show()


