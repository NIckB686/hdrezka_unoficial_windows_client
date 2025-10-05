from models import Genre


class URLBuilder:
    @staticmethod
    def build_url(genre: Genre = '', subgenre='', best: bool = False, filter_='watching', year='') -> str:
        base_url = 'https://rezka.ag'
        return f'{base_url}{genre}{'/best' if best else ''}{subgenre}{'' if year else f'/?filter={filter_}'}{year}'