import json
import logging
import urllib.parse

from network.errors import WrongLoginError
from network.aiorequests import HTTPClient

logger = logging.getLogger(__name__)


class MovieGateway:
    LOGIN_URL = 'https://rezka.ag/ajax/login/'
    PRE_SEARCH_URL = 'https://rezka.ag/engine/ajax/search.php'

    def __init__(self, http: HTTPClient):
        self.http = http

    async def pre_search(self, query: str) -> bytes | None:
        return await self.http.post(self.PRE_SEARCH_URL, data={'q': query})

    async def search(self, query: str) -> bytes | None:
        encoded = urllib.parse.quote(query)
        url = f'https://rezka.ag/search/?do=search&subaction=search&q={encoded}'
        return await self.http.get(url)

    async def global_login(self, login: str, password: str, not_save: bool) -> None:
        data = {
            'login_name': login,
            'login_password': password,
            'login_not_save': int(not_save)
        }
        res = await self.http.post(self.LOGIN_URL, data=data)
        res = json.loads(res)
        if not res['success']:
            raise WrongLoginError

