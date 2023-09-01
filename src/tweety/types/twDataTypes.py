import base64
import datetime
import json
import os.path
import re
import sys
import time
import traceback
import warnings
from typing import Callable
from dateutil import parser
import openpyxl
import dateutil
from ..utils import *


def deprecated(func):
    """

    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.

    """

    def new_func(*args, **kwargs):
        warnings.warn("Call to deprecated function {}.".format(func.__name__), category=DeprecationWarning)
        return func(*args, **kwargs)
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func



class Excel:
    def __init__(self, tweets, filename=None, append=False):
        self.tweets = tweets
        self.filename = filename
        self.author = self._get_author()
        self._append = append
        self._get_sheet()
        self.max_row = self._get_max_row()
        self._write_data()

    def _get_sheet(self):
        if self._append and self.filename:
            self.workbook = openpyxl.load_workbook(self.filename)
            self.worksheet = self.workbook.active
        else:
            self._append = False
            self.workbook = openpyxl.Workbook()
            self.worksheet = self.workbook.create_sheet("tweets")

    def _get_author(self):
        for tweet in self.tweets:
            if hasattr(tweet, "author"):
                return tweet.author.username

        return ""

    def _get_max_row(self):
        if self._append:
            for row in reversed(self.worksheet.iter_rows(values_only=True)):
                if any(cell for cell in row):
                    return row[0].row

        self._set_headers()
        return 1

    def _set_headers(self):
        for index, value in enumerate(WORKBOOK_HEADERS, start=1):
            self.worksheet.cell(row=1, column=index).value = value

    def _write_tweet(self, tweet):
        self.worksheet[f'A{self.max_row + 1}'] = tweet.date
        self.worksheet[f'B{self.max_row + 1}'] = tweet.author.name
        self.worksheet[f'C{self.max_row + 1}'] = tweet.id
        self.worksheet[f'D{self.max_row + 1}'] = tweet.text
        self.worksheet[f'E{self.max_row + 1}'] = tweet.is_retweet
        self.worksheet[f'F{self.max_row + 1}'] = tweet.is_reply
        self.worksheet[f'G{self.max_row + 1}'] = tweet.language
        self.worksheet[f'H{self.max_row + 1}'] = tweet.likes
        self.worksheet[f'I{self.max_row + 1}'] = tweet.retweet_counts
        self.worksheet[f'J{self.max_row + 1}'] = tweet.source
        self.worksheet[f'K{self.max_row + 1}'] = ",".join(
            [media.expanded_url for media in tweet.media]) if tweet.media else ""
        self.worksheet[f'L{self.max_row + 1}'] = ",".join(
            [user_mention.screen_name for user_mention in tweet.user_mentions]) if tweet.user_mentions else ""
        self.worksheet[f'M{self.max_row + 1}'] = ",".join(
            [url['expanded_url'] for url in tweet.urls]) if tweet.urls else ""
        self.worksheet[f'N{self.max_row + 1}'] = ",".join(
            [hashtag['text'] for hashtag in tweet.hashtags]) if tweet.hashtags else ""
        self.worksheet[f'O{self.max_row + 1}'] = ",".join([symbol for symbol in tweet.symbols]) if tweet.symbols else ""
        self.max_row += 1

    def _write_data(self):
        for tweet in self.tweets:
            if isinstance(tweet, Tweet):
                self._write_tweet(tweet)
            elif isinstance(tweet, SelfThread):
                for _threadedTweet in tweet:
                    self._write_tweet(_threadedTweet)

        if not self.filename:
            self.filename = f"tweets-{self.author}.xlsx"

        try:
            self.workbook.remove("sheet")
        except ValueError:
            pass

        self.workbook.save(self.filename)


