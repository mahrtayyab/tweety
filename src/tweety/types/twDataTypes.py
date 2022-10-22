import sys
from dateutil import parser
import openpyxl
import dateutil

try:
    import wget
except ModuleNotFoundError:
    import warnings
    warnings.warn(' "wget" not found in system ,you will not be able to download the medias')
WORKBOOK_HEADERS = ['Created on', 'author', 'is_retweet', 'is_reply', 'tweet_id', 'tweet_body', 'language', 'likes',
                    'retweet_count', 'source', 'medias', 'user_mentioned', 'urls', 'hashtags', 'symbols']


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


def get_graph_ql_query(typed, user, pages=None) -> str:
    """

    :param typed: internal script query type
    :param user: username or user_id
    :param pages: cursor of next page
    :return: string on graphql query object
    """
    if typed == 1:
        """
        {
            "userId":"",
            "count":20,
            "cursor":""
            "withTweetQuoteCount":true,
            "includePromotedContent":true,
            "withSuperFollowsUserFields":false,
            "withUserResults":true,
            "withBirdwatchPivots":false,
            "withReactionsMetadata":false,
            "withReactionsPerspective":false,
            "withSuperFollowsTweetFields":false,
            "withVoice":true
        }
        """
        if pages:
            data = '''%7B%22userId%22%3A%22''' + user + '''%22%2C%22count%22%3A20%2C%22cursor%22%3A%22''' + pages + '''%22%2C%22withTweetQuoteCount%22%3Atrue%2C%22includePromotedContent%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Afalse%2C%22withUserResults%22%3Atrue%2C%22withBirdwatchPivots%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Afalse%2C%22withVoice%22%3Atrue%7D'''
        else:
            data = '''%7B%22userId%22%3A%22''' + user + '''%22%2C%22count%22%3A20%2C%22withTweetQuoteCount%22%3Atrue%2C%22includePromotedContent%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Afalse%2C%22withUserResults%22%3Atrue%2C%22withBirdwatchPivots%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Afalse%2C%22withVoice%22%3Atrue%7D'''
    elif typed == 2:
        if pages:
            data = '''%7B%22userId%22%3A%22''' + user + '''%22%2C%22count%22%3A40%2C%22cursor%22%3A%22''' + pages + '''%22%2C%22includePromotedContent%22%3Atrue%2C%22withCommunity%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withDownvotePerspective%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Afalse%2C%22__fs_interactive_text%22%3Afalse%2C%22__fs_responsive_web_uc_gql_enabled%22%3Afalse%2C%22__fs_dont_mention_me_view_api_enabled%22%3Afalse%7D'''
        else:
            data = '''%7B%22userId%22%3A%22''' + user + '''%22%2C%22count%22%3A40%2C%22includePromotedContent%22%3Atrue%2C%22withCommunity%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withDownvotePerspective%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Afalse%2C%22__fs_interactive_text%22%3Afalse%2C%22__fs_responsive_web_uc_gql_enabled%22%3Afalse%2C%22__fs_dont_mention_me_view_api_enabled%22%3Afalse%7D'''
    else:
        """
        {
             "screen_name":f"{user}",
             "withSafetyModeUserFields":True,
             "withSuperFollowsUserFields":False
         }
        """
        data = '''%7B%22screen_name%22%3A%22''' + user + '''%22%2C%22withSafetyModeUserFields%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Afalse%7D'''
    return data


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
        self.workbook.remove("sheet")
        self.workbook.save(self.filename)


