import asyncio

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QHBoxLayout, QGridLayout

from network.aiorequests import gateway


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

        self.info_table_layout.addWidget(self.poster)

        self.main_layout.addLayout(self.info_table_layout)
        self.wrapper_layout.addLayout(self.main_layout)

        self.setWidget(self.content_widget)

    def load_page(self):
        ...

    async def _load_poster(self):
        data = await self.gw.request(self.url)
        pix = QPixmap()
        pix.loadFromData(data)
        self.poster.setPixmap(pix)
