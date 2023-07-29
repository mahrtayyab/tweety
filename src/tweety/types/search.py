import time
from . import Tweet, Excel, User, deprecated
from .base import BaseGeneratorClass


class Search(BaseGeneratorClass):
    def __init__(self, keyword, http, pages=1, filter_=None, wait_time=2, cursor=None):
        super().__init__()
        self.tweets = []
        self.users = []
        self.keyword = keyword
        self.cursor = cursor
        self.is_next_page = True
        self.http = http
        self.pages = pages
        self.wait_time = wait_time
        self.filter = filter_.lower().strip() if filter_ else None

    def __repr__(self):
        return "Search(keyword={}, count={}, filter={})".format(
            self.keyword,
            len(self.users) if self.filter == "users" else len(self.tweets),
            self.filter
        )

    def get_next_page(self):
        if self.is_next_page:
            response = self.http.perform_search(self.keyword, self.cursor, self.filter)
            thisTweets = self._parse_response(response)

            self['is_next_page'] = self.is_next_page
            self['cursor'] = self.cursor

            return thisTweets

        return []

    @staticmethod
    def _get_entries(response):
        instructions = response['data']['search_by_raw_query']['search_timeline']['timeline']['instructions']
        entries = []
        for instruction in instructions:
            if instruction.get("type") == "TimelineAddEntries":
                entries.extend(instruction['entries'])
            elif instruction.get("type") == "TimelineReplaceEntry":
                entries.append(instruction['entry'])

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

    def _parse_response(self, response):
        thisObjects = []
        entries = self._get_entries(response)
        for entry in entries:
            if self.filter == "users":
                users = self._get_tweet_content_key(entry)
                for user in users:
                    try:
                        user = User(user)
                        self.users.append(user)
                        thisObjects.append(user)
                    except:
                        pass
                self['users'] = self.users
            else:
                tweets = self._get_tweet_content_key(entry)
                for tweet in tweets:
                    try:
                        parsed = Tweet(tweet, self.http, response)
                        self.tweets.append(parsed)
                        thisObjects.append(parsed)
                    except:
                        pass

                self['tweets'] = self.tweets

        self.is_next_page = self._get_cursor(response)
        return thisObjects

    def to_xlsx(self, filename=None):
        if self.filter == "users":
            return AttributeError("to_xlsx with 'users' filter isn't supported yet")
        return Excel(self.tweets, f"search-{self.keyword}", filename)

    def __getitem__(self, index):
        if isinstance(index, str):
            return getattr(self, index)

        if self.filter == "users":
            return self.users[index]
        else:
            return self.tweets[index]

    def __iter__(self):
        if self.filter == "users":
            for _user in self.users:
                yield _user
        else:
            for _tweet in self.tweets:
                yield _tweet