class Tweet(dict):
    def __init__(self, raw_response, raw_tweet, http, get_threads=False, is_legacy_user=False):  # noqa
        super().__init__()
        self.http = http
        self.__raw_response = raw_response
        self.__raw_tweet = raw_tweet
        self.__is_legacy_user = is_legacy_user
        self.__formatted_tweet = self._format_tweet()
        self.id = None

        if get_threads:
            self._get_threads()

        for key, value in self.__formatted_tweet.items():
            setattr(self, key, value)
            self[key] = value

    def __repr__(self):
        return f"Tweet(id={self.id}, author={self.author}, created_on={self.created_on}, threads={len(self.threads) if self.threads else None})"  # noqa

    def __iter__(self):
        if self.threads:  # noqa
            for thread_ in self.threads:  # noqa
                yield thread_

    @deprecated
    def to_dict(self):
        return self.__formatted_tweet

    def _format_tweet(self):
        original_tweet = self.__raw_tweet['legacy'] if self.__raw_tweet.get("legacy") else self.__raw_tweet
        self.id = tweet_rest_id = self.__raw_tweet['rest_id']
        tweet_author = self.__raw_tweet['core']
        tweet_card = self.__raw_tweet.get("card")

        is_retweet = True if str(original_tweet.get('full_text', "")).startswith("RT") else False
        is_reply = True if original_tweet.get('in_reply_to_status_id') is not None or original_tweet.get(
            'in_reply_to_user_id') is not None or original_tweet.get('in_reply_to_screen_name') is not None else False

        return {
            "created_on": dateutil.parser.parse(original_tweet.get("created_at")),
            "author": UserLegacy(tweet_author) if self.__is_legacy_user else User(tweet_author, 3),
            "is_retweet": is_retweet,
            "is_reply": is_reply,
            "id": tweet_rest_id,
            "tweet_body": self._get_tweet_text(original_tweet, is_retweet),
            "text": self._get_tweet_text(original_tweet, is_retweet),
            "language": original_tweet['lang'] if original_tweet.get('lang') else "",
            "likes": original_tweet['favorite_count'] if original_tweet.get("favorite_count") else 0,
            "card": Card(tweet_card) if tweet_card else None,
            "place": Place(original_tweet['place']) if original_tweet.get('place') else None,
            "retweet_counts": original_tweet['retweet_count'] if original_tweet.get('retweet_count') else 0,
            "source": str(original_tweet['source']).split(">")[1].split("<")[0] if original_tweet.get('source') else "",
            "media": self._get_tweet_media(original_tweet),
            "user_mentions": self._get_tweet_mentions(original_tweet),
            "urls": self._get_tweet_urls(original_tweet),
            "hashtags": self._get_tweet_hashtags(original_tweet),
            "symbols": self._get_tweet_symbols(original_tweet),
            "reply_to": original_tweet['in_reply_to_screen_name'] if is_reply else None,
            "threads": [],
            "comments": []
        }

    def _get_threads(self):
        if not self.__raw_response:
            self.__raw_response = self.http.get_tweet_detail(self.id)  # noqa

        for entry in self.__raw_response.json()['data']['threaded_conversation_with_injections']['instructions'][0]['entries']:
            if str(entry['entryId']).split("-")[0] == "conversationthread":
                for item in entry['content']['items']:
                    try:
                        tweetType = item["item"]["itemContent"]["tweetDisplayType"]
                        tweet = item['item']['itemContent']['tweet_results']['result']
                        self.__formatted_tweet['threads' if tweetType == "SelfThread" else 'comments'].append(
                            Tweet(None, tweet, self.http))
                    except KeyError as e:
                        pass

    @staticmethod
    def _get_tweet_text(original_tweet, is_retweet):
        if is_retweet:
            return original_tweet['retweeted_status_result']['result']['legacy']['full_text']

        if original_tweet.get('full_text'):
            return original_tweet['full_text']

        return ""

    @staticmethod
    def _get_tweet_media(original_tweet):
        if not original_tweet.get("extended_entities"):
            return []

        if not original_tweet['extended_entities'].get("media"):
            return []

        return [Media(media) for media in original_tweet['extended_entities']['media']]

    @staticmethod
    def _get_tweet_mentions(original_tweet):
        if not original_tweet.get("entities"):
            return []

        if not original_tweet['entities'].get("user_mentions"):
            return []

        return [ShortUser(user) for user in original_tweet['entities']['user_mentions']]

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
    def __init__(self, media_dict):
        super().__init__()
        self.__dictionary = media_dict
        self.display_url = self.__dictionary.get("display_url")
        self.expanded_url = self.__dictionary.get("expanded_url")
        self.id = self.__dictionary.get("id_str")
        self.indices = self.__dictionary.get("indices")
        self.media_url_https = self.__dictionary.get("media_url_https")
        self.type = self.__dictionary.get("type")
        self.url = self.__dictionary.get("url")
        self.features = self.__dictionary.get("features")
        self.media_key = self.__dictionary.get("media_key")
        self.mediaStats = self.__dictionary.get("mediaStats")
        self.sizes = self.__dictionary.get("sizes")
        self.original_info = self.__dictionary.get("original_info")
        self.file_format = self.media_url_https.split(".")[-1] if self.type == "photo" else None
        self.streams = []
        if self.type == "video" or self.type == "animated_gif":
            self.__parse_video_streams()

        for k, v in vars(self).items():
            if not k.startswith("_"):
                self[k] = v

    def __parse_video_streams(self):
        videoDict = self.__dictionary.get("video_info")
        if videoDict:
            for i in videoDict.get("variants"):
                if not i.get("content_type").split("/")[-1] == "x-mpegURL":
                    self.streams.append(
                        Stream(i, videoDict.get("duration_millis", 0), videoDict.get("aspect_ratio"))
                    )

    def __repr__(self):
        return f"Media(id={self.id}, type={self.type})"

    def download(self, filename_, show_progress=True):
        if show_progress:
            show_progress = bar_progress
        else:
            show_progress = None

        if self.type == "photo":
            filename = f"{filename_}.{self.file_format}"
            wget.download(url=self.media_url_https, out=filename, bar=show_progress)
            if show_progress:
                sys.stdout.write("\n")
            return filename

        elif self.type == "video":
            _res = [int(stream.res) for stream in self.streams if stream.res]
            max_res = max(_res)
            for stream in self.streams:
                if int(stream.res) == max_res:
                    file_format = stream.content_type.split("/")[-1]
                    if not file_format == "x-mpegURL":
                        filename = f"{filename_}.{file_format}"
                        wget.download(url=stream.url, out=filename, bar=show_progress)
                        if show_progress:
                            sys.stdout.write("\n")
                        return filename

        elif self.type == "animated_gif":
            file_format = self.streams[0].content_type.split("/")[-1]
            if not file_format == "x-mpegURL":
                filename = f"{filename_}.{file_format}"
                wget.download(url=self.streams[0].url, out=filename, bar=show_progress)
                if show_progress:
                    sys.stdout.write("\n")
                return filename
        return None

    @deprecated
    def to_dict(self):
        return self.__dictionary


