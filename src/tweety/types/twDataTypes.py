import base64
import os.path
import re
import sys
import warnings
from dateutil import parser
import openpyxl
import dateutil

WORKBOOK_HEADERS = ['Created on', 'author', 'is_retweet', 'is_reply', 'tweet_id', 'tweet_body', 'language', 'likes',
                    'retweet_count', 'source', 'medias', 'user_mentioned', 'urls', 'hashtags', 'symbols']


def decodeBase64(encoded_string):
    return str(base64.b64decode(bytes(encoded_string, "utf-8")))[2:-1]


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


def bar_progress(current, total, width=80):
    progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
    sys.stdout.write("\r" + progress_message)
    sys.stdout.flush()


class Excel:
    def __init__(self, tweets, user, filename=None):
        self.tweets = tweets
        self.user = user
        self.filename = filename
        self.workbook = openpyxl.Workbook()
        self.worksheet = self.workbook.create_sheet("tweets")
        self._set_headers()
        self.max_row = 1
        self._write_data()

    def _set_headers(self):
        for index, value in enumerate(WORKBOOK_HEADERS, start=1):
            self.worksheet.cell(row=1, column=index).value = value

    def _write_data(self):
        for tweet in self.tweets:
            self.worksheet[f'A{self.max_row  + 1}'] = tweet.created_on
            self.worksheet[f'B{self.max_row  + 1}'] = tweet.author.name
            self.worksheet[f'C{self.max_row  + 1}'] = tweet.is_retweet
            self.worksheet[f'D{self.max_row  + 1}'] = tweet.is_reply
            self.worksheet[f'E{self.max_row  + 1}'] = tweet.id
            self.worksheet[f'F{self.max_row  + 1}'] = tweet.text
            self.worksheet[f'G{self.max_row  + 1}'] = tweet.language
            self.worksheet[f'H{self.max_row  + 1}'] = tweet.likes
            self.worksheet[f'I{self.max_row  + 1}'] = tweet.retweet_counts
            self.worksheet[f'J{self.max_row  + 1}'] = tweet.source
            self.worksheet[f'K{self.max_row  + 1}'] = ",".join([media.expanded_url for media in tweet.media]) if tweet.media else ""
            self.worksheet[f'L{self.max_row  + 1}'] = ",".join([user_mention.screen_name for user_mention in tweet.user_mentions]) if tweet.user_mentions else ""
            self.worksheet[f'M{self.max_row  + 1}'] = ",".join([url['expanded_url'] for url in tweet.urls]) if tweet.urls else ""
            self.worksheet[f'N{self.max_row  + 1}'] = ",".join([hashtag['text'] for hashtag in tweet.hashtags]) if tweet.hashtags else ""
            self.worksheet[f'O{self.max_row  + 1}'] = ",".join([symbol for symbol in tweet.symbols]) if tweet.symbols else ""
            self.max_row += 1

        if not self.filename:
            self.filename = f"tweets-{self.user.screen_name}.xlsx"

        try:
            self.workbook.remove("sheet")
        except ValueError:
            pass

        self.workbook.save(self.filename)


