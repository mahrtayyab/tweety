import base64
import os.path
import re
import sys
import time
import warnings
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
            elif isinstance(tweet, TweetThread):
                for _threadedTweet in tweet:
                    self._write_tweet(_threadedTweet)

        if not self.filename:
            self.filename = f"tweets-{self.author}.xlsx"

        try:
            self.workbook.remove("sheet")
        except ValueError:
            pass

        self.workbook.save(self.filename)


class TweetThread(dict):
    def __init__(self, response, http, _full_response=None):
        super().__init__()
        self._raw = response
        self._http = http
        self._full_response = _full_response
        self.tweets = self['tweets'] = self.parse_tweets()

    def parse_tweets(self):
        _tweets = []
        for tweet in self._raw:
            try:
                _tweets.append(Tweet(tweet, self._http, self._full_response))
            except:
                pass

        return _tweets

    def __getitem__(self, index):
        return self.tweets[index]

    def __iter__(self):
        for __tweet in self.tweets:
            yield __tweet

    def __len__(self):
        return len(self.tweets)

    def __repr__(self):
        return "TweetThread(tweets={})".format(
            len(self.tweets)
        )


class Tweet(dict):
    def __init__(self, tweet, http, full_response=None):  # noqa
        super().__init__()
        self.http = http
        self.__tweet = tweet
        self.__full_response = full_response
        self.__replied_to = None
        self._format_tweet()

        for key, value in vars(self).items():
            if not str(key).startswith("_"):
                self[key] = value

    def __repr__(self):
        return f"Tweet(id={self.id}, author={self.author}, created_on={self.created_on})"  # noqa

    def __iter__(self):
        if self.threads:  # noqa
            for thread_ in self.threads:  # noqa
                yield thread_

    def _format_tweet(self):
        original_tweet = self.__tweet['legacy'] if self.__tweet.get('legacy') else self.__tweet
        self.id = self._get_id()
        self.created_on = self.date = self._get_date(original_tweet)
        self.author = self._get_author()
        self.is_retweet = self._is_retweet(original_tweet)
        self.retweeted_tweet = self._get_retweeted_tweet(self.is_retweet, original_tweet)
        self.text = self.tweet_body = self._get_tweet_text(original_tweet, self.is_retweet)
        self.is_quoted = self._is_quoted(original_tweet)
        self.quoted_tweet = self._get_quoted_tweet(self.is_quoted)
        self.is_reply = self._is_reply(original_tweet)
        self.is_sensitive = self._is_sensitive(original_tweet)
        self.reply_counts = self._get_reply_counts(original_tweet)
        self.quote_counts = self._get_quote_counts(original_tweet)
        self.replied_to = self._get_reply_to(self.is_reply)
        self.bookmark_count = self._get_bookmark_count(original_tweet)
        self.vibe = self._get_vibe()
        self.views = self._get_views()
        self.language = self._get_language(original_tweet)
        self.likes = self._get_likes(original_tweet)
        self.place = self._get_place(original_tweet)
        self.retweet_counts = self._get_retweet_counts(original_tweet)
        self.source = self._get_source(self.__tweet)
        self.voice_info = None  # TODO
        self.media = self._get_tweet_media(original_tweet)
        self.user_mentions = self._get_tweet_mentions(original_tweet)
        self.urls = self._get_tweet_urls(original_tweet)
        self.hashtags = self._get_tweet_hashtags(original_tweet)
        self.symbols = self._get_tweet_symbols(original_tweet)
        self.comments = []

    def get_comments(self, pages=1, wait_time=2, cursor=None):
        if not wait_time:
            wait_time = 0

        results = [i for i in self.iter_comments(pages, wait_time, cursor)]
        return self.comments

    def iter_comments(self, pages=1, wait_time=2, cursor=None):
        if not wait_time:
            wait_time = 0

        cursor = cursor
        _comments = []
        pages = pages
        for page in range(1, int(pages) + 1):
            _, comments, new_cursor = self._get_comments(cursor, self.__full_response)

            yield self, comments

            if cursor != new_cursor and page != pages:
                time.sleep(wait_time)
            else:
                break

    def _get_comments(self, cursor=None, response=None):
        _comments = []
        _cursor = cursor

        if not response:
            response = self.http.get_tweet_detail(self.id, cursor)
        else:
            self.__full_response = None

        for instruction in response['data']['threaded_conversation_with_injections_v2']['instructions']:
            if instruction['type'] == "TimelineAddEntries":
                for entry in instruction['entries']:
                    if str(entry['entryId'].split("-")[0]) == "conversationthread":
                        for item in entry['content']['items']:
                            tweet = item['item']['itemContent']['tweet_results']['result']
                            try:
                                parsed = Tweet(tweet, self.http)
                                _comments.append(parsed)
                                self.comments.append(parsed)
                            except:
                                pass
                    elif "cursor-bottom" in str(entry['entryId']):
                        _cursor = entry['content']['itemContent']['value']

        return self, _comments, _cursor

    @staticmethod
    def _get_date(original_tweet):
        date = original_tweet.get("created_at")

        if date:
            return dateutil.parser.parse(date)

        return None

    def _get_id(self):
        if self.__tweet.get("rest_id"):
            return self.__tweet['rest_id']

        if self.__tweet.get("tweet"):
            return self.__tweet['tweet']['rest_id']

    def _get_author(self):
        if self.__tweet.get("core"):
            return User(self.__tweet['core']['user_results']['result'])

        if self.__tweet.get("author"):
            return User(self.__tweet['author'])

        return None

    def _get_retweeted_tweet(self, is_retweet, original_tweet):
        if is_retweet and original_tweet.get("retweeted_status_result"):
            retweet = original_tweet['retweeted_status_result']['result']
            return Tweet(retweet, self.http)

        return None

    def _get_quoted_tweet(self, is_quoted):
        if is_quoted:
            try:
                if self.__tweet.get("quoted_status_result"):
                    raw_tweet = self.__tweet['quoted_status_result']['result']
                    return Tweet(raw_tweet, self.http)

                if self.__tweet.get("legacy"):
                    raw_tweet = self.__tweet['legacy']['retweeted_status_result']['result']['quoted_status_result']['result']
                    return Tweet(raw_tweet, self.http)

                return None
            except:
                return None

        return None

    def _get_vibe(self):
        if self.__tweet.get("vibe"):
            vibeImage = self.__tweet['vibe']['imgDescription']
            vibeText = self.__tweet['vibe']['text']
            return f"{vibeImage} {vibeText}"

        return ""

    def _get_views(self):
        if self.__tweet.get("views"):
            return self.__tweet['views'].get('count', 'Unavailable')

        return 0

    def _get_reply_to(self, is_reply):
        if is_reply:
            tweet_id = self.__tweet['legacy']['in_reply_to_status_id_str']
            if not self.__full_response:
                response = self.http.get_tweet_detail(tweet_id)
            else:
                response = self.__full_response
            for entry in response['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries']:
                if str(entry['entryId']).split("-")[0] == "tweet" and str(entry['content']['itemContent']['tweet_results']['result']['rest_id']) == str(tweet_id):
                    raw_tweet = entry['content']['itemContent']['tweet_results']['result']
                    return Tweet(raw_tweet, self.http)
        return None

    @staticmethod
    def _is_sensitive(original_tweet):
        return original_tweet.get("possibly_sensitive", False)

    @staticmethod
    def _get_reply_counts(original_tweet):
        return original_tweet.get("reply_count", 0)

    @staticmethod
    def _get_quote_counts(original_tweet):
        return original_tweet.get("quote_count", 0)

    @staticmethod
    def _is_retweet(original_tweet):
        if original_tweet.get("retweeted"):
            return True

        if str(original_tweet.get('full_text', "")).startswith("RT"):
            return True

        return False

    @staticmethod
    def _is_reply(original_tweet):
        tweet_keys = list(original_tweet.keys())
        required_keys = ["in_reply_to_status_id_str", "in_reply_to_user_id_str", "in_reply_to_screen_name"]
        return any(x in tweet_keys and original_tweet[x] is True for x in required_keys)

    @staticmethod
    def _is_quoted(original_tweet):
        if original_tweet.get("is_quote_status"):
            return True

        return False

    @staticmethod
    def _get_language(original_tweet):
        return original_tweet.get('lang', "")

    @staticmethod
    def _get_likes(original_tweet):
        return original_tweet.get("favorite_count", 0)

    @staticmethod
    def _get_place(original_tweet):
        if original_tweet.get('place'):
            return Place(original_tweet['place'])

        return None

    @staticmethod
    def _get_retweet_counts(original_tweet):
        return original_tweet.get('retweet_count', 0)

    @staticmethod
    def _get_source(original_tweet):
        if original_tweet.get('source'):
            return str(original_tweet['source']).split(">")[1].split("<")[0]

        return ""

    @staticmethod
    def _get_tweet_text(original_tweet, is_retweet):
        if is_retweet and original_tweet.get("retweeted_status_result"):

            if not original_tweet['retweeted_status_result']['result'].get("legacy"):
                return original_tweet['retweeted_status_result']['result']['tweet']['legacy']['full_text']

            return original_tweet['retweeted_status_result']['result']['legacy']['full_text']

        if original_tweet.get('full_text'):
            return original_tweet['full_text']

        return ""

    def _get_tweet_media(self, original_tweet):
        if not original_tweet.get("extended_entities"):
            return []

        if not original_tweet['extended_entities'].get("media"):
            return []

        return [Media(media, self.http) for media in original_tweet['extended_entities']['media']]

    @staticmethod
    def _get_tweet_mentions(original_tweet):
        if not original_tweet.get("entities"):
            return []

        if not original_tweet['entities'].get("user_mentions"):
            return []

        return [ShortUser(user) for user in original_tweet['entities']['user_mentions']]

    @staticmethod
    def _get_bookmark_count(original_tweet):
        return original_tweet.get("bookmark_count", None)

    @staticmethod
    def _get_tweet_urls(original_tweet):
        if not original_tweet.get("entities"):
            return []

        if not original_tweet['entities'].get("urls"):
            return []

        return [url for url in original_tweet['entities']['urls']]

    @staticmethod
    def _get_tweet_hashtags(original_tweet):
        if not original_tweet.get("entities"):
            return []

        if not original_tweet['entities'].get("hashtags"):
            return []

        return [hashtag for hashtag in original_tweet['entities']['hashtags']]

    @staticmethod
    def _get_tweet_symbols(original_tweet):
        if not original_tweet.get("entities"):
            return []

        if not original_tweet['entities'].get("symbols"):
            return []

        return [symbol for symbol in original_tweet['entities']['symbols']]

    def __eq__(self, other):
        if isinstance(other, Tweet):
            return str(self.id) == str(other.id) and str(self.author.id) == str(other.author.id)

        return str(self.id) == str(other)


