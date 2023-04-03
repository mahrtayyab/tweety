import time
import traceback
from . import Tweet, Excel, deprecated


class UserTweets(dict):
    def __init__(self, user_id, http, pages=1, get_replies: bool = True, wait_time=2, cursor=None):
        super().__init__()
        self.tweets = []
        self.get_replies = get_replies
        self.cursor = cursor
        self.is_next_page = True
        self.http = http
        self.user_id = user_id
        self._get_tweets(user_id, pages, get_replies, wait_time)

    @staticmethod
    def _get_entries(response):
        instructions = response.json()['data']['user']['result']['timeline_v2']['timeline']['instructions']
        for instruction in instructions:
            if instruction.get("type") == "TimelineAddEntries":
                return instruction['entries']

        return []

    @staticmethod
    def _get_tweet_content_key(tweet):
        if str(tweet['entryId']).split("-")[0] == "tweet":
            return [tweet['content']['itemContent']['tweet_results']['result']]

        if str(tweet['entryId']).split("-")[0] == "homeConversation":
            return [item['item']['itemContent']['tweet_results']['result']['tweet'] for item in tweet["content"]["items"]]

        return []

    def get_next_page(self, user_id, get_replies):
        _tweets = []
        if self.is_next_page:
            response = self.http.get_tweets(user_id, replies=get_replies, cursor=self.cursor)
            entries = self._get_entries(response)

            for entry in entries:
                tweets = self._get_tweet_content_key(entry)
                for tweet in tweets:
                    try:
                        _tweets.append(Tweet(response, tweet, self.http))
                    except:
                        traceback.print_exc()
                        pass

            self.is_next_page = self._get_cursor(entries)
            for tweet in _tweets:
                self.tweets.append(tweet)

            self['tweets'] = self.tweets
            self['is_next_page'] = self.is_next_page
            self['cursor'] = self.cursor

            return self

    def _get_tweets(self, user_id, pages, get_replies, wait_time=2):
        for page in range(1, int(pages) + 1):
            self.get_next_page(user_id, get_replies)

            if self.is_next_page and page != pages:
                time.sleep(wait_time)

    def _get_cursor(self, entries):
        for entry in entries:
            if str(entry['entryId']).split("-")[0] == "cursor":
                if entry['content']['cursorType'] == "Bottom":
                    newCursor = entry['content']['value']

                    if newCursor == self.cursor:
                        return False

                    self.cursor = newCursor
                    return True

        return False

    def to_xlsx(self, filename=None):
        return Excel(self.tweets, self.tweets[0].author, filename)

    def __getitem__(self, index):
        return self.tweets[index]

    def __iter__(self):
        for __tweet in self.tweets:
            yield __tweet

    def __len__(self):
        return len(self.tweets)

    def __repr__(self):
        return f"UserTweets(user_id={self.user_id}, count={self.__len__()})"

    @deprecated
    def to_dict(self):
        return self.tweets


