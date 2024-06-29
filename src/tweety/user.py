import datetime
from typing import Union, Tuple, List
from .exceptions import ListNotFound, ConversationNotFound
from .types.inbox import Message, Conversation
from .utils import create_conversation_id, AuthRequired, find_objects, get_tweet_id
from .types import (User, Mention, Inbox, UploadedMedia, SendMessage, Tweet, Bookmarks, SelfTimeline, TweetLikes,
                    TweetRetweets, Poll, Choice, TweetNotifications, Lists, List as TwList, ListMembers, ListTweets,
                    Topic, TopicTweets, MutualFollowers, ScheduledTweets, ScheduledTweet, HOME_TIMELINE_TYPE_FOR_YOU, TweetAnalytics, BlockedUsers,
                    ShortUser, Place, INBOX_PAGE_TYPE_TRUSTED)
from . import constants


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

    def get_scheduled_tweets(self):
        """
        Get Tweets scheduled by authenticated user
        :return: .types.usertweet.ScheduledTweets
        """
        return ScheduledTweets(self)

    def delete_scheduled_tweet(self, tweet_id):
        """
        Delete a Scheduled Tweet

        :param tweet_id: Tweet ID of the Tweet
        :return: bool
        """

        if isinstance(tweet_id, ScheduledTweet):
            tweet_id = tweet_id.id

        res = self.request.delete_scheduled_tweet(tweet_id)
        return True if find_objects(res, "scheduledtweet_delete", "Done") else False

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

        tweetId = get_tweet_id(tweet_id)

        likes = TweetLikes(tweetId, self, pages, wait_time, cursor)
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

        tweetId = get_tweet_id(tweet_id)

        likes = TweetLikes(tweetId, self, pages, wait_time, cursor)

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

        tweetId = get_tweet_id(tweet_id)

        retweets = TweetRetweets(tweetId, self, pages, wait_time, cursor)
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

        tweetId = get_tweet_id(tweet_id)

        retweets = TweetRetweets(tweetId, self, pages, wait_time, cursor)

        return retweets.generator()

    def get_tweet_quotes(
            self,
            tweet_id: Union[str, Tweet],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """

        :param tweet_id: Tweet ID or the Tweet Object of which the Quotes to get
        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: .types.search.Search
        """

        tweetId = get_tweet_id(tweet_id)

        return self.search(f"quoted_tweet_id:{tweetId}", pages=pages, wait_time=wait_time, cursor=cursor)

    def iter_tweet_quotes(
            self,
            tweet_id: Union[str, Tweet],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """

        :param tweet_id: Tweet ID or the Tweet Object of which the Quotes to get
        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: (.types.search.Search, list[.types.twDataTypes.Tweet])
        """

        tweetId = get_tweet_id(tweet_id)

        return self.iter_search(f"quoted_tweet_id:{tweetId}", pages=pages, wait_time=wait_time, cursor=cursor)

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

        notifications = TweetNotifications(self.me.id, self, pages, wait_time, cursor)

        return notifications.generator()

    def get_inbox(
            self,
            user_id: Union[int, str, User] = None,
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            page_types: Union[str, List[str]] = INBOX_PAGE_TYPE_TRUSTED
    ) -> Inbox:
        """
        :param user_id : (`str`, `int`, `User`) Not Implemented
        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param page_types: list[`str`] Which Type of Conversation to Get | INBOX_PAGE_TYPE_TRUSTED, INBOX_PAGE_TYPE_UNTRUSTED
        :return:
        """

        inbox = Inbox(self.user.id, self, pages, wait_time, page_types)
        list(inbox.generator())
        return inbox

    def iter_inbox(
            self,
            user_id: Union[int, str, User] = None,
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            page_types: Union[str, List[str]] = INBOX_PAGE_TYPE_TRUSTED
    ) -> Inbox:
        """
        :param user_id : (`str`, `int`, `User`) Not Implemented
        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param page_types: list[`str`] Which Type of Conversation to Get | INBOX_PAGE_TYPE_TRUSTED, INBOX_PAGE_TYPE_UNTRUSTED
        :return:
        """

        inbox = Inbox(self.user.id, self, pages, wait_time, page_types)
        return inbox.generator()

    def get_conversation(self, conversation_id: Union[str, Conversation], max_id=None):
        """
            Get a conversation using its ID

        :param conversation_id: Conversation ID
        :param max_id: cursor from which onward you want to get messages
        :return:
        """

        if isinstance(conversation_id, Conversation):
            conversation_id = conversation_id.id

        res = self.request.get_conversation(conversation_id, max_id)
        _conversation_timeline = res.get("conversation_timeline", {})
        this_conv = find_objects(_conversation_timeline, conversation_id, None, recursive=False, none_value=None)

        if not this_conv:
            raise ConversationNotFound(f"Conversation with ID={conversation_id} isn't found")

        return Conversation(this_conv, _conversation_timeline, self)

    def add_member_to_group(
            self,
            members: Union[str, int, list],
            group_id: Union[str, int, Conversation]
    ):

        members = [members] if not isinstance(members, list) else members
        member_ids = []
        for member in members:
            member_ids.append(self.get_user_id(member))

        group_id = group_id.id if isinstance(group_id, Conversation) else group_id

        return self.request.add_group_member(member_ids, group_id)

    def create_conversation_group(
            self,
            participants: List[Union[str, int, User, ShortUser]],
            first_message: str,
            name: str = None
    ):
        """
        Create a Conversation Group

        :param participants: IDs of all the participants you want to add
        :param first_message: First message you want to in the group (Yes it is Required)
        :param name: Name of the group you want to set
        :return: .types.inbox.Conversation
        """

        participants_id = []
        for participant in participants:
            try:
                user_id = self._get_user_id(participant)
                participants_id.append(str(user_id))
            except:
                pass

        participants_id = ",".join(participants_id)
        response = self.request.create_conversation_group(participants_id, first_message)
        new_conversation = list(response["conversations"].values())[0]
        conversation = Conversation(new_conversation, response, self)

        if name:
            self.update_conversation_group_name(conversation, name)
            conversation.name = name

        return conversation

    def update_conversation_group_name(
            self,
            conversation_id: Union[str, int, Conversation],
            name: str
    ):
        """
        Update the name of Conversation Group

        :param conversation_id: ID of the Group
        :param name: New Name of the Group
        :return:
        """

        if isinstance(conversation_id, Conversation):
            conversation_id = conversation_id.id

        self.request.update_conversation_name(conversation_id, name)
        return True

    def update_conversation_group_avatar(
            self,
            conversation_id: Union[str, int, Conversation],
            file: Union[str, UploadedMedia]
    ):
        """
        Update the Avatar/Profile Image of Conversation Group

        :param conversation_id: ID of the Group
        :param file: New Name of the Group
        :return:
        """

        if isinstance(conversation_id, Conversation):
            conversation_id = conversation_id.id

        file = self._upload_media(file)[0].media_id

        self.request.update_conversation_avatar(conversation_id, file)
        return True

    def send_message(
            self,
            username: Union[str, int, User],
            text: str = "",
            file: Union[str, UploadedMedia] = None,
            in_group: bool = False,  # TODO : Find better way,
            reply_to_message_id: Union[int, str, Message] = None,
            audio_only=False,
            quote_tweet_id=None,
    ) -> Message:

        """
        Send Message to a Twitter User
        :param in_group: Message is being sent in group or not
        :param file: (`str`, `UploadedMedia`) File to be sent with message too
        :param username: (`str`, `int`, `User`) Username of the user or id of group whom to send message
        :param text: (`str`) Text to be sent as message
        :param reply_to_message_id: (`str`, `int`, `Message`) Reply to a message in conversation
        :param audio_only: (`bool`) Message media will be sent as audio only
        :param quote_tweet_id: (`str`, `int`, `Tweet`) Quote a Tweet in Message
        :return: .types.inbox.Message

        :example:
            from tweety import Twitter
            client = Twitter()
            client.send_message("elonmusk", "Hi Musk!")
        """

        if not file and not text.strip():
            raise ValueError("'file' and 'text' argument both can't be None")

        if not in_group and "-" not in str(username):
            user_id = self._get_user_id(username)
            conversation_id = create_conversation_id(self.user.id, user_id)
        else:
            conversation_id = username

        if file:
            file = self._upload_media(file, "dm_image")[0].media_id

        if isinstance(reply_to_message_id, Message):
            reply_to_message_id = reply_to_message_id.id

        if isinstance(quote_tweet_id, Tweet):
            quote_tweet_id = quote_tweet_id.id
        elif isinstance(quote_tweet_id, str):
            quote_tweet_id = get_tweet_id(quote_tweet_id)

        return SendMessage(self, conversation_id, text, file, reply_to_message_id, audio_only, quote_tweet_id).send()

    def create_tweet(
            self,
            text: str = "",
            files: List[Union[str, UploadedMedia, Tuple[str, str]]] = None,
            filter_: str = None,
            reply_to: Union[str, int, Tweet] = None,
            quote: Union[str, int, Tweet] = None,
            pool: dict = None,
            place: Union[str, Place] = None,
            batch_compose: bool = False
    ) -> Tweet:

        """
        Create a Tweet

        :param pool: (`dict`) Pool you want to include in the tweet
        :param text: (`str`) Text content of Tweet
        :param files: (`list[Union[str, UploadedMedia, tuple[str, str]]]`) Files to be sent with Tweet (max 4)
        :param filter_: (`str`) Filter to applied for Tweet audience
        :param reply_to: (`str` | `int` | `Tweet`) ID of tweet to reply to
        :param quote: (`str` | `int` | `Tweet`) ID / URL of tweet to be quoted
        :param place: (`str` `Place`) ID of location you want to add
        :param batch_compose: (`bool`) Is this tweet part of thread or not
        :return: Tweet
        """

        if not files and not text.strip():
            raise ValueError("'files' and 'text' argument both can't be None")

        if files:
            files = self._upload_media(files)
        else:
            files = []

        if reply_to and isinstance(reply_to, Tweet):
            reply_to = get_tweet_id(reply_to)

        if quote:
            if isinstance(quote, int) or str(quote).isdigit():
                quote = self.tweet_detail(quote)

            if isinstance(quote, Tweet):
                quote = quote.url

            if str(quote).startswith("https://twitter.com/") or str(quote).startswith("https://x.com/"):
                quote = quote
            else:
                quote = None

        if place and isinstance(place, Place):
            place = place.id

        response = self.request.create_tweet(text, files, filter_, reply_to, quote, pool, place, batch_compose)
        response['data']['create_tweet']['tweet_results']['result']['__typename'] = "Tweet"
        return Tweet(self, response, response)

    def schedule_tweet(
            self,
            date: datetime.datetime,
            text: str = "",
            files: List[Union[str, UploadedMedia, Tuple[str, str]]] = None,
            filter_: str = None,
            reply_to: Union[str, int, Tweet] = None,
            place: Union[str, Place] = None,
    ):
        """
        Schedule a Tweet at specific Time
        :param date: Date and Time at which to execute the Tweet Creation
        :param text: (`str`) Text content of Tweet
        :param files: (`list[Union[str, UploadedMedia, tuple[str, str]]]`) Files to be sent with Tweet (max 4)
        :param filter_: (`str`) Filter to applied for Tweet audience
        :param reply_to: (`str` | `int` | `Tweet`) ID of tweet to reply to
        :param place: (`str` `Place`) ID of location you want to add
        :return: `ID of the Scheduled Tweet`
        """
        if not files and not text.strip():
            raise ValueError("'files' and 'text' argument both can't be None")

        if files:
            files = self._upload_media(files)
        else:
            files = []

        if reply_to and isinstance(reply_to, Tweet):
            reply_to = get_tweet_id(reply_to)

        if place and isinstance(place, Place):
            place = place.id

        if isinstance(date, datetime.datetime):
            date = int(date.timestamp())
        elif isinstance(date, (float, str)):
            date = int(date)

        response = self.request.schedule_tweet(date, text, files, filter_, reply_to, place)
        rest_id = find_objects(response, "rest_id", None)
        return rest_id

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

        user_id = self.get_user_id(username)

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

        user_id = self.get_user_id(username)

        mutualFollowers = MutualFollowers(user_id, self, pages, wait_time, cursor)

        return mutualFollowers.generator()

    def like_tweet(self, tweet_id: Union[str, int, Tweet]):
        """

        :param tweet_id: (`str` | `int` | `Tweet`) ID of tweet to reply to
        :return: Bool
        """

        tweetId = get_tweet_id(tweet_id)

        response = self.request.like_tweet(tweetId)
        return True if find_objects(response, "favorite_tweet", "Done") else False

    def unlike_tweet(self, tweet_id: Union[str, int, Tweet]):
        """

        :param tweet_id: (`str` | `int` | `Tweet`) ID of tweet to reply to
        :return: Bool
        """

        tweetId = get_tweet_id(tweet_id)

        response = self.request.unlike_tweet(tweetId)
        return True if find_objects(response, "unfavorite_tweet", "Done") else False

    def retweet_tweet(self, tweet_id: Union[str, int, Tweet]):
        """

        :param tweet_id: (`str` | `int` | `Tweet`) ID of tweet to reply to
        :return: Bool
        """

        tweetId = get_tweet_id(tweet_id)

        response = self.request.retweet_tweet(tweetId)
        return True if find_objects(response, "rest_id", None) else False

    def delete_retweet(self, tweet_id: Union[str, int, Tweet]):
        """

        :param tweet_id: (`str` | `int` | `Tweet`) ID of tweet to reply to
        :return: Bool
        """

        tweetId = get_tweet_id(tweet_id)

        response = self.request.delete_retweet(tweetId)
        return True if find_objects(response, "rest_id", None) else False

    def bookmark_tweet(self, tweet_id: Union[str, int, Tweet]):
        """

        :param tweet_id: (`str` | `int` | `Tweet`) ID of tweet to be bookmarked
        :return: Bool
        """

        tweetId = get_tweet_id(tweet_id)

        response = self.request.bookmark_tweet(tweetId)
        return True if find_objects(response, "tweet_bookmark_put", "Done") else False

    def delete_bookmark_tweet(self, tweet_id: Union[str, int, Tweet]):
        """

        :param tweet_id: (`str` | `int` | `Tweet`) ID of tweet which was bookmarked and have to be removed
        :return: Bool
        """

        tweetId = get_tweet_id(tweet_id)

        response = self.request.delete_bookmark_tweet(tweetId)
        return True if find_objects(response, "tweet_bookmark_delete", "Done") else False

    def follow_user(self, user_id):
        """

        :param user_id: User Id of the user you want to follow
        :return:
        """

        user_id = self.get_user_id(user_id)
        response = self.request.follow_user(user_id)
        response['__typename'] = "User"
        return User(self, response)

    def unfollow_user(self, user_id):
        """

        :param user_id: User Id of the user you want to unfollow
        :return:
        """

        user_id = self.get_user_id(user_id)

        response = self.request.unfollow_user(user_id)
        response['__typename'] = "User"
        return User(self, response)

    def block_user(self, user_id):
        """

        :param user_id: User Id of the user you want to block
        :return:
        """

        user_id = self.get_user_id(user_id)

        response = self.request.block_user(user_id)
        response['__typename'] = "User"
        return User(self, response)
    
    def unblock_user(self, user_id):
        """

        :param user_id: User Id of the user you want to unblock
        :return:
        """

        user_id = self.get_user_id(user_id)

        response = self.request.unblock_user(user_id)
        response['__typename'] = "User"
        return User(self, response)

    def mute_user(self, user_id):
        """

        :param user_id: User Id of the user you want to block
        :return:
        """

        user_id = self.get_user_id(user_id)

        response = self.request.mute_user(user_id)
        response['__typename'] = "User"
        return User(self, response)

    def unmute_user(self, user_id):
        """

        :param user_id: User Id of the user you want to unblock
        :return:
        """

        user_id = self.get_user_id(user_id)

        response = self.request.unmute_user(user_id)
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

        tweetId = get_tweet_id(tweet_id)

        response = self.request.delete_tweet(tweetId)
        return True if response.get('data', {}).get('delete_tweet') else False

    def enable_user_notification(self, user_id):
        """
        Enable user notification on new tweet from specific user

        :param user_id: User ID of the user you want to apply
        :return: Bool
        """

        user_id = self.get_user_id(user_id)

        self.request.toggle_user_notifications(user_id, True)

        return True

    def disable_user_notification(self, user_id):
        """
        Disable user notification on new tweet from specific user

        :param user_id: User ID of the user you want to apply
        :return: Bool
        """

        user_id = self.get_user_id(user_id)

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

        user_id = self.get_user_id(user_id)

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

        user_id = self.get_user_id(user_id)

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

    def pin_tweet(self, tweet_id):
        """
            Pin a Tweet

        :param tweet_id: (`str`, `int`, `Tweet`)
        :return: bool
        """

        tweetId = get_tweet_id(tweet_id)

        response = self.request.pin_tweet(tweetId)
        return True if find_objects(response, "message", "post pinned successfully") else False

    def unpin_tweet(self, tweet_id):
        """
            UnPin a Tweet

        :param tweet_id: (`str`, `int`, `Tweet`)
        :return: bool
        """

        tweetId = get_tweet_id(tweet_id)

        response = self.request.unpin_tweet(tweetId)
        return True if find_objects(response, "message", "post unpinned successfully") else False

    def upload_media(
            self,
            files=Union[str, List[Union[str, tuple]]],
            upload_type=constants.UPLOAD_TYPE_TWEET_IMAGE
    ):
        """
            Upload a file to Twitter

        :param files: List of files to upload
        :param upload_type: Type of Upload ("tweet_image", "dm_image")
        :return: List[UploadedMedia]
        """

        return self._upload_media(files, upload_type)

    def _upload_media(self, files, _type=constants.UPLOAD_TYPE_TWEET_IMAGE):
        if not isinstance(files, constants.ITERABLE_TYPES):
            files = [files]

        uploaded = []

        for file in files:
            if isinstance(file, constants.ITERABLE_TYPES):
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
                uploaded.append(
                    UploadedMedia(
                        file_path,
                        self,
                        alt_text,
                        None,
                        _type
                    ).upload()
                )

        return uploaded