class Media(dict):
    def __init__(self, media_dict, http):
        super().__init__()
        self.__dictionary = media_dict
        self.__http = http
        self.display_url = self.__dictionary.get("display_url")
        self.expanded_url = self.__dictionary.get("expanded_url")
        self.id = self.__dictionary.get("id_str")
        self.indices = self.__dictionary.get("indices")
        self.media_url_https = self.direct_url = self._get_direct_url()
        self.type = self.__dictionary.get("type")
        self.url = self.__dictionary.get("url")
        self.features = self.__dictionary.get("features")
        self.media_key = self.__dictionary.get("media_key")
        self.mediaStats = self.__dictionary.get("mediaStats")
        self.sizes = [MediaSize(k, v) for k, v in self.__dictionary.get("sizes").items() if self.__dictionary.get('sizes')]
        self.original_info = self.__dictionary.get("original_info")
        self.file_format = self._get_file_format()
        self.streams = []

        if self.type == "video" or self.type == "animated_gif":
            self.__parse_video_streams()

        for k, v in vars(self).items():
            if not k.startswith("_"):
                self[k] = v

    def _get_direct_url(self):
        url = self.__dictionary.get("media_url_https")
        # if url.startswith("https://ton.twitter.com"):
        #     url = f"{url}:small"

        return url

    def _get_file_format(self):
        filename = os.path.basename(self.media_url_https).split("?")[0]
        return filename.split(".")[-1] if self.type == "photo" else "mp4"

    def __parse_video_streams(self):
        videoDict = self.__dictionary.get("video_info")
        if not videoDict:
            return

        for i in videoDict.get("variants"):
            if not i.get("content_type").split("/")[-1] == "x-mpegURL":
                self.streams.append(Stream(i, videoDict.get("duration_millis", 0), videoDict.get("aspect_ratio"), self.__http))

    def __repr__(self):
        return f"Media(id={self.id}, type={self.type})"

    def download(self, filename: str = None, progress_callback: Callable[[str, int, int], None] = None):
        if self.type == "photo":
            return self.__http.download_media(self.direct_url, filename, progress_callback)
        elif self.type == "video":
            _res = [eval(stream.res) for stream in self.streams if stream.res]
            max_res = max(_res)
            for stream in self.streams:
                if eval(stream.res) == max_res:
                    file_format = stream.content_type.split("/")[-1]
                    if not file_format == "x-mpegURL":
                        return self.__http.download_media(stream.url, filename, progress_callback)
        elif self.type == "animated_gif":
            file_format = self.streams[0].content_type.split("/")[-1]
            if not file_format == "x-mpegURL":
                return self.__http.download_media(self.streams[0].url, filename, progress_callback)
        return None


