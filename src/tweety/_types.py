import csv
import openpyxl

WORKBOOK_HEADERS = ['Created on','author', 'is_retweet', 'is_reply', 'tweet_id', 'tweet_body', 'language', 'likes',
                    'retweet_count', 'source', 'medias', 'user_mentioned', 'urls', 'hashtags', 'symbols']


class UserTweets:
    def __init__(self, dictionary,user):
        self.dict_ = dictionary
        self.user = user

    def to_xlsx(self, filename=None):
        if self.dict_.get("error") is None:
            wb = openpyxl.Workbook()
            ws = wb.active
            for v, i in enumerate(WORKBOOK_HEADERS):
                ws.cell(row=1, column=v + 1).value = i
            max_row = 1
            all_tweets = self.dict_['tweets']
            for p in all_tweets:
                p = p.to_dict()
                ws[f'A{max_row + 1}'] = p['created_on']
                ws[f'B{max_row + 1}'] = p['author'].name
                ws[f'C{max_row + 1}'] = p['is_retweet']
                ws[f'D{max_row + 1}'] = p['is_reply']
                ws[f'E{max_row + 1}'] = p['tweet_id']
                ws[f'F{max_row + 1}'] = p['tweet_body']
                ws[f'G{max_row + 1}'] = p['language']
                ws[f'H{max_row + 1}'] = p['likes']
                ws[f'I{max_row + 1}'] = p['retweet_counts']
                ws[f'J{max_row + 1}'] = p['source']
                media_ = ""
                if not isinstance(p['media'], str) and p['media'] is not None:
                    for media in p['media']:
                        media_ = f"{media_} {media.expanded_url};"
                    ws[f'K{max_row + 1}'] = media_
                else:
                    ws[f'K{max_row + 1}'] = p['media']
                user_mentions = ""
                if not isinstance(p['user_mentions'], str) and p['user_mentions'] is not None:
                    for user in p['user_mentions']:
                        user_mentions = f"{user_mentions} {user.screen_name};"
                    ws[f'L{max_row + 1}'] = user_mentions
                else:
                    ws[f'L{max_row + 1}'] = p['user_mentions']
                urls = ""
                if not isinstance(p['urls'], str):
                    for url in p['urls']:
                        urls = f"{urls} {url['expanded_url']};"
                    ws[f'M{max_row + 1}'] = urls
                else:
                    ws[f'M{max_row + 1}'] = p['urls']
                hashtags = ""
                if not isinstance(p['hashtags'], str):
                    for tag in p['hashtags']:
                        hashtags = f"{hashtags} {tag['text']};"
                    ws[f'N{max_row + 1}'] = hashtags
                else:
                    ws[f'N{max_row + 1}'] = p['hashtags']
                ws[f'O{max_row + 1}'] = p['symbols']
                max_row = max_row + 1
            if not filename:
                filename = f"tweets-{self.user}.xlsx"
            wb.save(filename)
        else:
            return self.dict_['error']

    def to_csv(self,filename=None):
        all_tweets = self.dict_['tweets']
        if not filename:
            filename = f"tweets-{self.user}.csv"
        with open(filename,"w",encoding="ASCII",errors="ignore",newline="") as csv_:
            writer = csv.writer(csv_)
            writer.writerow(WORKBOOK_HEADERS)
            for p in all_tweets:
                p = p.to_dict()
                created_on = p.get('created_at') if p.get('created_at') else p.get('created_on')
                author = p['author'].name
                is_retweet = p['is_retweet']
                is_reply = p['is_reply']
                tweet_id = p['tweet_id']
                tweet_body = p['tweet_body']
                language = p['language']
                likes = p['likes']
                retweet_count = p['retweet_counts']
                source = p['source']
                symbols = p['symbols']
                media_ = ""
                if not isinstance(p['media'], str) and p['media'] is not None:
                    for media in p['media']:
                        media_ = f"{media_} {media.expanded_url};"
                else:
                    media_ = p['media']
                user_mentions = ""
                if not isinstance(p['user_mentions'], str) and p['user_mentions'] is not None:
                    for user in p['user_mentions']:
                        user_mentions = f"{user_mentions} {user.screen_name};"
                else:
                    user_mentions = p['user_mentions']
                hashtags = ""
                if not isinstance(p['hashtags'], str):
                    for tag in p['hashtags']:
                        hashtags = f"{hashtags} {tag['text']};"
                else:
                    hashtags = p['hashtags']
                urls = ""
                if not isinstance(p['urls'], str):
                    for url in p['urls']:
                        urls = f"{urls} {url['expanded_url']};"
                else:
                    urls = p['urls']
                row = [created_on,author,is_retweet,is_reply,tweet_id,tweet_body,language,likes,retweet_count,source,media_,user_mentions,urls,hashtags,symbols]
                writer.writerow(row)

    def to_dict(self):
        return self.dict_

    def __repr__(self):
        return f"<UserTweets (user={self.user}) (count={len(self.dict_['tweets'])})>"