class Tweet(dict):
    def __init__(self, raw_response, raw_tweet, http, get_threads=False, is_legacy_user=False, get_reply=False):  # noqa
        super().__init__()
        self.http = http
        self.__raw_response = raw_response
        self.__raw_tweet = raw_tweet
        self.__is_legacy_user = is_legacy_user
        self.__replied_to = None
        self._get_reply = get_reply
        self._format_tweet()

        if get_threads:
            self._get_threads()

        for key, value in vars(self).items():
            if not str(key).startswith("_"):
                self[key] = value

    def __repr__(self):
        return f"Tweet(id={self.id}, author={self.author}, created_on={self.created_on}, threads={len(self.threads) if self.threads else None})"  # noqa

    def __iter__(self):
        if self.threads:  # noqa
            for thread_ in self.threads:  # noqa
                yield thread_

    def _format_tweet(self):
        original_tweet = self._get_original_tweet()
        self.id = self._get_id()
        self.created_on = dateutil.parser.parse(original_tweet["created_at"])
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
        self.replied_to = self.__replied_to = self._get_reply_to(self.is_reply, original_tweet)
        self.bookmark_count = self._get_bookmark_count(original_tweet)
        self.vibe = self._get_vibe()
        self.views = self._get_views()
        self.language = self._get_language(original_tweet)
        self.likes = self._get_likes(original_tweet)
        self.card = self._get_card()
        self.place = self._get_place(original_tweet)
        self.retweet_counts = self._get_retweet_counts(original_tweet)
        self.source = self._get_source(self.__raw_tweet)
        self.media = self._get_tweet_media(original_tweet)
        self.user_mentions = self._get_tweet_mentions(original_tweet)
        self.urls = self._get_tweet_urls(original_tweet)
        self.hashtags = self._get_tweet_hashtags(original_tweet)
        self.symbols = self._get_tweet_symbols(original_tweet)
        self.threads = []
        self.comments = []

    def _get_id(self):
        if self.__raw_tweet.get("rest_id"):
            return self.__raw_tweet['rest_id']

        if self.__raw_tweet.get("tweet"):
            return self.__raw_tweet['tweet']['rest_id']

    def _get_original_tweet(self):
        if self.__raw_tweet.get("tweet"):
            self.__raw_tweet = self.__raw_tweet['tweet']

        if self.__raw_tweet.get("legacy"):
            return self.__raw_tweet['legacy']

        return self.__raw_tweet

    def _get_author(self):
        if self.__raw_tweet.get("core"):
            return User(self.__raw_tweet['core']['user_results']['result'])

        if self.__raw_tweet.get("author"):
            return User(self.__raw_tweet['author'])
        return None

    def _get_retweeted_tweet(self, is_retweet, original_tweet):
        if is_retweet and original_tweet.get("retweeted_status_result"):
            retweet = original_tweet['retweeted_status_result']['result']
            return Tweet(None, retweet, self.http)

        return None

    def _get_threads(self):
        if not self.__raw_response:
            self.__raw_response = self.http.get_tweet_detail(self.id)  # noqa

        for entry in self.__raw_response['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries']:
            if str(entry['entryId']).split("-")[0] == "conversationthread":
                for item in entry['content']['items']:
                    try:
                        tweetType = item["item"]["itemContent"]["tweetDisplayType"]
                        tweet = item['item']['itemContent']['tweet_results']['result']

                        if not self.__replied_to or self.__replied_to.id != tweet['rest_id']:
                            if tweetType == "SelfThread":
                                self.threads.append(Tweet(None, tweet, self.http))
                            else:
                                self.comments.append(Tweet(None, tweet, self.http))
                    except KeyError as e:
                        pass

    def _get_quoted_tweet(self, is_quoted):
        raw_tweet = None
        if is_quoted:
            raw_response = self.__raw_response
            try:
                if self.__raw_tweet.get("quoted_status_result"):
                    raw_tweet = self.__raw_tweet['quoted_status_result']['result']
                    return Tweet(raw_response, raw_tweet, self.http)

                if not raw_tweet and self.__raw_tweet.get("legacy"):
                    raw_tweet = self.__raw_tweet['legacy']['retweeted_status_result']['result']['quoted_status_result']['result']
                    return Tweet(raw_response, raw_tweet, self.http)
            except:
                return None

        return None

    def _get_card(self):
        if self.__raw_tweet.get("card"):
            try:
                return Card(self.__raw_tweet['card'])
            except KeyError:
                pass
        return None

    def _get_vibe(self):
        if self.__raw_tweet.get("vibe"):
            vibeImage = self.__raw_tweet['vibe']['imgDescription']
            vibeText = self.__raw_tweet['vibe']['text']
            return f"{vibeImage} {vibeText}"

        return ""

    def _get_views(self):
        if self.__raw_tweet.get("views"):
            return self.__raw_tweet['views'].get('count', 'Unavailable')

        return 0

    def _get_reply_to(self, is_reply, tweet):
        if is_reply and self._get_reply:
            tweet_id = tweet['in_reply_to_status_id_str']
            response = self.http.get_tweet_detail(tweet_id)
            for entry in response.json()['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries']:
                if str(entry['entryId']).split("-")[0] == "tweet":
                    raw_tweet = entry['content']['itemContent']['tweet_results']['result']
                    return Tweet(response, raw_tweet, self.http)

        elif is_reply and not self._get_reply:
            return tweet['in_reply_to_screen_name']
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


class Media(dict):
    def __init__(self, media_dict, http):
        super().__init__()
        self.__dictionary = media_dict
        self.__http = http
        self.display_url = self.__dictionary.get("display_url")
        self.expanded_url = self.__dictionary.get("expanded_url")
        self.id = self.__dictionary.get("id_str")
        self.indices = self.__dictionary.get("indices")
        self.media_url_https = self.direct_url = self.__dictionary.get("media_url_https")
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

    def download(self, filename=None, show_progress=True):
        if self.type == "photo":
            return self.__http.download_media(self.direct_url, filename, show_progress)
        elif self.type == "video":
            _res = [eval(stream.res) for stream in self.streams if stream.res]
            max_res = max(_res)
            for stream in self.streams:
                if eval(stream.res) == max_res:
                    file_format = stream.content_type.split("/")[-1]
                    if not file_format == "x-mpegURL":
                        return self.__http.download_media(stream.url, filename, show_progress)
        elif self.type == "animated_gif":
            file_format = self.streams[0].content_type.split("/")[-1]
            if not file_format == "x-mpegURL":
                return self.__http.download_media(self.streams[0].url, filename, show_progress)
        return None

    @deprecated
    def to_dict(self):
        return self.__dictionary


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

    def download(self, filename_=None, show_progress=False):
        return self.__http.download_media(self.url, filename_, show_progress)


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

    def to_dict(self):
        return self.__dictionary


class Trends:
    def __init__(self, trends_dict):
        self.__dictionary = trends_dict
        self.name = self.__dictionary.get("name")
        self.url = self.__dictionary.get("url")
        self.tweet_count = self.__dictionary.get("tweet_count")

    def __repr__(self):
        return f"Trends(name={self.name})"

    def to_dict(self):
        return self.__dictionary


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
        self.created_at = self.get_created_at()
        self.description = self._get_key("description")
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
        # self.verified_type = self._get_key("verified_type")
        self.possibly_sensitive = self._get_key("possibly_sensitive")
        self.pinned_tweets = self._get_key("pinned_tweet_ids_str")
        self.profile_url = "https://twitter.com/{}".format(self.screen_name)

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
        