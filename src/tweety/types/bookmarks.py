from .twDataTypes import Tweet, Excel
from .base import BaseGeneratorClass


class Bookmarks(BaseGeneratorClass):
    _RESULT_ATTR = "tweets"

    def __init__(self, user_id, client, pages=1, wait_time=2, cursor=None):
        super().__init__()
        self.tweets = []
        self.cursor = cursor
        self.cursor_top = cursor
        self.is_next_page = True
        self.client = client
        self.user_id = user_id
        self.pages = pages
        self.wait_time = wait_time

    def get_page(self, cursor):
        _tweets = []
        response = self.client.http.get_bookmarks(cursor=cursor)

        entries = self._get_entries(response)
        for entry in entries:
            try:
                parsed = Tweet(self.client, entry, response)
                if parsed:
                    self.tweets.append(parsed)
                    _tweets.append(parsed)
            except:
                pass

        cursor = self._get_cursor_(response)
        cursor_top = self._get_cursor_(response, "Top")

        return _tweets, cursor, cursor_top

    def to_xlsx(self, filename=None):
        return Excel(self, filename)