class Tweet:
    def __init__(self,tweet_dict):
        self.__dictionary = tweet_dict
        self.id = self.__dictionary.get("tweet_id")
        self.author = self.__dictionary.get("author")
        self.created_on = self.__dictionary.get("created_on")
        self.is_retweet = self.__dictionary.get("is_retweet")
        self.is_reply = self.__dictionary.get("is_reply")
        self.tweet_body = self.__dictionary.get("tweet_body")
        self.language = self.__dictionary.get("language")
        self.likes = self.__dictionary.get("likes")
        self.retweet_counts = self.__dictionary.get("retweet_counts")
        self.media = self.__dictionary.get("media")
        self.user_mentions = self.__dictionary.get("user_mentions")
        self.urls = self.__dictionary.get("urls")
        self.hashtags = self.__dictionary.get("hashtags")
        self.symbols = self.__dictionary.get("symbols")
        self.reply_to = self.__dictionary.get("reply_to")

    def __repr__(self):
        return f"<Tweet (id={self.id}) (author={self.author}) (created_on={self.created_on})>"

    def to_dict(self):
        return self.__dictionary


class Media:
    def __init__(self,media_dict):
        self.__dictionary = media_dict
        self.display_url = self.__dictionary.get("display_url")
        self.expanded_url = self.__dictionary.get("expanded_url")
        self.id = self.__dictionary.get("id_str")
        self.indices = self.__dictionary.get("indices")
        self.media_url_https = self.__dictionary.get("media_url_https")
        self.type = self.__dictionary.get("type")
        self.url = self.__dictionary.get("url")
        self.features = self.__dictionary.get("features")
        self.sizes = self.__dictionary.get("sizes")
        self.original_info = self.__dictionary.get("original_info")

    def __repr__(self):
        return f"<Media (id={self.id}) (type={self.type})>"

    def to_dict(self):
        return self.__dictionary


class ShortUser:
    def __init__(self,user_dict):
        self.__dictionary = user_dict
        self.id = self.__dictionary.get("id_str")
        self.name = self.__dictionary.get("name")
        self.screen_name = self.__dictionary.get("screen_name")

    def __repr__(self):
        return f"<ShortUser (id={self.id}) (name={self.name})>"

    def to_dict(self):
        return self.__dictionary


class User:
    def __init__(self,user_dict,type_=1):
        self.__dictionary = user_dict['data']['user']['result'] if type_ == 1 else user_dict['user_results']['result']
        self.id = self.__dictionary.get("id")
        self.rest_id = self.__dictionary.get("rest_id")
        self.created_at = self.__dictionary.get("legacy").get("created_at")
        self.default_profile = self.__dictionary.get("legacy").get("default_profile")
        self.default_profile_image = self.__dictionary.get("legacy").get("default_profile_image")
        self.description = self.__dictionary.get("legacy").get("description")
        self.entities = self.__dictionary.get("legacy").get("entities")
        self.fast_followers_count = self.__dictionary.get("legacy").get("fast_followers_count")
        self.favourites_count = self.__dictionary.get("legacy").get("favourites_count")
        self.followers_count = self.__dictionary.get("legacy").get("followers_count")
        self.friends_count = self.__dictionary.get("legacy").get("friends_count")
        self.has_custom_timelines = self.__dictionary.get("legacy").get("has_custom_timelines")
        self.is_translator = self.__dictionary.get("legacy").get("is_translator")
        self.listed_count = self.__dictionary.get("legacy").get("listed_count")
        self.location = self.__dictionary.get("legacy").get("location")
        self.media_count = self.__dictionary.get("legacy").get("media_count")
        self.name = self.__dictionary.get("legacy").get("name")
        self.normal_followers_count = self.__dictionary.get("legacy").get("normal_followers_count")
        self.profile_banner_url = self.__dictionary.get("legacy").get("profile_banner_url")
        self.profile_image_url_https = self.__dictionary.get("legacy").get("profile_image_url_https")
        self.profile_interstitial_type = self.__dictionary.get("legacy").get("profile_interstitial_type")
        self.protected = self.__dictionary.get("legacy").get("protected")
        self.screen_name = self.__dictionary.get("legacy").get("screen_name")
        self.statuses_count = self.__dictionary.get("legacy").get("statuses_count")
        self.translator_type = self.__dictionary.get("legacy").get("translator_type")
        self.verified = self.__dictionary.get("legacy").get("verified")

    def __repr__(self):
        return f"<User (id={self.rest_id}) (name={self.name}) (followers={self.followers_count}) (verified={self.verified})>"

    def to_dict(self):
        return self.__dictionary