class Stream(dict):
    def __init__(self, videoDict, length, ratio):
        super().__init__()
        self.__dictionary = videoDict
        self.bitrate = self.__dictionary.get("bitrate")
        self.content_type = self.__dictionary.get("content_type")
        self.url = self.__dictionary.get("url")
        self.length = length
        self.aspect_ratio = ratio
        try:
            self.res = int(self.url.split("/")[7].split("x")[0]) * int(self.url.split("/")[7].split("x")[1])
        except (ValueError, IndexError):
            try:
                self.res = int(self.url.split("/")[6].split("x")[0]) * int(self.url.split("/")[6].split("x")[1])
            except (ValueError, IndexError):
                self.res = None

        for k, v in vars(self).items():
            if not k.startswith("_"):
                self[k] = v

    def __repr__(self):
        return f"Stream(content_type={self.content_type}, length={self.length}, bitrate={self.bitrate}, res={self.res})"

    def download(self, filename_=None, show_progress=False):
        if show_progress:
            show_progress = bar_progress
        else:
            show_progress = None
        file_format = self.content_type.split("/")[-1]
        if filename_:
            filename = f"{filename_}.{file_format}"
        else:
            filename = None
        wget.download(url=self.url, out=filename, bar=show_progress)
        if show_progress:
            sys.stdout.write("\n")
        return filename


class ShortUser(dict):
    def __init__(self, user_dict):
        super().__init__()
        self.__dictionary = user_dict
        self.id = self.__dictionary.get("id_str")
        self.name = self.__dictionary.get("name")
        self.screen_name = self.__dictionary.get("screen_name")

        for k, v in vars(self).items():
            if not k.startswith("_"):
                self[k] = v

    def __repr__(self):
        return f"ShortUser(id={self.id}, name={self.name})"

    def to_dict(self):
        return self.__dictionary