class Stream(dict):
    def __init__(self, videoDict, length, ratio, http):
        super().__init__()
        self.__dictionary = videoDict
        self.__http = http
        self.bitrate = self.__dictionary.get("bitrate")
        self.content_type = self.__dictionary.get("content_type")
        self.url = self.direct_url = self.__dictionary.get("url")
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
        return self.__http.download_media(self.url, filename, progress_callback)


class MediaSize(dict):
    def __init__(self, name, data):
        super().__init__()
        self._json = data
        self.name = self['name'] = name
        self.width = self['width'] = self._json['w']
        self.height = self['height'] = self._json['h']
        self.resize = self['resize'] = self._json['resize']

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
    def __init__(self, trends_dict):
        self.__dictionary = trends_dict
        self.name = self.__dictionary.get("name")
        self.url = self.__dictionary.get("url")
        self.tweet_count = self.__dictionary.get("tweet_count")

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
        self.user_ref = [User(user) for user in self._dict['legacy']["user_refs"]] if self._dict['legacy'].get("user_refs") else []
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
    def __init__(self, user_data):
        super().__init__()
        self._json = user_data
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

    def _get_verified(self):
        verified = self._get_key("verified", False)
        if verified is False:
            verified = self._get_key("is_blue_verified", False)

        if verified is False:
            verified = self._get_key("ext_is_blue_verified", False)

        return False if verified in (None, False) else True

    def get_id(self):
        raw_id = self._json.get("id")

        if not str(raw_id).isdigit():
            raw_id = decodeBase64(raw_id).split(":")[-1]

        return int(raw_id)

    def get_created_at(self):
        date = None
        if self._json.get("legacy"):
            date = self._json['legacy']['created_at']

        if not date and self._json.get("created_at"):
            date = self._json["created_at"]

        return parser.parse(date) if date else None

    def _get_key(self, key, default=None):
        user = self._json
        keyValue = default
        if user.get("legacy"):
            keyValue = user['legacy'].get(key)

        if not keyValue and user.get(key):
            keyValue = user[key]

        if str(keyValue).isdigit():
            keyValue = int(keyValue)

        return keyValue