class Search:
    def __init__(self, dictionary, keyword):
        self.dict_ = dictionary
        self.keyword = keyword

    def to_xlsx(self, filename=None):
        if self.dict_.get("error") is None:
            wb = openpyxl.Workbook()
            ws = wb.active
            for v, i in enumerate(WORKBOOK_HEADERS):
                ws.cell(row=1, column=v + 1).value = i
            max_row = 1
            all_tweets = self.dict_['tweets']
            for p in all_tweets:
                p = p.to_dict()
                ws[f'A{max_row + 1}'] = p['created_on']
                ws[f'B{max_row + 1}'] = p['author'].name
                ws[f'C{max_row + 1}'] = p['is_retweet']
                ws[f'D{max_row + 1}'] = p['is_reply']
                ws[f'E{max_row + 1}'] = p['tweet_id']
                ws[f'F{max_row + 1}'] = p['tweet_body']
                ws[f'G{max_row + 1}'] = p['language']
                ws[f'H{max_row + 1}'] = p['likes']
                ws[f'I{max_row + 1}'] = p['retweet_counts']
                ws[f'J{max_row + 1}'] = p['source']
                media_ = ""
                if not isinstance(p['media'], str) and p['media'] is not None:
                    for media in p['media']:
                        media_ = f"{media_} {media.expanded_url};"
                    ws[f'K{max_row + 1}'] = media_
                else:
                    ws[f'K{max_row + 1}'] = p['media']
                user_mentions = ""
                if not isinstance(p['user_mentions'], str) and p['user_mentions'] is not None:
                    for user in p['user_mentions']:
                        user_mentions = f"{user_mentions} {user.screen_name};"
                    ws[f'L{max_row + 1}'] = user_mentions
                else:
                    ws[f'L{max_row + 1}'] = p['user_mentions']
                urls = ""
                if not isinstance(p['urls'], str):
                    for url in p['urls']:
                        urls = f"{urls} {url['expanded_url']};"
                    ws[f'M{max_row + 1}'] = urls
                else:
                    ws[f'M{max_row + 1}'] = p['urls']
                hashtags = ""
                if not isinstance(p['hashtags'], str):
                    for tag in p['hashtags']:
                        hashtags = f"{hashtags} {tag['text']};"
                    ws[f'N{max_row + 1}'] = hashtags
                else:
                    ws[f'N{max_row + 1}'] = p['hashtags']
                ws[f'O{max_row + 1}'] = p['symbols']
                max_row = max_row + 1
            if not filename:
                filename = f"searches-{self.keyword}.xlsx"
            wb.save(filename)
        else:
            return self.dict_['error']

    def to_csv(self, filename=None):
        all_tweets = self.dict_['tweets']
        if not filename:
            filename = f"searches-{self.keyword}.csv"
        with open(filename, "w", encoding="ASCII", errors="ignore", newline="") as csv_:
            writer = csv.writer(csv_)
            writer.writerow(WORKBOOK_HEADERS)
            for p in all_tweets:
                p = p.to_dict()
                created_on = p.get('created_at') if p.get('created_at') else p.get('created_on')
                author = p['author'].name
                is_retweet = p['is_retweet']
                is_reply = p['is_reply']
                tweet_id = p['tweet_id']
                tweet_body = p['tweet_body']
                language = p['language']
                likes = p['likes']
                retweet_count = p['retweet_counts']
                source = p['source']
                symbols = p['symbols']
                media_ = ""
                if not isinstance(p['media'], str) and p['media'] is not None:
                    for media in p['media']:
                        media_ = f"{media_} {media.expanded_url};"
                else:
                    media_ = p['media']
                user_mentions = ""
                if not isinstance(p['user_mentions'], str) and p['user_mentions'] is not None:
                    for user in p['user_mentions']:
                        user_mentions = f"{user_mentions} {user.screen_name};"
                else:
                    user_mentions = p['user_mentions']
                hashtags = ""
                if not isinstance(p['hashtags'], str):
                    for tag in p['hashtags']:
                        hashtags = f"{hashtags} {tag['text']};"
                else:
                    hashtags = p['hashtags']
                urls = ""
                if not isinstance(p['urls'], str):
                    for url in p['urls']:
                        urls = f"{urls} {url['expanded_url']};"
                else:
                    urls = p['urls']
                row = [created_on,author, is_retweet, is_reply, tweet_id, tweet_body, language, likes, retweet_count,
                       source, media_, user_mentions, urls, hashtags, symbols]
                writer.writerow(row)

    def to_dict(self):
        return self.dict_

    def __repr__(self):
        return f"<Search (keyword={self.keyword}) (count={len(self.dict_['tweets'])})>"


class Trends:
    def __init__(self,trends_dict):
        self.__dictionary = trends_dict
        self.name = self.__dictionary.get("name")
        self.url = self.__dictionary.get("url")
        self.tweet_count = self.__dictionary.get("tweet_count")

    def __repr__(self):
        return f"<Trends (name={self.name})>"

    def to_dict(self):
        return self.__dictionary


class UserLegacy:
    def __init__(self,user_dict):
        self.__dictionary = user_dict
        self.id = self.__dictionary.get("id")
        self.rest_id = self.__dictionary.get("id")
        self.created_at = self.__dictionary.get("created_at")
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

    def __repr__(self):
        return f"<User (id={self.rest_id}) (name={self.name}) (followers={self.followers_count}) (verified={self.verified})>"

    def to_dict(self):
        return self.__dictionary
