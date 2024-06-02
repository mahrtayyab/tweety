from .base import BaseGeneratorClass
from .twDataTypes import Tweet


class TweetNotifications(BaseGeneratorClass):
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

        response = self.client.http.get_tweet_notifications(cursor=cursor)
        users = response.get('globalObjects', {}).get('users', {})
        tweets = response.get('globalObjects', {}).get('tweets', {})

        for tweet_id, tweet in tweets.items():
            user = users.get(str(tweet['user_id']))
            user['__typename'] = "User"
            tweet['author'], tweet['rest_id'], tweet['__typename'] = user, tweet_id, "Tweet"

            try:
                parsed = Tweet(self.client, tweet, response)
                if parsed:
                    _tweets.append(parsed)
            except:
                pass

        cursor = self._get_cursor_(response)
        cursor_top = self._get_cursor_(response, "Top")

        return _tweets, cursor, cursor_top
