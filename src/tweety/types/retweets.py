from .base import BaseGeneratorClass
from .twDataTypes import User


class TweetRetweets(BaseGeneratorClass):
    _RESULT_ATTR = "users"

    def __init__(self, tweet_id, client, pages=1, wait_time=2, cursor=None):
        super().__init__()
        self.users = []
        self.cursor = cursor
        self.cursor_top = cursor
        self.is_next_page = True
        self.client = client
        self.tweet_id = tweet_id
        self.pages = pages
        self.wait_time = wait_time

    def __repr__(self):
        return "TweetRetweets(tweet_id={}, count={})".format(
            self.tweet_id,
            len(self.users)
        )

    def get_page(self, cursor):
        _users = []
        response = self.client.http.get_tweet_retweets(tweet_id=self.tweet_id, cursor=cursor)

        entries = self._get_entries(response)

        for entry in entries:
            try:
                parsed = User(self.client, entry)
                if parsed:
                    _users.append(parsed)
            except:
                pass

        cursor = self._get_cursor_(response)
        cursor_top = self._get_cursor_(response, "Top")

        return _users, cursor, cursor_top