class User(dict):
    def __init__(self, user_dict, type_=1):
        super().__init__()
        if type_ == 1:
            self.__dictionary = user_dict['data']['user']['result']
        elif type_ == 2:
            self.__dictionary = user_dict
        else:
            self.__dictionary = user_dict['user_results']['result']

        self.id = self.__dictionary.get("id")

        self.rest_id = self.__dictionary.get("rest_id") if self.__dictionary.get("rest_id") else self.__dictionary.get(
            "id_str")

        self.created_at = parser.parse(self.__dictionary.get("created_at")) if type_ == 2 else parser.parse(
            self.__dictionary.get("legacy").get("created_at"))

        self.default_profile = self.__dictionary.get("default_profile") if type_ == 2 else self.__dictionary.get(
            "legacy").get("default_profile")

        self.default_profile_image = self.__dictionary.get(
            "default_profile_image") if type_ == 2 else self.__dictionary.get("legacy").get("default_profile_image")

        self.description = self.__dictionary.get("description") if type_ == 2 else self.__dictionary.get("legacy").get(
            "description")

        self.entities = self.__dictionary.get("description") if type_ == 2 else self.__dictionary.get("legacy").get(
            "entities")

        self.fast_followers_count = self.__dictionary.get(
            "fast_followers_count") if type_ == 2 else self.__dictionary.get("legacy").get("fast_followers_count")

        self.favourites_count = self.__dictionary.get("favourites_count") if type_ == 2 else self.__dictionary.get(
            "legacy").get("favourites_count")

        self.followers_count = self.__dictionary.get("followers_count") if type_ == 2 else self.__dictionary.get(
            "legacy").get("followers_count")

        self.friends_count = self.__dictionary.get("friends_count") if type_ == 2 else self.__dictionary.get(
            "legacy").get("friends_count")

        self.has_custom_timelines = self.__dictionary.get(
            "has_custom_timelines") if type_ == 2 else self.__dictionary.get("legacy").get("has_custom_timelines")

        self.is_translator = self.__dictionary.get("is_translator") if type_ == 2 else self.__dictionary.get(
            "legacy").get("is_translator")

        self.listed_count = self.__dictionary.get("listed_count") if type_ == 2 else self.__dictionary.get(
            "legacy").get("listed_count")

        self.location = self.__dictionary.get("location") if type_ == 2 else self.__dictionary.get("legacy").get(
            "location")

        self.media_count = self.__dictionary.get("media_count") if type_ == 2 else self.__dictionary.get("legacy").get(
            "media_count")

        self.name = self.__dictionary.get("name") if type_ == 2 else self.__dictionary.get("legacy").get("name")

        self.normal_followers_count = self.__dictionary.get(
            "normal_followers_count") if type_ == 2 else self.__dictionary.get("legacy").get("normal_followers_count")

        self.profile_banner_url = self.__dictionary.get("profile_banner_url") if type_ == 2 else self.__dictionary.get(
            "legacy").get("profile_banner_url")

        self.profile_image_url_https = self.__dictionary.get(
            "profile_image_url_https") if type_ == 2 else self.__dictionary.get("legacy").get("profile_image_url_https")

        self.profile_interstitial_type = self.__dictionary.get(
            "profile_interstitial_type") if type_ == 2 else self.__dictionary.get("legacy").get(
            "profile_interstitial_type")

        self.protected = self.__dictionary.get("protected") if type_ == 2 else self.__dictionary.get("legacy").get(
            "protected")

        self.screen_name = self.__dictionary.get("screen_name") if type_ == 2 else self.__dictionary.get("legacy").get(
            "screen_name")

        self.statuses_count = self.__dictionary.get("statuses_count") if type_ == 2 else self.__dictionary.get(
            "legacy").get("statuses_count")

        self.translator_type = self.__dictionary.get("translator_type") if type_ == 2 else self.__dictionary.get(
            "legacy").get("translator_type")

        self.verified = self.__dictionary.get("verified") if type_ == 2 else self.__dictionary.get("legacy").get(
            "verified")

        self.profile_url = "https://twitter.com/{}".format(self.screen_name)

        for k, v in vars(self).items():
            if not k.startswith("_"):
                self[k] = v

    def __repr__(self):
        return f"User(id={self.rest_id}, name={self.name}, screen_name={self.screen_name}, followers={self.followers_count}, verified={self.verified})"

    @deprecated
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


class UserLegacy(dict):
    def __init__(self, user_dict):
        super().__init__()
        self.__dictionary = user_dict
        self.id = self.__dictionary.get("id")
        self.rest_id = self.__dictionary.get("id")
        self.created_at = parser.parse(self.__dictionary.get("created_at")) if self.__dictionary.get(
            "created_at") else None
        self.default_profile = self.__dictionary.get("default_profile")
        self.default_profile_image = self.__dictionary.get("default_profile_image")
        self.description = self.__dictionary.get("description")
        self.entities = self.__dictionary.get("entities")
        self.fast_followers_count = self.__dictionary.get("fast_followers_count")
        self.favourites_count = self.__dictionary.get("favourites_count")
        self.followers_count = self.__dictionary.get("followers_count")
        self.friends_count = self.__dictionary.get("friends_count")
        self.has_custom_timelines = self.__dictionary.get("has_custom_timelines")
        self.is_translator = self.__dictionary.get("is_translator")
        self.listed_count = self.__dictionary.get("listed_count")
        self.location = self.__dictionary.get("location")
        self.media_count = self.__dictionary.get("media_count")
        self.name = self.__dictionary.get("name")
        self.normal_followers_count = self.__dictionary.get("normal_followers_count")
        self.profile_banner_url = self.__dictionary.get("profile_banner_url")
        self.profile_image_url_https = self.__dictionary.get("profile_image_url_https")
        self.profile_interstitial_type = self.__dictionary.get("profile_interstitial_type")
        self.protected = self.__dictionary.get("protected")
        self.screen_name = self.__dictionary.get("screen_name")
        self.statuses_count = self.__dictionary.get("statuses_count")
        self.translator_type = self.__dictionary.get("translator_type")
        self.verified = self.__dictionary.get("verified")
        self.profile_url = "https://twitter.com/{}".format(self.screen_name)

        for k, v in vars(self).items():
            if not k.startswith("_"):
                self[k] = v

    def __repr__(self):
        return f"User(id={self.rest_id}, name={self.name}, followers={self.followers_count} , verified={self.verified})"

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
        self.user_ref = [User(user, 2) for user in self._dict['legacy']["user_refs"]] if self._dict['legacy'].get("user_refs") else []
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
        return f"Card(id={self.rest_id}, choices={len(self.choices) if self.choices else []}, end_time={self.end_time}, duration={len(self.duration)} minutes)"


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
