import time
from . import Tweet, Excel, get_graph_ql_query, deprecated


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
    def _get_graph_query(get_replies, user_id, cursor):
        if get_replies:
            return str(get_graph_ql_query(2, user_id, cursor))
        else:
            return str(get_graph_ql_query(1, user_id, cursor))

    @staticmethod
    def _get_tweets_index(response):
        if response.json()['data']['user']['result']['timeline']['timeline']['instructions'][0]['type'] == "TimelineAddEntries":
            tweets_index = 0
        else:
            tweets_index = 1

        return tweets_index

    @staticmethod
    def _get_tweet_content_key(tweet):
        if str(tweet['entryId']).split("-")[0] == "tweet":
            return [tweet['content']['itemContent']['tweet_results']['result']]

        if str(tweet['entryId']).split("-")[0] == "homeConversation":
            return [item['item']['itemContent']['tweet_results']['result'] for item in tweet["content"]["items"]]

        return []

    def get_next_page(self, user_id, get_replies):
        _tweets = []
        if self.is_next_page:
            graph_request = self._get_graph_query(get_replies, user_id, self.cursor)
            response = self.http.get_tweets(graph_request, replies=get_replies)
            tweets_index = self._get_tweets_index(response)

            for entry in response.json()['data']['user']['result']['timeline']['timeline']['instructions'][tweets_index]['entries']:
                tweets = self._get_tweet_content_key(entry)
                for tweet in tweets:
                    try:
                        _tweets.append(Tweet(None, tweet, self.http))
                    except:
                        pass

            self.is_next_page = self._get_cursor(response, tweets_index)
            for tweet in _tweets:
                self.tweets.append(tweet)

            self['tweets'] = self.tweets
            self['is_next_page'] = self.is_next_page
            self['cursor'] = self.cursor

            return _tweets

    def _get_tweets(self, user_id, pages, get_replies, wait_time=2):
        for page in range(1, int(pages) + 1):
            all_tweets = self.get_next_page(user_id, get_replies)
            if self.is_next_page and page != pages:
                time.sleep(wait_time)

    def _get_cursor(self, response, tweets_index):
        for entry in response.json()['data']['user']['result']['timeline']['timeline']['instructions'][tweets_index]['entries']:
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

    def __repr__(self):
        return f"UserTweets(user_id={self.user_id}, count={len(self.tweets)})"

    @deprecated
    def to_dict(self):
        return self.tweets


