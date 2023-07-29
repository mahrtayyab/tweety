from .twDataTypes import TweetThread
from ..exceptions_ import UserProtected, UserNotFound
from . import Tweet, Excel, deprecated
from .base import BaseGeneratorClass


class UserTweets(BaseGeneratorClass):
    def __init__(self, user_id, http, pages=1, get_replies: bool = True, wait_time=2, cursor=None):
        super().__init__()
        self.tweets = []
        self.get_replies = get_replies
        self.cursor = cursor
        self.is_next_page = True
        self.http = http
        self.user_id = user_id
        self.pages = pages
        self.wait_time = wait_time

    @staticmethod
    def _get_entries(response):
        instructions = response['data']['user']['result']['timeline_v2']['timeline']['instructions']
        for instruction in instructions:
            if instruction.get("type") == "TimelineAddEntries":
                return instruction['entries']

        return []

    @staticmethod
    def _get_tweet_content_key(tweet):
        if str(tweet['entryId']).split("-")[0] == "tweet":
            return [tweet['content']['itemContent']['tweet_results']['result']]

        if str(tweet['entryId']).split("-")[0] == "homeConversation":
            return [item['item']['itemContent']['tweet_results']['result'] for item in tweet["content"]["items"]]

        if str(tweet['entryId']).split("-")[0] == "profile" and str(tweet['entryId']).split("-")[1] == "conversation":
            return [item['item']['itemContent']['tweet_results']['result'] for item in tweet["content"]["items"]]

        return []

    def get_next_page(self):
        _tweets = []
        if self.is_next_page:
            response = self.http.get_tweets(self.user_id, replies=self.get_replies, cursor=self.cursor)

            if not response['data']['user'].get("result"):
                raise UserNotFound(error_code=50, error_name="GenericUserNotFound", response=response)

            if response['data']['user']['result']['__typename'] == "UserUnavailable":
                raise UserProtected(403, "UserUnavailable", None)

            entries = self._get_entries(response)

            for entry in entries:
                tweets = self._get_tweet_content_key(entry)
                try:
                    if len(tweets) > 1:
                        parsed = TweetThread(tweets, self.http, response)
                    else:
                        parsed = Tweet(tweets[0], self.http, response)
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





