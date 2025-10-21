class HDRezkaError(Exception):
    __slots__ = ()


class WrongLoginError(HDRezkaError):
    __slots__ = ()


class NotImgUrlError(HDRezkaError):
    __slots__ = ()


class HTTPError(HDRezkaError):
    __slots__ = ()


class HTTPMaxRetriesError(HTTPError):
    def __init__(self, url: str, cause: Exception):
        super().__init__(f'Request failed for {url}: {cause}')
