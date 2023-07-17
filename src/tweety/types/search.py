import time
import traceback

from . import Tweet, Excel, User, deprecated


class Search(dict):
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
        for instruction in instructions:
            if instruction.get("type") == "TimelineAddEntries":
                return instruction['entries']

        return []

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

        self.is_next_page = self._get_cursor(entries)
        return thisObjects

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

    def generator(self):
        for page in range(1, int(self.pages) + 1):
            this_tweets = self.get_next_page()

            yield self, this_tweets

            if self.is_next_page and page != self.pages:
                time.sleep(self.wait_time)

        return self

    def to_xlsx(self, filename=None):
        if self.filter == "users":
            return AttributeError("to_xlsx with 'users' filter isn't supported yet")
        return Excel(self.tweets, f"search-{self.keyword}", filename)

    def __getitem__(self, index):
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