class Tweet(dict):
    def __init__(self, tweet, client, full_http_response=None):  # noqa
        super().__init__()

        self._comments_cursor = None
        self._raw = tweet
        self._client = client
        self._full_http_response = full_http_response
        self._format_tweet()

        for key, value in vars(self).items():
            if not str(key).startswith("_"):
                self[key] = value

    def __repr__(self):
        return f"Tweet(id={self.id}, author={self.author}, created_on={self.created_on})"  # noqa

    def __iter__(self):
        if self.threads:  # noqa
            for thread in self.threads:  # noqa
                yield thread

    def _format_tweet(self):
        self._tweet = find_objects(self._raw, "__typename", ["Tweet", "TweetWithVisibilityResults"], recursive=False)
        self.original_tweet = self._get_original_tweet()
        self.id = self._get_id()
        self.created_on = self.date = self._get_date()
        self.author = self._get_author()
        self.is_retweet = self._is_retweet()
        self.retweeted_tweet = self._get_retweeted_tweet()
        self.text = self.tweet_body = self._get_tweet_text()
        self.is_quoted = self._is_quoted()
        self.quoted_tweet = self._get_quoted_tweet()
        self.is_reply = self._is_reply()
        self.is_sensitive = self._is_sensitive()
        self.reply_counts = self._get_reply_counts()
        self.quote_counts = self._get_quote_counts()
        self.replied_to = None
        self.bookmark_count = self._get_bookmark_count()
        self.vibe = self._get_vibe()
        self.views = self._get_views()
        self.language = self._get_language()
        self.likes = self._get_likes()
        self.place = self._get_place()
        self.retweet_counts = self._get_retweet_counts()
        self.source = self._get_source()
        self.audio_space_id = self._get_audio_space()
        self.voice_info = None  # TODO
        self.media = self._get_tweet_media()
        self.user_mentions = self._get_tweet_mentions()
        self.urls = self._get_tweet_urls()
        self.hashtags = self._get_tweet_hashtags()
        self.symbols = self._get_tweet_symbols()
        self.community_note = self._get_community_note()
        self.url = self._get_url()
        self.threads = self.get_threads()
        self.comments = []

    def _get_url(self):
        return "https://twitter.com/{}/status/{}".format(
            self.author.username, self.id
        )

    def like(self):
        return self._client.like_tweet(self.id)

    def retweet(self):
        return self._client.retweet_tweet(self.id)


    def _get_original_tweet(self):
        tweet = self._tweet

        if tweet.get('tweet'):
            tweet = tweet['tweet']


        return tweet['legacy'] if tweet.get('legacy') else tweet

    def get_threads(self):
        _threads = []
        if not self._full_http_response:
            return _threads

        instruction = find_objects(self._full_http_response, "type", "TimelineAddEntries")
        if not instruction:
            return _threads

        entries = instruction.get('entries', [])
        for entry in entries:

            if str(entry['entryId'].split("-")[0]) == "conversationthread":
                _thread = [i for i in entry['content']['items']]
                self_threads = [i for i in _thread if i['item']['itemContent'].get('tweetDisplayType') == "SelfThread"]

                if len(self_threads) == 0:
                    continue

                for _ in self_threads:
                    try:
                        parsed = Tweet(_, self._client, None)
                        _threads.append(parsed)
                    except:
                        pass

            elif str(entry['entryId'].split("-")[0]) == "tweet" and entry['content']['itemContent']['tweetDisplayType'] == "SelfThread":
                try:
                    parsed = Tweet(entry, self._client, None)
                    _threads.append(parsed)
                except:
                    pass
        return _threads

    def get_comments(self, pages=1, wait_time=2, cursor=None):
        if not wait_time:
            wait_time = 0

        results = [i for i in self.iter_comments(pages, wait_time, cursor)]
        return self.comments

    def iter_comments(self, pages=1, wait_time=2, cursor=None):
        if not wait_time:
            wait_time = 0

        self._comments_cursor = cursor if cursor else self._comments_cursor
        pages = pages
        for page in range(1, int(pages) + 1):
            _, comments, self._comments_cursor = self._get_comments(self._comments_cursor, self._full_http_response)

            yield self, comments

            if cursor != self._comments_cursor and page != pages:
                time.sleep(wait_time)
            else:
                break

    def _get_comments(self, cursor=None, response=None):
        _comments = []
        _cursor = cursor

        if not response:
            response = self._client.http.get_tweet_detail(self.id, _cursor)

        instruction = find_objects(response, "type", "TimelineAddEntries")
        for entry in instruction['entries']:
            if str(entry['entryId'].split("-")[0]) == "conversationthread":
                thread = [i for i in entry['content']['items']]

                if len(thread) == 0:
                    continue

                try:
                    parsed = ConversationThread(self, thread, self._client)
                    _comments.append(parsed)
                    self.comments.append(parsed)
                except:
                    pass


            elif "cursor-bottom" in str(entry['entryId']):
                _cursor = entry['content']['itemContent']['value']

        return self, _comments, _cursor

    def _get_audio_space(self):
        if not self._tweet.get('card'):
            return None

        if "audiospace" not in self._tweet['card']['legacy'].get('name'):
            return None

        for value in self._tweet['card']['legacy'].get('binding_values', []):
            if value['key'] == "id":
                return value['value']['string_value']

        return None


    def _get_community_note(self):
        if self._tweet.get("birdwatch_pivot"):
            return self._tweet['birdwatch_pivot']['subtitle']['text']

        return None

    def _get_date(self):
        date = self.original_tweet.get("created_at")

        if date:
            return dateutil.parser.parse(date)

        return None

    def _get_id(self):
        return self._tweet.get('rest_id')

    def _get_author(self):
        if self._tweet.get("core"):
            return User(self._tweet['core'], self._client)

        if self._tweet.get("author"):
            return User(self._tweet['author'], self._client)

        return None

    def _get_retweeted_tweet(self):
        if self.is_retweet and self.original_tweet.get("retweeted_status_result"):
            retweet = self.original_tweet['retweeted_status_result']['result']
            return Tweet(retweet, self._client)

        return None

    def _get_quoted_tweet(self):
        if not self.is_quoted:
            return None

        try:
            if self._tweet.get("quoted_status_result"):
                raw_tweet = self._tweet['quoted_status_result']['result']
                return Tweet(raw_tweet, self._client)

            if self.original_tweet.get('retweeted_status_result'):
                raw_tweet = self.original_tweet['retweeted_status_result']['result']['quoted_status_result']['result']
                return Tweet(raw_tweet, self._client)

            return None
        except:
            return None


    def _get_vibe(self):
        if self._tweet.get("vibe"):
            vibeImage = self._tweet['vibe']['imgDescription']
            vibeText = self._tweet['vibe']['text']
            return f"{vibeImage} {vibeText}"

        return ""

    def _get_views(self):
        if self._tweet.get("views"):
            return self._tweet['views'].get('count', 'Unavailable')

        return 0

    def get_reply_to(self):
        if not self.is_reply:
            return None

        tweet_id = self.original_tweet['in_reply_to_status_id_str']
        if not self._full_http_response:
            response = self._client.http.get_tweet_detail(tweet_id)
        else:
            response = self._full_http_response

        try:
            if response['data'].get('threaded_conversation_with_injections_v2'):
                entries = response['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries']
            else:
                entries = response['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][0]['entries']

            for entry in entries:
                if str(entry['entryId']).split("-")[0] == "tweet" and str(entry['content']['itemContent']['tweet_results']['result']['rest_id']) == str(tweet_id):
                    raw_tweet = entry['content']['itemContent']['tweet_results']['result']
                    return Tweet(raw_tweet, self._client.http)
        except:
            pass

        return None

    def _is_sensitive(self):
        return self.original_tweet.get("possibly_sensitive", False)

    def _get_reply_counts(self):
        return self.original_tweet.get("reply_count", 0)

    def _get_quote_counts(self):
        return self.original_tweet.get("quote_count", 0)

    def _is_retweet(self):
        if self.original_tweet.get('retweeted'):
            return self.original_tweet['retweeted']

        if str(self.original_tweet.get('full_text', "")).startswith("RT"):
            return True

        return False

    def _is_reply(self):
        tweet_keys = list(self.original_tweet.keys())
        required_keys = ["in_reply_to_status_id_str", "in_reply_to_user_id_str", "in_reply_to_screen_name"]
        return all(x in tweet_keys for x in required_keys)

    def _is_quoted(self):
        if self.original_tweet.get("is_quote_status"):
            return True

        return False

    def _get_language(self):
        return self.original_tweet.get('lang', "")

    def _get_likes(self):
        return self.original_tweet.get("favorite_count", 0)

    def _get_place(self):
        if self.original_tweet.get('place'):
            return Place(self.original_tweet['place'])

        return None

    def _get_retweet_counts(self):
        return self.original_tweet.get('retweet_count', 0)

    def _get_source(self):
        if self._tweet.get('source'):
            return str(self._tweet['source']).split(">")[1].split("<")[0]

        return ""

    def _get_tweet_text(self):
        if self.is_retweet and self.original_tweet.get("retweeted_status_result"):

            if not self.original_tweet['retweeted_status_result']['result'].get("legacy"):
                return self.original_tweet['retweeted_status_result']['result']['tweet']['legacy']['full_text']

            return self.original_tweet['retweeted_status_result']['result']['legacy']['full_text']

        if self.original_tweet.get('full_text'):
            return self.original_tweet['full_text']

        return ""

    def _get_tweet_media(self):
        if not self.original_tweet.get("extended_entities"):
            return []

        if not self.original_tweet['extended_entities'].get("media"):
            return []

        return [Media(media, self._client) for media in self.original_tweet['extended_entities']['media']]

    def _get_tweet_mentions(self):
        if not self.original_tweet.get("entities"):
            return []

        if not self.original_tweet['entities'].get("user_mentions"):
            return []

        return [ShortUser(user) for user in self.original_tweet['entities']['user_mentions']]

    def _get_bookmark_count(self):
        return self.original_tweet.get("bookmark_count", None)

    def _get_tweet_urls(self):
        if not self.original_tweet.get("entities"):
            return []

        if not self.original_tweet['entities'].get("urls"):
            return []

        return [url for url in self.original_tweet['entities']['urls']]

    def _get_tweet_hashtags(self):
        if not self.original_tweet.get("entities"):
            return []

        if not self.original_tweet['entities'].get("hashtags"):
            return []

        return [hashtag for hashtag in self.original_tweet['entities']['hashtags']]

    def _get_tweet_symbols(self):
        if not self.original_tweet.get("entities"):
            return []

        if not self.original_tweet['entities'].get("symbols"):
            return []

        return [symbol for symbol in self.original_tweet['entities']['symbols']]

    def __eq__(self, other):
        if isinstance(other, Tweet):
            return str(self.id) == str(other.id) and str(self.author.id) == str(other.author.id)

        return str(self.id) == str(other)

class SelfThread(dict):
    def __init__(self, conversation_tweet, client, full_response):
        super().__init__()
        self._client = client
        self._raw = conversation_tweet
        self.tweets = []
        self.all_tweets_id = self._get_all_tweet_ids()
        self._format_tweet()

        for key, value in vars(self).items():
            if not str(key).startswith("_"):
                self[key] = value

    def _format_tweet(self):
        for item in self._raw['content']['items']:
            try:
                parsed = Tweet(item, self._client, None)
                self.tweets.append(parsed)
            except:
                pass

    def __iter__(self):
        if self.tweets:
            for tweet in self.tweets:  # noqa
                yield tweet

    def expand(self):
        tweet = self._client.tweet_detail(self.tweets[0].id)
        self.tweets = tweet.threads

    def _get_all_tweet_ids(self):
        return self._raw['content']['metadata']['conversationMetadata']['allTweetIds']

    def __repr__(self):
        return "SelfThread(tweets={}, all_tweets={})".format(
            len(self.tweets), len(self.all_tweets_id)
        )


class ConversationThread(dict):
    def __init__(self, parent_tweet, thread_tweets, client):
        super().__init__()
        self._client = client
        self.tweets = []
        self.parent = parent_tweet
        self.cursor = None
        self._threads = thread_tweets
        self._format_threads()

        for key, value in vars(self).items():
            if not str(key).startswith("_"):
                self[key] = value

    def __repr__(self):
        return "ConversationThread(parent={}, tweets={})".format(
            self.parent, len(self.tweets)
        )

    def _format_threads(self):
        for thread in self._threads:
            entry_type = str(thread['entryId']).split("-")[-2].lower()
            if entry_type == "tweet":
                self.tweets.append(Tweet(thread, self._client, None))
            elif entry_type == "showmore":
                self.cursor = thread['item']['itemContent']['value']

    def expand(self):
        if not self.cursor:
            return self.tweets

        response = self._client.http.get_tweet_detail(self.parent.id, self.cursor)
        moduleItems = find_objects(response, "moduleItems", None)

        if not moduleItems or len(moduleItems) == 0:
            return self.tweets

        for item in moduleItems:
            tweet = find_objects(item, "__typename", ["Tweet", "TweetWithVisibilityResults"], recursive=False)
            if tweet:
                self.tweets.append(Tweet(tweet, self._client, None))

        return self.tweets




class Media(dict):
    def __init__(self, media_dict, client):
        super().__init__()
        self._raw = media_dict
        self._client = client
        self.display_url = self._raw.get("display_url")
        self.expanded_url = self._raw.get("expanded_url")
        self.id = self._raw.get("id_str")
        self.indices = self._raw.get("indices")
        self.media_url_https = self.direct_url = self._get_direct_url()
        self.type = self._raw.get("type")
        self.url = self._raw.get("url")
        self.features = self._raw.get("features")
        self.media_key = self._raw.get("media_key")
        self.mediaStats = self._raw.get("mediaStats")
        self.sizes = [MediaSize(k, v) for k, v in self._raw.get("sizes", {}).items() if self._raw.get('sizes')]
        self.original_info = self._raw.get("original_info")
        self.file_format = self._get_file_format()
        self.streams = []

        if self.type == "video" or self.type == "animated_gif":
            self._parse_video_streams()

        for k, v in vars(self).items():
            if not k.startswith("_"):
                self[k] = v

    def _get_direct_url(self):
        url = self._raw.get("media_url_https")

        return url

    def _get_file_format(self):
        filename = os.path.basename(self.media_url_https).split("?")[0]
        return filename.split(".")[-1] if self.type == "photo" else "mp4"

    def _parse_video_streams(self):
        videoDict = self._raw.get("video_info")

        if not videoDict:
            return

        for i in videoDict.get("variants"):
            if not i.get("content_type").split("/")[-1] == "x-mpegURL":
                self.streams.append(Stream(i, videoDict.get("duration_millis", 0), videoDict.get("aspect_ratio"), self._client))

    def __repr__(self):
        return f"Media(id={self.id}, type={self.type})"

    def download(self, filename: str = None, progress_callback: Callable[[str, int, int], None] = None):
        if self.type == "photo":
            return self._client.http.download_media(self.direct_url, filename, progress_callback)
        elif self.type == "video":
            _res = [eval(stream.res) for stream in self.streams if stream.res]
            max_res = max(_res)
            for stream in self.streams:
                if eval(stream.res) == max_res:
                    file_format = stream.content_type.split("/")[-1]
                    if not file_format == "x-mpegURL":
                        return self._client.http.download_media(stream.url, filename, progress_callback)
        elif self.type == "animated_gif":
            file_format = self.streams[0].content_type.split("/")[-1]
            if not file_format == "x-mpegURL":
                return self._client.http.download_media(self.streams[0].url, filename, progress_callback)
        return None


class Stream(dict):
    def __init__(self, videoDict, length, ratio, client):
        super().__init__()
        self._raw = videoDict
        self._client = client
        self.bitrate = self._raw.get("bitrate")
        self.content_type = self._raw.get("content_type")
        self.url = self.direct_url = self._raw.get("url")
        self.length = length
        self.aspect_ratio = ratio
        self.res = self._get_resolution()

        for k, v in vars(self).items():
            if not k.startswith("_"):
                self[k] = v

    def _get_resolution(self):
        result = re.findall("/(\d+)x(\d+)/", self.url)
        if result:
            result = result[0]
            return f"{result[0]}*{result[1]}"

        return None

    def __repr__(self):
        return f"Stream(content_type={self.content_type}, length={self.length}, bitrate={self.bitrate}, res={self.res})"

    def download(self, filename: str = None, progress_callback: Callable[[str, int, int], None] = None):
        return self._client.http.download_media(self.url, filename, progress_callback)


class MediaSize(dict):
    def __init__(self, name, data):
        super().__init__()
        self._json = data
        self.name = self['name'] = name
        self.width = self['width'] = self._json.get('w')
        self.height = self['height'] = self._json.get('h')
        self.resize = self['resize'] = self._json.get('resize')

    def __repr__(self):
        return "MediaSize(name={}, width={}, height={}, resize={})".format(
            self.name, self.width, self.height, self.resize
        )


class ShortUser(dict):
    def __init__(self, user_dict):
        super().__init__()
        self.__dictionary = user_dict
        self.id = self.__dictionary.get("id_str")
        self.name = self.__dictionary.get("name")
        self.screen_name = self.username = self.__dictionary.get("screen_name")

        for k, v in vars(self).items():
            if not k.startswith("_"):
                self[k] = v

    def __repr__(self):
        return f"ShortUser(id={self.id}, name={self.name})"


class Trends:
    def __init__(self, trend_item):
        self._raw = trend_item
        self._trend = find_objects(self._raw, "trend", None)
        self.name = self._get_name()
        self.url = self._get_url()
        self.tweet_count = self._get_count()

    def _get_name(self):
        return self._trend.get('name')

    def _get_url(self):
        url = self._trend['url'].get('url')
        url = url.replace("twitter://", "https://twitter.com/").replace("query","q")
        return url

    def _get_count(self):
        return  self._trend.get('trendMetadata', {}).get('metaDescription')


    def __repr__(self):
        return f"Trends(name={self.name})"


class Card(dict):
    def __init__(self, card_dict):
        super().__init__()
        self._dict = card_dict
        self._bindings = self._dict['legacy'].get("binding_values")
        self.rest_id = self._dict.get("rest_id")
        self.name = self._dict['legacy'].get("name")
        self.choices = []
        self.end_time = None
        self.last_updated_time = None
        self.duration = None
        self.user_ref = [User(user, None) for user in self._dict['legacy']["user_refs"]] if self._dict['legacy'].get("user_refs") else []
        self.__parse_choices()

        for k, v in vars(self).items():
            if not k.startswith("_"):
                self[k] = v

    def __parse_choices(self):
        for _ in self._bindings:
            _key = _.get("key").split("_")
            if "choice" in _key[0] and "label" in _key[1]:
                _cardName = _key[0]
                _cardValue = _['value']['string_value']
                _cardValueType = _['value']['type']
                _cardCounts = 0
                _cardCountsType = None
                for __ in self._bindings:
                    __key = __.get("key")
                    if __key[0] == _key[0] and "count" in __key[1]:
                        _cardCounts = __['value']['string_value']
                        _cardCountsType = __['value']['type']
                _r = {
                    "card_name": _cardName,
                    "card_value": _cardValue,
                    "card_value_type": _cardValueType,
                    "card_counts": _cardCounts,
                    "card_counts_type": _cardCountsType,
                }
                self.choices.append(Choice(_r))
            elif _key[0] == "end" and _key[1] == "datetime":
                self.end_time = parser.parse(_['value']['string_value'])
                # last_updated_datetime_utc
            elif _key[0] == "last" and _key[1] == "updated":
                self.last_updated_time = parser.parse(_['value']['string_value'])
                # duration_minutes
            elif _key[0] == "duration" and _key[1] == "minutes":
                self.duration = _['value']['string_value']

    def __repr__(self):
        return f"Card(id={self.rest_id}, choices={len(self.choices) if self.choices else []}, end_time={self.end_time}, duration={len(self.duration) if self.duration else 0} minutes)"


class Choice(dict):
    def __init__(self, _dict):
        super().__init__()
        self._dict = _dict
        self.name = self._dict.get("card_name")
        self.value = self._dict.get("card_value")
        self.type = self._dict.get("card_value_type")
        self.counts = self._dict.get("card_counts")
        self.counts_type = self._dict.get("card_counts_type")

        for k, v in vars(self).items():
            if not k.startswith("_"):
                self[k] = v

    def __repr__(self):
        return f"Choice(name={self.name}, value={self.value}, counts={self.counts})"


class Place(dict):
    def __init__(self, place_dict):
        super().__init__()
        self.__dict = place_dict
        self.id = self.__dict.get("id")
        self.country = self.__dict.get("country")
        self.country_code = self.__dict.get("country_code")
        self.full_name = self.__dict.get("full_name")
        self.name = self.__dict.get("name")
        self.url = self.__dict.get("url")
        self.coordinates = self.parse_coordinates()

        for k, v in vars(self).items():
            if not k.startswith("_"):
                self[k] = v

    def parse_coordinates(self):
        results = []
        if not self.__dict.get("bounding_box"):
            return results

        for i in self.__dict['bounding_box'].get("coordinates"):
            for p in i:
                coordinates = [p[1], p[0]]
                if coordinates not in results:
                    results.append([coordinates[0], coordinates[1]])

        return [Coordinates(i[0], i[1]) for i in results]

    def __repr__(self):
        return f"Place(id={self.id}, name={self.name}, country={self.country, self.country_code}, coordinates={self.coordinates})"


class Coordinates(dict):
    def __init__(self, latitude, longitude):
        super().__init__()
        self.latitude = latitude
        self.longitude = longitude

        for k, v in vars(self).items():
            if not k.startswith("_"):
                self[k] = v

    def __repr__(self):
        return f"Coordinates(latitude={self.latitude}, longitude={self.longitude})"


class User(dict):
    def __init__(self, user_data, client, *args):
        super().__init__()
        self._raw = user_data
        self._client = client
        self._user = find_objects(self._raw, "__typename", "User", recursive=False)
        self.original_user = self._user['legacy'] if self._user.get('legacy') else self._user
        self.id = self.rest_id = self.get_id()
        self.created_at = self.date = self.get_created_at()
        self.entities = self._get_key("entities")
        self.description = self.bio = self._get_key("description")
        self.fast_followers_count = self._get_key("fast_followers_count")
        self.favourites_count = self._get_key("favourites_count")
        self.followers_count = self._get_key("followers_count")
        self.friends_count = self._get_key("friends_count")
        self.has_custom_timelines = self._get_key("has_custom_timelines")
        self.is_translator = self._get_key("is_translator")
        self.listed_count = self._get_key("listed_count")
        self.location = self._get_key("location")
        self.media_count = self._get_key("media_count")
        self.name = self._get_key("name")
        self.normal_followers_count = self._get_key("normal_followers_count")
        self.profile_banner_url = self._get_key("profile_banner_url")
        self.profile_image_url_https = self._get_key("profile_image_url_https")
        self.profile_interstitial_type = self._get_key("profile_interstitial_type")
        self.protected = self._get_key("protected")
        self.screen_name = self.username = self._get_key("screen_name")
        self.statuses_count = self._get_key("statuses_count")
        self.translator_type = self._get_key("translator_type")
        self.verified = self._get_verified()
        self.can_dm = self._get_key("can_dm")
        self.following = self._get_key("following", False)
        # self.verified_type = self._get_key("verified_type")
        self.possibly_sensitive = self._get_key("possibly_sensitive")
        self.pinned_tweets = self._get_key("pinned_tweet_ids_str")
        self.profile_url = "https://twitter.com/{}".format(self.screen_name)

        for k, v in vars(self).items():
            if not k.startswith("_"):
                self[k] = v

    def __repr__(self):
        return "User(id={}, username={}, name={}, verified={})".format(
            self.id, self.username, self.name, self.verified
        )

    def follow(self):
        return self._client.follow_user(self.id)

    def unfollow(self):
        return self._client.unfollow_user(self.id)

    def _get_verified(self):
        verified = self._get_key("verified", False)
        if verified is False:
            verified = self._get_key("is_blue_verified", False)

        if verified is False:
            verified = self._get_key("ext_is_blue_verified", False)

        return False if verified in (None, False) else True

    def get_id(self):
        raw_id = self._user.get("id")

        if not str(raw_id).isdigit():
            raw_id = decodeBase64(raw_id).split(":")[-1]

        return int(raw_id)

    def get_created_at(self):
        date = None

        if self.original_user.get('created_at'):
            date = self.original_user['created_at']

        return parser.parse(date) if date else None

    def _get_key(self, key, default=None):
        keyValue = default

        if self._user.get(key):
            keyValue = self._user[key]

        if self.original_user.get(key):
            keyValue = self.original_user[key]

        if str(keyValue).isdigit():
            keyValue = int(keyValue)

        return keyValue

class PeriScopeUser(dict):
    def __init__(self, user_data):
        super().__init__()
        self._raw = user_data
        self.id = self._raw.get('periscope_user_id')
        self.twitter_screen_name = self.username =  self._raw.get('twitter_screen_name')
        self.display_name = self.name = self._raw.get('display_name')
        self.is_verified = self._raw.get('is_verified')
        self.twitter_id = self._raw['user_results'].get('rest_id')

class AudioSpace(dict):
    def __init__(self, audio_space, client):
        super().__init__()
        self._raw = audio_space
        self._client = client
        self._space = find_objects(self._raw, "audioSpace", None, recursive=False)
        self._meta_data = find_objects(self._space, "metadata", None, recursive=False)
        self._participants = find_objects(self._raw, "participants", None, recursive=False)
        self.id = self._meta_data.get('rest_id')
        self.state = self._meta_data.get('state')
        self.title = self._meta_data.get('title')
        self.media_key = self._meta_data.get('media_key')
        self.created_at = self.ts_to_datetime(self._meta_data.get('created_at'))
        self.started_at = self.ts_to_datetime(self._meta_data.get('started_at'))
        self.ended_at = self.ts_to_datetime(self._meta_data.get('ended_at'))
        self.updated_at = self.ts_to_datetime(self._meta_data.get('updated_at'))
        self.creator = User(self._meta_data.get('creator_results'), self._client)
        self.total_live_listeners = self._meta_data.get('total_live_listeners')
        self.total_replay_watched = self._meta_data.get('total_replay_watched')
        self.disallow_join = self._meta_data.get('disallow_join')
        self.is_employee_only = self._meta_data.get('is_employee_only')
        self.is_locked = self._meta_data.get('is_locked')
        self.is_muted = self._meta_data.get('is_muted')
        self.tweet = Tweet(self._meta_data.get('tweet_results'), self._client)
        self.admins = self._get_participants('admins')
        self.speakers = self._get_participants('speakers')

    def _get_participants(self, participant):
        return [PeriScopeUser(user) for user in self._participants[participant]]

    def get_stream_link(self):
        return self._client.http.get_audio_stream(self.media_key)


    @staticmethod
    def ts_to_datetime(ts):
        try:
            return datetime.datetime.fromtimestamp(int(ts))
        except ValueError:
            return datetime.datetime.fromtimestamp(int(ts) / 1000)

    def __repr__(self):
        return "AudioSpace(id={}, title={}, state={}, tweet={})".format(
            self.id, self.title, self.state, self.tweet
        )
