import time
from . import Tweet, Excel, User, deprecated
from .base import BaseGeneratorClass
from .twDataTypes import SelfThread


class Search(BaseGeneratorClass):
    OBJECTS_TYPES = {
        "tweet": Tweet,
        "homeConversation": SelfThread,
        "profile": SelfThread,
        "user":User
    }

    def __init__(self, keyword, client, pages=1, filter_=None, wait_time=2, cursor=None):
        super().__init__()
        self.results = []
        self.keyword = keyword
        self.cursor = cursor
        self.is_next_page = True
        self.client = client
        self.pages = pages
        self.wait_time = wait_time
        self.filter = filter_.strip() if filter_ else None

    def __repr__(self):
        return "Search(keyword={}, count={}, filter={})".format(
            self.keyword,len(self.results),self.filter
        )

    def get_next_page(self):
        if self.is_next_page:
            response = self.client.http.perform_search(self.keyword, self.cursor, self.filter)
            thisTweets = self._parse_response(response)

            self['is_next_page'] = self.is_next_page
            self['cursor'] = self.cursor

            return thisTweets

        return []

    def _get_target_object(self, tweet):
        entry_type = str(tweet['entryId']).split("-")[0]
        return self.OBJECTS_TYPES.get(entry_type)

    def _parse_response(self, response):
        thisObjects = []
        entries = self._get_entries(response)
        for entry in entries:
            object_type = self._get_target_object(entry)

            try:
                if object_type is None:
                    continue

                parsed = object_type(entry, self.client, None)
                thisObjects.append(parsed)
                self.results.append(parsed)
            except:
                pass

                self['results'] = self.results

        self.is_next_page = self._get_cursor(response)
        return thisObjects

    def to_xlsx(self, filename=None):
        if self.filter == "users":
            return AttributeError("to_xlsx with 'users' filter isn't supported yet")

        return Excel(self.results, f"search-{self.keyword}", filename)

    def __getitem__(self, index):
        if isinstance(index, str):
            return getattr(self, index)

        return self.results[index]

    def __iter__(self):
        for _result in self.results:
            yield _result
