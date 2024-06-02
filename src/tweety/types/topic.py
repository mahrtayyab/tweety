from .base import BaseGeneratorClass
from .twDataTypes import Topic, Tweet


class TopicTweets(BaseGeneratorClass):
    _RESULT_ATTR = "tweets"

    def __init__(self, topic_id, client, pages=1, cursor=None, wait_time=2):
        super().__init__()
        self.topic_id = topic_id
        self.client = client
        self.pages = pages
        self.cursor = cursor
        self.wait_time = wait_time
        self.is_next_page = True
        self.topic = None
        self.tweets = []

    def get_page(self, cursor):
        _tweets = []
        response = self.client.http.get_topic_landing_page(self.topic_id, cursor)

        if not self.topic:
            self.topic = Topic(self.client, response)

        entries = self._get_entries(response)

        for entry in entries:
            try:
                parsed = Tweet(self.client, entry, None)
                if parsed:
                    _tweets.append(parsed)
            except:
                pass

        cursor = self._get_cursor_(response)
        cursor_top = self._get_cursor_(response, "Top")
        return _tweets, cursor, cursor_top

    def __repr__(self):
        return "TopicTweets(topic={}, tweets={})".format(self.topic, len(self.tweets))



