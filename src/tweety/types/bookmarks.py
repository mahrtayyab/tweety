from . import Tweet, Excel
from .base import BaseGeneratorClass


class Bookmarks(BaseGeneratorClass):
    def __init__(self, user_id, http, pages=1, wait_time=2, cursor=None):
        super().__init__()
        self.tweets = []
        self.cursor = cursor
        self.is_next_page = True
        self.http = http
        self.user_id = user_id
        self.pages = pages
        self.wait_time = wait_time

    @staticmethod
    def _get_entries(response):
        instructions = response['data']['bookmark_timeline_v2']['timeline']['instructions']
        entries = []
        for instruction in instructions:
            if instruction.get("type") == "TimelineAddEntries":
                entries.extend(instruction['entries'])

        return entries

    @staticmethod
    def _get_tweet_content_key(response):
        if str(response['entryId']).split("-")[0] == "tweet":
            return [response['content']['itemContent']['tweet_results']['result']]

        if str(response['entryId']).split("-")[0] == "user":
            return [response['content']['itemContent']['user_results']['result']]

        if str(response['entryId']).split("-")[0] == "homeConversation":
            return [item['item']['itemContent']['tweet_results']['result'] for item in response["content"]["items"]]

        return []

    def get_next_page(self):
        _tweets = []
        if self.is_next_page:
            response = self.http.get_bookmarks(cursor=self.cursor)

            entries = self._get_entries(response)
            for entry in entries:
                tweets = self._get_tweet_content_key(entry)
                for tweet in tweets:
                    try:
                        parsed = Tweet(tweet, self.http, response)
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

    def __repr__(self):
        return f"Bookmarks(user_id={self.user_id}, count={self.__len__()})"

