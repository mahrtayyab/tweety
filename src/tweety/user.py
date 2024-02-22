from typing import Union, Tuple, List
from .exceptions_ import ListNotFound
from .types.inbox import Message
from .utils import create_conversation_id, AuthRequired, find_objects
from .types import (User, Mention, Inbox, UploadedMedia, SendMessage, Tweet, Bookmarks, SelfTimeline, TweetLikes,
                    TweetRetweets, Poll, Choice, TweetNotifications, Lists, List as TwList, ListMembers, ListTweets,
                    Topic, TopicTweets, MutualFollowers, HOME_TIMELINE_TYPE_FOR_YOU, TweetAnalytics, BlockedUsers)


@AuthRequired
class UserMethods:

    @property
    def me(self) -> User:
        """

        :return:
        """
        return self.user

    @property
    def rate_limits(self):
        return self.request._limits

    def get_home_timeline(
            self,
            timeline_type: str = HOME_TIMELINE_TYPE_FOR_YOU,
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """

        :param timeline_type: Type of TimeLine to get (`HomeTimeline`|`HomeLatestTimeline`)
        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: .types.usertweet.SelfTimeline
        """

        if wait_time is None:
            wait_time = 0

        timeline = SelfTimeline(self.user.id, self, timeline_type, pages, wait_time, cursor)
        list(timeline.generator())

        return timeline

    def iter_home_timeline(
            self,
            timeline_type: str = HOME_TIMELINE_TYPE_FOR_YOU,
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """

        :param timeline_type: Type of TimeLine to get (`HomeTimeline`|`HomeLatestTimeline`)
        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: (.types.usertweet.SelfTimeline, list[.types.twDataTypes.Tweet])
        """

        if wait_time is None:
            wait_time = 0

        timeline = SelfTimeline(self.user.id, self, timeline_type, pages, wait_time, cursor)

        return timeline.generator()

    def get_tweet_likes(
            self,
            tweet_id: Union[str, Tweet],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """

        :param tweet_id: Tweet ID or the Tweet Object of which the Likes to get
        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: .types.likes.TweetLikes
        """

        if isinstance(tweet_id, Tweet):
            tweet_id = tweet_id.id

        likes = TweetLikes(tweet_id, self, pages, wait_time, cursor)
        list(likes.generator())
        return likes

    def iter_tweet_likes(
            self,
            tweet_id: Union[str, Tweet],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """

        :param tweet_id: Tweet ID or the Tweet Object of which the Likes to get
        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: (.types.likes.TweetLikes, list[.types.twDataTypes.User])
        """

        if isinstance(tweet_id, Tweet):
            tweet_id = tweet_id.id

        likes = TweetLikes(tweet_id, self, pages, wait_time, cursor)

        return likes.generator()

    def get_tweet_retweets(
            self,
            tweet_id: Union[str, Tweet],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """

        :param tweet_id: Tweet ID or the Tweet Object of which the Likes to get
        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: .types.retweets.TweetRetweets
        """

        if isinstance(tweet_id, Tweet):
            tweet_id = tweet_id.id

        retweets = TweetRetweets(tweet_id, self, pages, wait_time, cursor)
        list(retweets.generator())
        return retweets

    def iter_tweet_retweets(
            self,
            tweet_id: Union[str, Tweet],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """

        :param tweet_id: Tweet ID or the Tweet Object of which the Likes to get
        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: (.types.retweets.TweetRetweets, list[.types.twDataTypes.User])
        """

        if isinstance(tweet_id, Tweet):
            tweet_id = tweet_id.id

        retweets = TweetRetweets(tweet_id, self, pages, wait_time, cursor)

        return retweets.generator()

    def get_mentions(
            self,
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ) -> Mention:
        """

        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: .types.mention.Mention
        """

        if wait_time is None:
            wait_time = 0

        mentions = Mention(self.user.id, self, pages, wait_time, cursor)
        list(mentions.generator())

        return mentions

    def iter_mentions(
            self,
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """

        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: (.types.mention.Mention, list[.types.twDataTypes.Tweet])
        """

        if wait_time is None:
            wait_time = 0

        mentions = Mention(self.user.id, self, pages, wait_time, cursor)

        return mentions.generator()

    def get_bookmarks(
            self,
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ) -> Bookmarks:
        """

        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: Bookmarks
        """

        if wait_time is None:
            wait_time = 0

        bookmarks = Bookmarks(self.user.id, self, pages, wait_time, cursor)
        list(bookmarks.generator())

        return bookmarks

    def iter_bookmarks(
            self,
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """

        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: (.types.bookmarks.Bookmarks, list[.types.twDataTypes.Tweet])
        """

        if wait_time is None:
            wait_time = 0

        bookmarks = Bookmarks(self.user.id, self, pages, wait_time, cursor)

        return bookmarks.generator()

    def get_tweet_notifications(
            self,
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):

        """
        Get the Notified Tweets of the subscribed users

        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: .types.notification.TweetNotifications
        """
        if wait_time is None:
            wait_time = 0

        notifications = TweetNotifications(self.me.id, self, pages, wait_time, cursor)
        list(notifications.generator())

        return notifications

    def iter_tweet_notifications(
            self,
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """
        Get the Notified Tweets of the subscribed users as Generator

        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: (.types.notification.TweetNotifications, list[.types.twDataTypes.Tweet])
        """

        if wait_time is None:
            wait_time = 0

        notifications = TweetNotifications(self.me.id, self, pages, wait_time, cursor)

        return notifications.generator()

    def get_inbox(
            self,
            user_id: Union[int, str, User] = None,
            cursor: str = None
    ) -> Inbox:
        """
        :param user_id : (`str`, `int`, `User`) User id or username of the user whom to get the messages of. Default is ALL
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
                                It is used to get the messages updates
        :return:
        """

        if user_id:
            user_id = self._get_user_id(user_id)

        inbox = Inbox(user_id, self, cursor)

        return inbox

    def send_message(
            self,
            username: Union[str, int, User],
            text: str,
            file: Union[str, UploadedMedia] = None,
            in_group: bool = False  # TODO : Find better way
    ) -> Message:

        """
        Send Message to a Twitter User
        :param in_group: Message is being sent in group or not
        :param file: (`str`, `UploadedMedia`) File to be sent with message too
        :param username: (`str`, `int`, `User`) Username of the user or id of group whom to send message
        :param text: (`str`) Text to be sent as message
        :return: .types.inbox.Message

        :example:
            from tweety import Twitter
            client = Twitter()
            client.send_message("elonmusk", "Hi Musk!")
        """

        if not in_group:
            user_id = self._get_user_id(username)
            conversation_id = create_conversation_id(self.user.id, user_id)
        else:
            conversation_id = username

        if file:
            file = self._upload_media(file, "dm_image")[0].media_id

        return SendMessage(self, conversation_id, text, file).send()

    def create_tweet(
            self,
            text: str,
            files: List[Union[str, UploadedMedia, Tuple[str, str]]] = None,
            filter_: str = None,
            reply_to: Union[str, int, Tweet] = None,
            quote: Union[str, int, Tweet] = None,
            pool: dict = None
    ) -> Tweet:

        """
        Create a Tweet

        :param pool: Pool you want to include in the tweet
        :param text: (`str`) Text content of Tweet
        :param files: (`list[Union[str, UploadedMedia, tuple[str, str]]]`) Files to be sent with Tweet (max 4)
        :param filter_: (`str`) Filter to applied for Tweet audience
        :param reply_to: (`str` | `int` | `Tweet`) ID of tweet to reply to
        :param quote: (`str` | `int` | `Tweet`) ID / URL of tweet to be quoted
        :return: Tweet
        """

        if files:
            files = self._upload_media(files)
        else:
            files = []

        if reply_to and isinstance(reply_to, Tweet):
            reply_to = reply_to.id

        if not reply_to and quote:
            if isinstance(quote, int) or str(quote).isdigit():
                quote = self.tweet_detail(quote)

            if isinstance(quote, Tweet):
                quote = quote.url

            if str(quote).startswith("https://twitter.com/"):
                quote = quote
            else:
                quote = None
        else:
            quote = None

        response = self.request.create_tweet(text, files, filter_, reply_to, quote, pool)
        response['data']['create_tweet']['tweet_results']['result']['__typename'] = "Tweet"
        return Tweet(self, response, response)

    def iter_lists(
            self,
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """

        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: (.types.lists.Lists, list[.types.twDataTypes.List])
        """

        if wait_time is None:
            wait_time = 0

        lists = Lists(self.user.id, self, pages, wait_time, cursor)

        return lists.generator()

    def get_lists(
            self,
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """

        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: .types.lists.Lists
        """

        if wait_time is None:
            wait_time = 0

        lists = Lists(self.user.id, self, pages, wait_time, cursor)
        list(lists.generator())
        return lists

    def iter_list_member(
            self,
            list_id: Union[str, int, List],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """

        :param list_id: List ID of which to get members of
        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: (.types.lists.ListMembers, list[.types.twDataTypes.User])
        """

        if wait_time is None:
            wait_time = 0

        if isinstance(list_id, TwList):
            list_id = list_id.id

        lists = ListMembers(list_id, self, pages, wait_time, cursor)

        return lists.generator()

    def get_list_member(
            self,
            list_id: Union[str, int, List],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """

        :param list_id: List ID of which to get members of
        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: .types.lists.ListMembers
        """

        if wait_time is None:
            wait_time = 0

        if isinstance(list_id, TwList):
            list_id = list_id.id

        lists = ListMembers(list_id, self, pages, wait_time, cursor)
        list(lists.generator())
        return lists

    def iter_list_tweets(
            self,
            list_id: Union[str, int, List],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """

        :param list_id: List ID of which to get members of
        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: (.types.lists.ListTweets, list[.types.twDataTypes.Tweet])
        """

        if wait_time is None:
            wait_time = 0

        if isinstance(list_id, TwList):
            list_id = list_id.id

        lists = ListTweets(list_id, self, pages, wait_time, cursor)

        return lists.generator()

    def get_list_tweets(
            self,
            list_id: Union[str, int, List],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """

        :param list_id: List ID of which to get members of
        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: .types.lists.ListTweets
        """

        if wait_time is None:
            wait_time = 0

        if isinstance(list_id, TwList):
            list_id = list_id.id

        lists = ListTweets(list_id, self, pages, wait_time, cursor)
        list(lists.generator())
        return lists

    def get_mutual_followers(
            self,
            username: Union[str, int, User],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ) -> MutualFollowers:
        """
         Get the mutual friends of a user

        :param: username: (`str` | `int` | `User`) username of the user whom to get the followers of
        :param: pages: (`int`) number of pages to be scraped
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param: cursor: Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)

        :return: .types.follow.UserFollowers
        """
        if wait_time is None:
            wait_time = 0

        user_id = self._get_user_id(username)

        mutualFollowers = MutualFollowers(user_id, self, pages, wait_time, cursor)

        list(mutualFollowers.generator())

        return mutualFollowers

    def iter_mutual_followers(
            self,
            username: Union[str, int, User],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """
         Get the mutual friends of a user as generator

        :param: username: (`str` | `int` | `User`) username of the user whom to get the followers of
        :param: pages: (`int`) number of pages to be scraped
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param: cursor: Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)

        :return: .types.follow.UserFollowers
        """
        if wait_time is None:
            wait_time = 0

        user_id = self._get_user_id(username)

        mutualFollowers = MutualFollowers(user_id, self, pages, wait_time, cursor)

        return mutualFollowers.generator()

    def like_tweet(self, tweet_id: Union[str, int, Tweet]):
        """

        :param tweet_id: (`str` | `int` | `Tweet`) ID of tweet to reply to
        :return: Bool
        """

        if isinstance(tweet_id, Tweet):
            tweet_id = tweet_id.id

        response = self.request.like_tweet(tweet_id)
        return True if find_objects(response, "favorite_tweet", "Done") else False

    def unlike_tweet(self, tweet_id: Union[str, int, Tweet]):
        """

        :param tweet_id: (`str` | `int` | `Tweet`) ID of tweet to reply to
        :return: Bool
        """

        if isinstance(tweet_id, Tweet):
            tweet_id = tweet_id.id

        response = self.request.unlike_tweet(tweet_id)
        return True if find_objects(response, "unfavorite_tweet", "Done") else False

    def retweet_tweet(self, tweet_id: Union[str, int, Tweet]):
        """

        :param tweet_id: (`str` | `int` | `Tweet`) ID of tweet to reply to
        :return: Bool
        """

        if isinstance(tweet_id, Tweet):
            tweet_id = tweet_id.id

        response = self.request.retweet_tweet(tweet_id)
        return True if find_objects(response, "rest_id", None) else False

    def delete_retweet(self, tweet_id: Union[str, int , Tweet]):
        """

        :param tweet_id: (`str` | `int` | `Tweet`) ID of tweet to reply to
        :return: Bool
        """

        if isinstance(tweet_id, Tweet):
            tweet_id = tweet_id.id

        response = self.request.delete_retweet(tweet_id)
        return True if find_objects(response, "rest_id", None) else False

    def follow_user(self, user_id):
        """

        :param user_id: User Id of the user you want to follow
        :return:
        """

        if isinstance(user_id, User):
            user_id = user_id.id

        response = self.request.follow_user(user_id)
        response['__typename'] = "User"
        return User(self, response)

    def unfollow_user(self, user_id):
        """

        :param user_id: User Id of the user you want to unfollow
        :return:
        """

        if isinstance(user_id, User):
            user_id = user_id.id

        response = self.request.unfollow_user(user_id)
        response['__typename'] = "User"
        return User(self, response)

    def block_user(self, user_id):
        """

        :param user_id: User Id of the user you want to block
        :return:
        """

        if isinstance(user_id, User):
            user_id = user_id.id

        response = self.request.block_user(user_id)
        response['__typename'] = "User"
        return User(self, response)
    
    def unblock_user(self, user_id):
        """

        :param user_id: User Id of the user you want to unblock
        :return:
        """

        if isinstance(user_id, User):
            user_id = user_id.id

        response = self.request.unblock_user(user_id)
        response['__typename'] = "User"
        return User(self, response)

    def pool_vote(self, poll_id, tweet, choice, poll_name=None):
        """

        :param poll_id: (`str`, `Poll`) ID OR URI of the Poll , Or the `Poll` Object
        :param tweet: (`str`, `int`, `Tweet`) Tweet ID in which the Poll was posted
        :param choice: (`str`, `int`, `Choice`) Choice you want to vote to
        :param poll_name: (`str`) Name of the Pool in case the `poll_id` isn't `Poll`
        :return: Poll
        """

        if not isinstance(poll_id, Poll) and not poll_name:
            raise ValueError("`pool_name` is required if `poll_id` isn't `Poll`")

        if isinstance(poll_id, Poll):
            poll_name = poll_id.name
            poll_id = poll_id.id

        if isinstance(tweet, Tweet):
            tweet = tweet.id

        if isinstance(choice, Choice):
            choice = choice.key

        response = self.request.poll_vote(poll_id, poll_name, tweet, choice)
        response['card']['legacy'] = response['card']
        return Poll(self, response['card'])

    def delete_tweet(self, tweet_id):
        """

        :param tweet_id: (`str`, `int`, Tweet) Tweet to be deleted
        :return: Bool
        """

        if isinstance(tweet_id, Tweet):
            tweet_id = tweet_id.id

        response = self.request.delete_tweet(tweet_id)
        return True if response.get('data', {}).get('delete_tweet') else False

    def enable_user_notification(self, user_id):
        """
        Enable user notification on new tweet from specific user

        :param user_id: User ID of the user you want to apply
        :return: Bool
        """

        if isinstance(user_id, User):
            user_id = user_id.id

        self.request.toggle_user_notifications(user_id, True)

        return True

    def disable_user_notification(self, user_id):
        """
        Disable user notification on new tweet from specific user

        :param user_id: User ID of the user you want to apply
        :return: Bool
        """

        if isinstance(user_id, User):
            user_id = user_id.id

        self.request.toggle_user_notifications(user_id, False)
        return True

    def get_list(
            self,
            list_id: Union[str, int, TwList]
    ):
        if isinstance(list_id, TwList):
            return list_id

        response = self.request.get_list(list_id)
        if not response.get('data', {}).get('list', {}).get('name'):
            raise ListNotFound(404, "ListNotFound", None)

        return TwList(self, response['data'])

    def create_list(
            self,
            name: str,
            description: str = "",
            is_private: bool = True
    ):
        """

        :param name: Name of new list
        :param description: Description of new list
        :param is_private: Either the List is private or public
        :return: .types.twDataTypes.List
        """

        response = self.request.create_list(name, description, is_private)
        return TwList(self, response['data'])

    def delete_list(
            self,
            list_id: Union[str, int, TwList],
    ):
        """

        :param list_id: LIST ID to be deleted
        :return: bool
        """

        if isinstance(list_id, TwList):
            list_id = list_id.id

        response = self.request.delete_list(list_id)
        return True if response.get('data', {}).get('list_delete', '') == 'Done' else False

    def add_list_member(
            self,
            list_id: Union[str, int, TwList],
            user_id: Union[str, int, User],
    ):
        if isinstance(list_id, TwList):
            list_id = list_id.id

        if isinstance(user_id, User):
            user_id = user_id.id

        response = self.request.add_list_member(list_id, user_id)
        if not response.get('data', {}).get('list', {}).get('name'):
            raise ListNotFound(404, "ListNotFound", None)

        return TwList(self, response['data'])

    def remove_list_member(
            self,
            list_id: Union[str, int, TwList],
            user_id: Union[str, int, User],
    ):
        if isinstance(list_id, TwList):
            list_id = list_id.id

        if isinstance(user_id, User):
            user_id = user_id.id

        response = self.request.remove_list_member(list_id, user_id)
        if not response.get('data', {}).get('list', {}).get('name'):
            raise ListNotFound(404, "ListNotFound", None)

        return TwList(self, response['data'])

    def get_topic(self, topic_id):
        """

        :param topic_id: ID of the Topic
        :return:
        """

        response = self.request.get_topic_landing_page(topic_id)
        return Topic(self, response)

    def get_topic_tweets(
            self,
            topic_id: Union[str, int, Topic],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ) -> TopicTweets:
        """
            Get Tweets of a Topic

            :param topic_id: Topic ID of which to get tweets of
            :param pages: (`int`) The number of pages to get
            :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
            :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
            :return: .types.lists.TopicTweets
        """

        if isinstance(topic_id, Topic):
            topic_id = topic_id.id

        topic_tweets = TopicTweets(topic_id, self, pages, cursor, wait_time)
        list(topic_tweets.generator())
        return topic_tweets

    def iter_topic_tweets(
            self,
            topic_id: Union[str, int, Topic],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """
            Get Tweets of a Topic as Generator

            :param topic_id: Topic ID of which to get tweets of
            :param pages: (`int`) The number of pages to get
            :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
            :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
            :return: (.types.lists.TopicTweets, List[.types.twDataTypes.Tweet])
        """

        if isinstance(topic_id, Topic):
            topic_id = topic_id.id

        topic_tweets = TopicTweets(topic_id, self, pages, cursor, wait_time)
        return topic_tweets.generator()

    def get_tweet_analytics(self, tweet_id):
        response = self.request.get_tweet_analytics(tweet_id)
        return TweetAnalytics(self, response)

    def get_blocked_users(
            self,
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ) -> BlockedUsers:
        """
            Get Users which have been blocked by the authenticated user

            :param pages: (`int`) The number of pages to get
            :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
            :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
            :return: .types.follow.BlockedUsers
        """

        blocked_users = BlockedUsers(self, pages, wait_time, cursor)
        list(blocked_users.generator())
        return blocked_users

    def iter_blocked_users(
            self,
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """
            Get Users which have been blocked by the authenticated user as iterator

            :param pages: (`int`) The number of pages to get
            :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
            :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
            :return: (.types.follow.BlockedUsers, List[.types.twDataTypes.User])
        """

        blocked_users = BlockedUsers(self, pages, wait_time, cursor)
        return blocked_users.generator()

    def _upload_media(self, files, _type="tweet_image"):
        if not isinstance(files, list):
            files = [files]

        uploaded = []

        for file in files:
            if isinstance(file, (tuple, list)):
                file_path = file[0]
                alt_text = file[1]
            else:
                file_path = file
                alt_text = None

            if isinstance(file_path, UploadedMedia):
                if file_path.media_id is None:
                    uploaded.append(file_path.upload())
                else:
                    uploaded.append(file_path)
            else:
                uploaded.append(UploadedMedia(file_path, self, alt_text, None, _type).upload())

        return uploaded
