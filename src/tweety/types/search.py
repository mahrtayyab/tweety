from . import Tweet, Excel, User, List
from .base import BaseGeneratorClass
from .twDataTypes import SelfThread
from ..utils import find_objects
from ..filters import SearchFilters



class Search(BaseGeneratorClass):
    OBJECTS_TYPES = {
        "tweet": Tweet,
        "search": Tweet,
        "homeConversation": SelfThread,
        "profile": SelfThread,
        "user": User,
        "list": List
    }
    _RESULT_ATTR = "results"

    def __init__(self, keyword, client, pages=1, filter_=None, wait_time=2, cursor=None):
        super().__init__()
        self.results = []
        self.keyword = keyword
        self.cursor = cursor
        self.cursor_top = cursor
        self.is_next_page = True
        self.client = client
        self.pages = pages
        self.wait_time = wait_time
        self.filter = filter_.strip() if filter_ else None

    def __repr__(self):
        return "Search(keyword={}, count={}, filter={})".format(
            self.keyword, len(self.results), self.filter
        )

    def get_page(self, cursor):
        thisObjects = []
        response = self.client.http.perform_search(self.keyword, cursor, self.filter)
        entries = self._get_entries(response)

        if self.filter == SearchFilters.Lists:
            entries = self._get_list_entries(entries)
        elif self.filter == SearchFilters.Media:
            entries = self._get_grid_entries(entries)

        for entry in entries:
            object_type = self._get_target_object(entry)
            try:
                if object_type is None:
                    continue

                parsed = object_type(self.client, entry, None)
                if parsed:
                    thisObjects.append(parsed)
            except:
                pass

        cursor = self._get_cursor_(response)
        cursor_top = self._get_cursor_(response, "Top")

        return thisObjects, cursor, cursor_top

    def _get_target_object(self, obj):
        entry_type = str(obj['entryId']).split("-")[0]
        return self.OBJECTS_TYPES.get(entry_type)

    @staticmethod
    def _get_grid_entries(entries):
        results = []
        for entry in entries:
            obj = find_objects(entry, "displayType", "VerticalGrid", none_value={}, recursive=False)
            if obj:
                results.extend(obj.get("items", []))
        return results

    @staticmethod
    def _get_list_entries(entries):
        results = []
        for entry in entries:
            if str(entry['entryId']).split("-")[0] == "list":
                for item in entry['content']['items']:
                    results.append(item)
        return results

    def to_xlsx(self, filename=None):
        if self.filter == "users":
            return AttributeError("to_xlsx with 'users' filter isn't supported yet")

        return Excel(self.results, f"search-{self.keyword}", filename)


class TypeHeadSearch(dict):
    DATA_TYPES = {
        "users": User
    }

    def __init__(self, client, keyword, result_type='events,users,topics,lists'):
        super().__init__()
        self.client = client
        self.keyword = keyword
        self.result_type = result_type
        self.results = []
        self._get_results()

    def _get_results(self):
        response = self.client.http.search_typehead(self.keyword, self.result_type)
        for _type_name, _type_object in self.DATA_TYPES.items():
            for result in response.get(_type_name, []):
                try:
                    if _type_name == "users":
                        result['__typename'] = "User"

                    parsed = _type_object(self.client, result)
                    self.results.append(parsed)
                except:
                    pass
        self['results'] = self.results
        return self.results

    def __getitem__(self, index):
        if isinstance(index, str):
            return getattr(self, index)

        return self.results[index]

    def __iter__(self):
        for i in self.results:
            yield i

    def __len__(self):
        return len(self.results)

    def __repr__(self):
        return "TypeHeadSearch(keyword={})".format(self.keyword)

