from . import Gif
from .base import BaseGeneratorClass


class GifSearch(BaseGeneratorClass):
    _RESULT_ATTR = "gifs"

    def __init__(self, search_term, client, pages=1, cursor=None, wait_time=2):
        super().__init__()
        self.term = search_term
        self.client = client
        self.pages = pages
        self.cursor = cursor
        self.wait_time = wait_time
        self.is_next_page = True
        self.gifs = []

    def get_page(self, cursor):
        _gifs = []
        response = self.client.http.gif_search(self.term, cursor)

        if not response.get('data'):
            return _gifs

        items = response.get('data', {}).get('items', [])
        for item in items:
            _gifs.append(Gif(self.client, item))

        cursor = response.get('cursor', {}).get('next')
        cursor_top = self._get_cursor_(response, "Top")

        return _gifs, cursor, cursor_top

    def __repr__(self):
        return f"GifSearch(count={self.__len__()})"



