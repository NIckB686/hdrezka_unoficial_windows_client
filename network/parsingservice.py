import logging
import re

from bs4 import BeautifulSoup

from network.models import InlineItem, PageMeta

logger = logging.getLogger(__name__)


class ParsingService:
    @staticmethod
    def get_cards(html: str) -> list[InlineItem] | None:
        soup = BeautifulSoup(html, 'lxml')
        return _CardsExtractor.extract_cards(soup)

    @staticmethod
    def get_movie_page(html: str) -> PageMeta | None:
        soup = BeautifulSoup(html, 'lxml')
        return _DetailsPageExtractor.extract_page(soup)


class _CardsExtractor:
    @staticmethod
    def extract_cards(soup) -> list[InlineItem]:
        if soup is None:
            logger.warning("Soup is None - карточки не получены")
            return []

        cards_root = soup.find(class_="b-content__inline_items") or soup.find(
            class_="b-sidelist"
        )
        if not cards_root:
            logger.warning("Карточки не найдены")
            return []

        metas = []
        for card in cards_root.find_all(class_="b-content__inline_item"):
            metas.append(_CardsExtractor._build_movie_meta(card))
        return metas

    @staticmethod
    def _build_movie_meta(card) -> InlineItem:
        cover = card.find(class_="b-content__inline_item-cover")
        url = cover.find("a").get("href")
        img_url = cover.find("img").get("src")

        bottom = card.find(class_="b-content__inline_item-link")
        title = bottom.find("a").get_text(strip=True)
        year = bottom.find("div").get_text(strip=True)

        logger.debug("Создана мета карточки")
        return InlineItem(url, img_url, title, year)


class _DetailsPageExtractor:
    @staticmethod
    def extract_page(soup: BeautifulSoup) -> PageMeta | None:
        if not soup:
            logger.warning("Soup пуст - невозможно извлечь страницу")
            return None

        soup = soup.find(class_='b-content__main')

        info_table = soup.find(class_="b-post__infotable clearfix")
        if not info_table:
            logger.warning("Блок информации о фильме не найден")
            return None

        title = soup.find(class_="b-post__title").get_text()
        if title:
            logger.warning(title)
        orig_title = soup.find(class_="b-post__origtitle").get_text()
        if orig_title:
            logger.warning(orig_title)
        poster_url = info_table.find("img").get("src")
        table = str(info_table.find(class_="b-post__infotable_right"))
        description = str(soup.find(class_="b-post__description"))

        table = _DetailsPageExtractor._normalize_html(table)
        description = _DetailsPageExtractor._normalize_html(description)

        cards = _CardsExtractor.extract_cards(soup)

        return PageMeta(
            title=title,
            orig_title=orig_title,
            poster_url=poster_url,
            table=table,
            description=description,
            cards=cards,
        )

    @staticmethod
    def _normalize_html(text: str) -> str:
        return re.sub(
            r"</(h[1-6])>\s*([:;,.?!])", r"\2</\1>", string=text, flags=re.IGNORECASE
        )
