import time
import traceback
from . import Tweet, Excel, deprecated


class Mention(dict):
    def __init__(self, user_id, http, pages=1, wait_time=2, cursor=None):
        super().__init__()
        self.tweets = []
        self.cursor = cursor
        self.is_next_page = True
        self.http = http
        self.user_id = user_id
        self.pages = pages
        self.wait_time = wait_time

    def get_next_page(self):
        _tweets = []
        if self.is_next_page:
            response = self.http.get_mentions(self.user_id, cursor=self.cursor)

            if not response['globalObjects']:
                self.is_next_page = False
                return self, _tweets

            users = response['globalObjects']['users']
            tweets = response['globalObjects']['tweets']
            for tweet_id, tweet in tweets.items():
                user = users.get(str(tweet['user_id']))
                tweet['author'], tweet['rest_id'] = user, tweet_id
                parsed = Tweet(response, tweet, self.http)
                _tweets.append(parsed)

            self.is_next_page = self._get_cursor(response)

            for tweet in _tweets:
                self.tweets.append(tweet)

            self['tweets'] = self.tweets
            self['is_next_page'] = self.is_next_page
            self['cursor'] = self.cursor

        return self, _tweets

    def generator(self):
        for page in range(1, int(self.pages) + 1):
            _, tweets = self.get_next_page()

            yield self, tweets

            if self.is_next_page and page != self.pages:
                time.sleep(self.wait_time)

    def _get_cursor(self, response):
        for instruction in response['timeline']['instructions']:
            if instruction.get('addEntries'):
                entries = instruction['addEntries']['entries']
                for entry in entries:
                    if str(entry['entryId']).split("-")[0] == "cursor":
                        newCursor = entry['content']['operation']['cursor']['value']

                        if newCursor == self.cursor:
                            return False

                        self.cursor = newCursor
                        return True

        return False

    def __getitem__(self, index):
        return self.tweets[index]

    def __iter__(self):
        for __tweet in self.tweets:
            yield __tweet

    def __len__(self):
        return len(self.tweets)

    def __repr__(self):
        return f"Mentions(user_id={self.user_id}, count={self.__len__()})"

