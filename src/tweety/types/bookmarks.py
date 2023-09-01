from . import Tweet, Excel
from .base import BaseGeneratorClass


class Bookmarks(BaseGeneratorClass):
    def __init__(self, user_id, client, pages=1, wait_time=2, cursor=None):
        super().__init__()
        self.tweets = []
        self.cursor = cursor
        self.is_next_page = True
        self.client = client
        self.user_id = user_id
        self.pages = pages
        self.wait_time = wait_time

    def get_next_page(self):
        _tweets = []
        if self.is_next_page:
            response = self.client.http.get_bookmarks(cursor=self.cursor)

            entries = self._get_entries(response)
            for entry in entries:
                try:
                    parsed = Tweet(entry, self.client, response)
                    self.tweets.append(parsed)
                    _tweets.append(parsed)
                except:
                    pass

            self.is_next_page = self._get_cursor(response)

            for tweet in _tweets:
                self.tweets.append(tweet)

            self['tweets'] = self.tweets
            self['is_next_page'] = self.is_next_page
            self['cursor'] = self.cursor

        return _tweets

    def to_xlsx(self, filename=None):
        return Excel(self, filename)

    def __getitem__(self, index):
        if isinstance(index, str):
            return getattr(self, index)

        return self.tweets[index]

    def __iter__(self):
        for __tweet in self.tweets:
            yield __tweet

    def __len__(self):
        return len(self.tweets)

