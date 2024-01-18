from . import Gif
from .base import BaseGeneratorClass


class GifSearch(BaseGeneratorClass):
    def __init__(self, search_term, client, pages=1, cursor=None, wait_time=2):
        super().__init__()
        self.term = search_term
        self.client = client
        self.pages = pages
        self.cursor = cursor
        self.wait_time = wait_time
        self.is_next_page = True
        self.results = []

    def get_next_page(self):
        _gifs = []
        if self.is_next_page:
            response = self.client.http.gif_search(self.term, self.cursor)

            if not response.get('data'):
                return _gifs

            self.cursor = response.get('cursor', {}).get('next')
            items = response.get('data', {}).get('items', [])
            for item in items:
                _gifs.append(Gif(self.client, item))

            self.results.extend(_gifs)
            self['gifs'] = self.results
            self['cursor'] = self.cursor

        return self, _gifs

    def __getitem__(self, index):
        if isinstance(index, str):
            return getattr(self, index)

        return self.results[index]

    def __iter__(self):
        for __tweet in self.results:
            yield __tweet

    def __len__(self):
        return len(self.results)

    def __repr__(self):
        return f"GifSearch(count={self.__len__()})"



