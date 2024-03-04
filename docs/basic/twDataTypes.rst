.. _twDataTypes:

=============
TwDataTypes
=============

This page contains all the Data Class

.. py:data:: PROXY_TYPE_SOCKS4 = 1

.. py:data:: PROXY_TYPE_SOCKS5 = 2

.. py:data:: PROXY_TYPE_HTTP = 3



Proxy
-------------------
.. py:class:: Proxy(host: str, port: int, proxy_type: int, username: str = None, password: str = None)

    .. py:data:: Arguments

        .. py:data:: host
            :type: str

            Host of Proxy

        .. py:data:: port
            :type: int

            Port of proxy

        .. py:data:: proxy_type
            :type: int

            Type of Proxy

        .. py:data:: username (optional)
            :type: str

            Username required for authentication

        .. py:data:: password (optional)
            :type: str

            Password required for authentication


UserTweets
---------------------

.. py:class:: UserTweets

    Bases : `BaseGeneratorClass`

    :reference: `tweety.types.usertweet.UserTweets`

    .. py:data:: Attributes:

        .. py:attribute:: tweets
            :type: list[Tweet | SelfThread]

            List of User Tweets

        .. py:attribute:: get_replies
            :type: bool

            Either to get replies or Not

        .. py:attribute:: user_id
            :type: int

            User ID of the user in question

    .. py:data:: Methods:

        .. py:method:: to_xlsx(filename=None)

            Export the User Tweets to Excel

            .. py:data:: Arguments:

                .. py:data:: filename (optional)
                    :type: str
                    :value: None

                    Filename of Excel Workbook

            .. py:data:: Return
                :type: None

UserMedia
---------------------

.. py:class:: UserMedia

    Bases : `BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.usertweet.UserMedia`

    .. py:data:: Attributes:

        .. py:attribute:: tweets
            :type: list[Tweet | SelfThread]

            List of User Tweets

        .. py:attribute:: user_id
            :type: int

            User ID of the user in question

SelfTimeline
---------------------

.. py:class:: SelfTimeline

    Bases : `BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.usertweet.SelfTimeline`

    .. py:data:: Attributes:

        .. py:attribute:: tweets
            :type: list[Tweet | SelfThread]

            List of User Tweets

        .. py:attribute:: timeline_type
            :type: str

            Type of Timeline

        .. py:attribute:: user_id
            :type: int

            User ID of the user in question

TweetComments
---------------------

.. py:class:: TweetComments

    Bases : `BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.usertweet.TweetComments`

    .. py:data:: Attributes:

        .. py:attribute:: tweets
            :type: list[ConversationThread]

            List of Tweet ConversationThreads

        .. py:attribute:: tweet_id
            :type: str

            ID of Tweet

        .. py:attribute:: get_hidden
            :type: bool

            Got hidden comments or not

Search
---------------------
Reference `Search`_.


.. py:class:: Search

    Bases : `BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.search.Search`

    .. py:data:: Attributes:

        .. py:attribute:: results
            :type: list[Tweet | SelfThread | User | List]

            List of Results

        .. py:attribute:: keyword
            :type: str

            keyword which is begin searched

        .. py:attribute:: filter
            :type: str | None

            Any Filter which is begin applied

    .. py:data:: Methods:

        .. py:method:: to_xlsx(filename=None)

            Export the User Tweets to Excel

            .. py:data:: Arguments:

                .. py:data:: filename (optional)
                    :type: str
                    :value: None

                    Filename of Excel Workbook

            .. py:data:: Return
                :type: None

TopicTweets
---------------------

.. py:class:: TopicTweets

    Bases : `BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.topic.TopicTweets`

    .. py:data:: Attributes:

        .. py:attribute:: tweets
            :type: list[Tweet]

            List of Tweets

TweetLikes
---------------------

.. py:class:: TweetLikes

    Bases : `BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.likes.TweetLikes`

    .. py:data:: Attributes:

        .. py:attribute:: users
            :type: list[User]

            List of Users

        .. py:attribute:: user_id
            :type: int

            User ID of the user in question

TweetRetweets
---------------------

.. py:class:: TweetRetweets

    Bases : `BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.likes.TweetRetweets`

    .. py:data:: Attributes:

        .. py:attribute:: users
            :type: list[User]

            List of Users

        .. py:attribute:: user_id
            :type: int

            User ID of the user in question


Mention
---------------------

.. py:class:: Mention

    Bases : `BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.mentions.Mention`

    .. py:data:: Attributes:

        .. py:attribute:: tweets
            :type: list

            List of User Tweets

        .. py:attribute:: user_id
            :type: int

            User ID of the user in question


Bookmarks
---------------------

.. py:class:: Bookmarks

    Bases : `BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.bookmarks.Bookmarks`

    .. py:data:: Attributes:

        .. py:attribute:: tweets
            :type: list

            List of User Tweets

        .. py:attribute:: user_id
            :type: int

            User ID of the user in question

CommunityTweets
---------------------

.. py:class:: CommunityTweets

    Bases : `BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.community.CommunityTweets`

    .. py:data:: Attributes:

        .. py:attribute:: tweets
            :type: list[Tweet | SelfThread]

            List of  Tweets

        .. py:attribute:: filter
            :type: str | None

            Any Filter which is begin applied

    .. py:data:: Methods:

        .. py:method:: to_xlsx(filename=None)

            Export the User Tweets to Excel

            .. py:data:: Arguments:

                .. py:data:: filename (optional)
                    :type: str
                    :value: None

                    Filename of Excel Workbook

            .. py:data:: Return
                :type: None

CommunityMembers
---------------------

.. py:class:: CommunityMembers

    Bases : `BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.community.CommunityMembers`

    .. py:data:: Attributes:

        .. py:attribute:: users
            :type: list[User]

            List of User

        .. py:attribute:: filter
            :type: str | None

            Any Filter which is begin applied

Lists
---------------------

.. py:class:: Lists

    Bases : `BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.lists.Lists`

    .. py:data:: Attributes:

        .. py:attribute:: lists
            :type: list[TwList]

            List of Twitter List

ListMembers
---------------------

.. py:class:: ListMembers

    Bases : `BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.lists.ListMembers`

    .. py:data:: Attributes:

        .. py:attribute:: users
            :type: list[User]

            Users of Twitter List


ListTweets
---------------------

.. py:class:: ListTweets

    Bases : `BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.lists.ListTweets`

    .. py:data:: Attributes:

        .. py:attribute:: tweets
            :type: list[Tweet | SelfThread]

            Tweets of the List

UserFollowers
---------------------

.. py:class:: UserFollowers

    Bases : `BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.follow.UserFollowers`

    .. py:data:: Attributes:

        .. py:attribute:: users
            :type: list[User]

            Users List

UserFollowings
---------------------

.. py:class:: UserFollowings

    Bases : `BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.follow.UserFollowings`

    .. py:data:: Attributes:

        .. py:attribute:: users
            :type: list[User]

            Users List

MutualFollowers
---------------------

.. py:class:: MutualFollowers

    Bases : `BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.follow.MutualFollowers`

    .. py:data:: Attributes:

        .. py:attribute:: users
            :type: list[User]

            Users List

BlockedUsers
---------------------

.. py:class:: BlockedUsers

    Bases : `BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.follow.BlockedUsers`

    .. py:data:: Attributes:

        .. py:attribute:: users
            :type: list[User]

            Users List

TweetNotifications
---------------------

.. py:class:: TweetNotifications

    Bases : `BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.notification.TweetNotifications`

    .. py:data:: Attributes:

        .. py:attribute:: tweets
            :type: list[Tweet]

            List of tweets

Inbox
---------------------

.. py:class:: Inbox

    Bases : `dict`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.inbox.Inbox`

    .. py:data:: Attributes:

        .. py:attribute:: conversations
            :type: list[Conversation]

            List of User Conversation

        .. py:attribute:: messages
            :type: list[Message]

            List of User Message

        .. py:attribute:: cursor
            :type: str

            Pagination cursor to get new message

    .. py:data:: Methods:

        .. py:method:: get_conversation(conversation_id)

            Get conversation of with specific User using its conversation id

            .. py:data:: Arguments:

                .. py:data:: conversation_id
                    :type: str

                    Conversation id of the specific user

            .. py:data:: Return
                :type: Conversation | None


SelfThread
---------------------

.. py:class:: SelfThread

    Bases : `dict`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.twDataTypes.SelfThread`

    .. py:data:: Attributes:

        .. py:attribute:: tweets
            :type: list[Tweet]

            List of Threaded Tweets

        .. py:attribute:: all_tweets_id
            :type: list[str]

            List of all tweet ids in the thread

    .. py:data:: Methods:

        .. py:method:: expand()

            Try getting all the tweets of the thread (by default Twitter returns only 3 Tweets from Thread)


ConversationThread
---------------------

.. py:class:: ConversationThread

    Bases : `dict`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.twDataTypes.ConversationThread`

    .. py:data:: Attributes:

        .. py:attribute:: tweets
            :type: list[Tweet]

            List of Threaded Tweets

        .. py:attribute:: parent
            :type: Tweet

            Parnet Tweet

    .. py:data:: Methods:

        .. py:method:: expand()

            Try getting all the tweets of the thread (by default Twitter returns only 2 Tweets from Thread)


Tweet
---------------------

.. py:class:: Tweet

    Bases : `dict`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.twDataTypes.Tweet`

    .. py:data:: Attributes:

        .. py:attribute:: id
            :type: int

            ID of the Tweet

        .. py:attribute:: created_on
            :type: datetime.datetime

            DateTime at which the Tweet was created

        .. py:attribute:: date
            :type: datetime.datetime

            DateTime at which the Tweet was created

        .. py:attribute:: text
            :type: str

            Text of the Tweet

        .. py:attribute:: rich_text
            :type: RichText

            Text of the Tweet

        .. py:attribute:: author
            :type: User

            Author of the Tweet

        .. py:attribute:: is_retweet
            :type: bool

            Is this Tweet a retweet or not

        .. py:attribute:: retweeted_tweet
            :type: Tweet

            Retweeted Tweet if `is_retweet` is `True`

        .. py:attribute:: is_quoted
            :type: bool

            Is the Tweet quoted or not

        .. py:attribute:: quoted_tweet
            :type: Tweet

            Quoted Tweet if `is_quoted` is `True`

        .. py:attribute:: is_reply
            :type: bool

            Is this Tweet replied in response of any other Tweet

        .. py:attribute:: is_sensitive
            :type: bool

            Does the Tweet contain sensitive content

        .. py:attribute:: reply_counts
            :type: int

            Number of Times someone replied to this Tweet

        .. py:attribute:: quote_counts
            :type: int

            Number of Times this Tweet was Quoted

        .. py:attribute:: replied_to
            :type: Tweet | str

            Tweet this Tweet was sent in response to or USER ID

        .. py:attribute:: bookmark_count
            :type: int

            Number of Times this Tweet was Bookmarked

        .. py:attribute:: views
            :type: int

            Number of Times this Tweet was Viewed

        .. py:attribute:: likes
            :type: int

            Number of Times this Tweet was Liked

        .. py:attribute:: language
            :type: str

            Language of the Tweet (identified by Twitter)

        .. py:attribute:: place
            :type: Place

            Any Place mentioned in the Tweet

        .. py:attribute:: retweet_counts
            :type: int

            Number of Times this Tweet was Retweeted

        .. py:attribute:: source
            :type: str

            Source of Tweet

        .. py:attribute:: has_moderated_replies
            :type: bool

            Are replies on this Tweet moderated

        .. py:attribute:: is_liked
            :type: bool

            is this tweet liked by authenticated user

        .. py:attribute:: is_retweeted
            :type: bool

            is this tweet retweeted by authenticated user

        .. py:attribute:: can_reply
            :type: bool

            can authenticated user reply to this Tweet

        .. py:attribute:: broadcast
            :type: Broadcast | None

            Broadcast

        .. py:attribute:: edit_control
            :type: EditControl | None

            Edit Control of the Tweet

        .. py:attribute:: has_newer_version
            :type: bool

            Do this Tweet was edited and has newer version

        .. py:attribute:: audio_space_id
            :type: str

            Id of the Audio Space in the Tweet

        .. py:attribute:: pool
            :type: Pool | None

            Pool in the Tweet

        .. py:attribute:: community
            :type: Community | None

            Community this tweet is part of

        .. py:attribute:: media
            :type: list[Media]

            Media of the Tweet

        .. py:attribute:: user_mentions
            :type: list[ShortUser]

            Users mentioned in the Tweet

        .. py:attribute:: urls
            :type: list[URL]

            URLs mentioned in the Tweet

        .. py:attribute:: hashtags
            :type: list[Hashtag]

            Hashtags mentioned in the Tweet

        .. py:attribute:: symbols
            :type: list[Symbol]

            Symbols mentioned in the Tweet

        .. py:attribute:: community_note
            :type: str | None

            Community Note posted in response to the Tweet

        .. py:attribute:: url
            :type: str

            URL of the Tweet

        .. py:attribute:: threads
            :type: list[Tweet]

            List of Threaded Tweets

        .. py:attribute:: comments
            :type: list[ConversationThread]

            List of Comments sent in response to this Tweet

    .. py:data:: Methods:

        .. py:method:: get_comments(pages=1, wait_time=2, cursor=None)
        .. py:method:: iter_comments(pages=1, wait_time=2, cursor=None)

            Get the comments / replies posted in response to this tweet

            .. py:data:: Arguments:

                .. py:data:: pages (optional)
                    :type: int
                    :value: 1

                    How many pages to get

                .. py:data:: wait_time (optional)
                    :type: int
                    :value: 2

                    Number of seconds to wait between multiple requests

                .. py:data:: cursor (optional)
                    :type: str
                    :value: None

                    Pagination cursor to get the comments from that cursor up-to

            .. py:data:: Return
                :type: list[Tweet]

        .. py:method:: like()

            Like the Tweet

            .. py:data:: Return
                :type: Bool

        .. py:method:: unlike()

            Un-Like the Tweet

            .. py:data:: Return
                :type: Bool

        .. py:method:: translate()

            Translate the Tweet

            .. py:data:: Return
                :type: TweetTranslate

        .. py:method:: delete()

            Delete the Tweet

            .. py:data:: Return
                :type: Bool

        .. py:method:: download_all_media(progress_callback: Callable[[str, int, int], None] = None)

            Download All Media from Tweet

            .. py:data:: progress_callback (optional)
                :type: Callable[[str, int, int], None]
                :value: None

                Callback function which will called while downloading to track the progress.
                [filename, total_size_in_bytes, downloaded_in_bytes]

        .. py:method:: retweet()

            Retweet the Tweet

            .. py:data:: Return
                :type: Bool

        .. py:method:: get_reply_to()

            Get the Tweet to which this Tweet was sent in reply

            .. py:data:: Return
                :type: Tweet

Media
---------------------

.. py:class:: Media

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.twDataTypes.Media`

    .. py:data:: Attributes:

        .. py:attribute:: id
            :type: str

            Internal ID of the Media

        .. py:attribute:: display_url
            :type: str

            Short Display URL of Media (This will open the Twitter website)

        .. py:attribute:: expanded_url
            :type: str

            Full Display URL of Media (This will open the Twitter website)


        .. py:attribute:: media_url_https
            :type: str

            Direct Link to the Media (thumbnail if media is Video)

        .. py:attribute:: type
            :type: str

            Type of Media (`video` | `photo`)

        .. py:attribute:: url
            :type: str

            Short URL of Tweet

        .. py:attribute:: streams
            :type: list[Stream]

            List of streams available if the `type` is `video`

        .. py:attribute:: mediaStats
            :type: dict

            Stats of the media , usually `viewCount`

        .. py:attribute:: source_user
            :type: User | None

            Source from where the Media was posted

    .. py:data:: Methods:

        .. py:method:: download(filename: str = None, progress_callback: Callable[[str, int, int], None] = None)

            Download the Media

            .. py:data:: Arguments:

                .. py:data:: filename (optional)
                    :type: str
                    :value: None

                    Filename of the Media

                .. py:data:: progress_callback (optional)
                    :type: Callable[[str, int, int], None]
                    :value: None

                    Callback function which will called while downloading to track the progress.
                    [filename, total_size_in_bytes, downloaded_in_bytes]

            .. py:data:: Return
                :type: filename | None

        .. py:method:: best_stream()

            Get Best available Media/Stream

            .. py:data:: Return
                :type: Media | Stream | None

Stream
---------------------

.. py:class:: Stream

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.twDataTypes.Stream`

    .. py:data:: Attributes:

        .. py:attribute:: bitrate
            :type: int

            bitrate of stream audio

        .. py:attribute:: content_type
            :type: str

            Mime-type of the Media

        .. py:attribute:: url
            :type: str

            Direct URL to Stream


        .. py:attribute:: length
            :type: int

            Length of stream in mini-seconds

        .. py:attribute:: aspect_ratio
            :type: list[int,int]

            Aspect Ratio of the Stream

        .. py:attribute:: res
            :type: str

            Resolution of the Stream

    .. py:data:: Methods:

        .. py:method:: download(filename: str = None, progress_callback: Callable[[str, int, int], None] = None)

            Download the Media

            .. py:data:: Arguments:

                .. py:data:: filename (optional)
                    :type: str
                    :value: None

                    Filename of the Media

                .. py:data:: progress_callback (optional)
                    :type: Callable[[str, int, int], None]
                    :value: None

                    Callback function which will called while downloading to track the progress.
                    [filename, total_size_in_bytes, downloaded_in_bytes]

            .. py:data:: Return
                :type: filename | None

ShortUser
---------------------

.. py:class:: ShortUser

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.twDataTypes.ShortUser`

    .. py:data:: Attributes:

        .. py:attribute:: id
            :type: str

            id of the User

        .. py:attribute:: name
            :type: str

            Name of the User

        .. py:attribute:: screen_name
            :type: str

            Username of the User

        .. py:attribute:: username
            :type: str

            Username of the User

Trends
---------------------

.. py:class:: Trends

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.twDataTypes.Trends`

    .. py:data:: Attributes:

        .. py:attribute:: name
            :type: str

            Name of the Trend

        .. py:attribute:: url
            :type: str

            URL of the Trend

        .. py:attribute:: tweet_count
            :type: int

            Number of Tweets this trend has till now

Card
---------------------

.. py:class:: Card

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.twDataTypes.Card`

    .. py:data:: Attributes:

        .. py:attribute:: rest_id
            :type: int

            Id of the card

        .. py:attribute:: name
            :type: str

            Name of the card

        .. py:attribute:: choices
            :type: list[Choice]

            Number of Tweets this trend has till now

        .. py:attribute:: end_time
            :type: datetime.datetime

            End Time of the Pool

        .. py:attribute:: last_updated_time
            :type: datetime.datetime

            Last Updated Time of the Pool

        .. py:attribute:: duration
            :type: str

            Duration of Pool in Minutes

        .. py:attribute:: user_ref
            :type: list[User]

            Users Referred in the Pool


Choice
---------------------

.. py:class:: Choice

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.twDataTypes.Choice`

    .. py:data:: Attributes:

        .. py:attribute:: id
            :type: str

            Id of the pool

        .. py:attribute:: name
            :type: str

            Name of the choice

        .. py:attribute:: value
            :type: str

            Value of the choice

        .. py:attribute:: key
            :type: str

            Key of the choice

        .. py:attribute:: counts
            :type: str

            Number of the votes this `value` has

Place
---------------------

.. py:class:: Place

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.twDataTypes.Place`

    .. py:data:: Attributes:

        .. py:attribute:: name
            :type: str

            Name of the place

        .. py:attribute:: id
            :type: str

            Id of the place

        .. py:attribute:: country
            :type: str

            Country of the place

        .. py:attribute:: full_name
            :type: str

            Full Name of the place

        .. py:attribute:: country_code
            :type: str

            Country Code of the place

        .. py:attribute:: url
            :type: str

            URL of the place

        .. py:attribute:: coordinates
            :type: list[Coordinates]

            Coordinates of the place

Coordinates
---------------------

.. py:class:: Coordinates

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.twDataTypes.Coordinates`

    .. py:data:: Attributes:

        .. py:attribute:: latitude
            :type: float

            Latitude Value of the place

        .. py:attribute:: longitude
            :type: float

            Longitude Value of the place

User
---------------------

.. py:class:: User

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.twDataTypes.User`

    .. py:data:: Attributes:

        .. py:attribute:: id
            :type: int

            Id of the User

        .. py:attribute:: rest_id
            :type: int

            Id of the User

        .. py:attribute:: created_at
            :type: datetime.datetime

            DateTime at which the user was created

        .. py:attribute:: date
            :type: datetime.datetime

            DateTime at which the Tweet was created

        .. py:attribute:: description
            :type: str

            Bio / Description on User Profile

        .. py:attribute:: bio
            :type: str

            Bio / Description on User Profile

        .. py:attribute:: can_dm
            :type: bool

            Can the authenticated user send dm to this user

        .. py:attribute:: is_blocked
            :type: bool

            Is the user blocked by authenticated user

        .. py:attribute:: entities
            :type: dict | None

            Additional entities of user, usually links

        .. py:attribute:: fast_followers_count
            :type: int

            Number of Fast Followers this user has

        .. py:attribute:: favourites_count
            :type: int

            Number of Favourite this user has received

        .. py:attribute:: followers_count
            :type: int

            Number of followers this user has

        .. py:attribute:: friends_count
            :type: int

            Number of friends this user has

        .. py:attribute:: listed_count
            :type: int

            Number of lists this user has

        .. py:attribute:: location
            :type: str | None

            Location of the User

        .. py:attribute:: media_count
            :type: int

            Number of Media this user has posted

        .. py:attribute:: name
            :type: str

            Name of the User

        .. py:attribute:: normal_followers_count
            :type: int

            Number of normal followers count this user has

        .. py:attribute:: profile_banner_url
            :type: str

            Direct URL to the User banner image

        .. py:attribute:: profile_image_url_https
            :type: str

            Direct URL to the User profile image

        .. py:attribute:: protected
            :type: bool

            Is user private or not

        .. py:attribute:: screen_name
            :type: str

            Username of the user

        .. py:attribute:: username
            :type: str

            Username of the user

        .. py:attribute:: statuses_count
            :type: int

            Number of status this user has posted

        .. py:attribute:: verified
            :type: bool

            Is user verified or not.

        .. py:attribute:: possibly_sensitive
            :type: bool

            Is the user known for posting sensitive content

        .. py:attribute:: pinned_tweets
            :type: list[str] | None

            List of id of tweets pinned by the user

        .. py:attribute:: notifications_enabled
            :type: bool

            Is new tweet notification enabled for this user

        .. py:attribute:: notifications
            :type: bool

            Is new tweet notification enabled for this user

        .. py:attribute:: community_role
            :type: str | None

            Role in Community (if applicable)



    .. py:data:: Methods:

        .. py:method:: follow()

            Follow the User

            .. py:data:: Return
                :type: User

        .. py:method:: unfollow()

            un-Follow the User

            .. py:data:: Return
                :type: User

        .. py:method:: enable_notifications()

            Enable new Tweet notification for this user

            .. py:data:: Return
                :type: bool

        .. py:method:: disable_notifications()

            Disable new Tweet notification for this user

            .. py:data:: Return
                :type: bool


Conversation
---------------------

.. py:class:: Conversation

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.inbox.Conversation`

    .. py:data:: Attributes:

        .. py:attribute:: id
            :type: int

            Id of the conversation

        .. py:attribute:: name
            :type: str

            Name of conversation

        .. py:attribute:: low_quality
            :type: bool

            Is the conversation low quality

        .. py:attribute:: muted
            :type: bool

            Is this conversation muted

        .. py:attribute:: notifications_disabled
            :type: bool

            Is the notifications for this conversation disabled

        .. py:attribute:: nsfw
            :type: bool

            Is this conversation not suitable for work

        .. py:attribute:: read_only
            :type: bool

            Is this conversation read only

        .. py:attribute:: trusted
            :type: bool

            Is this conversation trusted by the user

        .. py:attribute:: is_group
            :type: bool

            Is this conversation a Group or Not

        .. py:attribute:: type
            :type: str

            Type of conversation (`GROUP_DM`, `ONE_TO_ONE`)

        .. py:attribute:: participants
            :type: list[User]

            Participants of the conversation

        .. py:attribute:: messages
            :type: list[Message]

            Messages of the conversation

    .. py:data:: Methods:

        .. py:method:: get_all_messages(wait_time: int = 2, cursor: int = 0, till_date: datetime.datetime = None, count: int =None)
        .. py:method:: iter_all_messages(wait_time: int = 2, cursor: int = 0, till_date: datetime.datetime = None, count: int =None)

            Force get all the messages of the conversation (`iter` for Generator)

            .. py:data:: Arguments:

                .. py:data:: wait_time
                    :type: int | tuple[int, int]

                    Number of seconds to wait between multiple requests

                .. py:data:: cursor
                    :type: str

                    Cursor of that specific Page

                .. py:data:: till_date
                    :type: datetime.datetime

                    Get Messages till that date

                .. py:data:: count
                    :type: int

                    Get this number of Messages

            .. py:data:: Return
                :type: list[Message]

        .. py:method:: send_message(text)

            Send Message in this conversation

            .. py:data:: Arguments:

                .. py:data:: text
                    :type: str

                    Content of the message to send

                .. py:data:: file
                    :type: str | PathLike

                    File to send with message

            .. py:data:: Return
                :type: Message

Message
---------------------

.. py:class:: Message

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.inbox.Message`

    .. py:data:: Attributes:

        .. py:attribute:: id
            :type: int

            Id of the message

        .. py:attribute:: conversation_id
            :type: str

            Id of the conversation this message belongs to

        .. py:attribute:: epoch_time
            :type: int

            Epoch Time at which the message was sent

        .. py:attribute:: time
            :type: datetime.datetime

            Time at which the message was sent

        .. py:attribute:: request_id
            :type: str

            Request ID of the message

        .. py:attribute:: text
            :type: str

            Text of the message

        .. py:attribute:: receiver
            :type: User

            The receiver of this message

        .. py:attribute:: sender
            :type: User

            The sender of this message

        .. py:attribute:: media
            :type: Media | None

            Media in the message

NewMessage
---------------------

.. py:class:: NewMessage

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.events.newmessage.NewMessageUpdate.NewMessage`

    .. py:data:: Attributes:

        .. py:attribute:: id
            :type: int

            Id of the message

        .. py:attribute:: conversation_id
            :type: str

            Id of the conversation this message belongs to

        .. py:attribute:: time
            :type: datetime.datetime

            Time at which the message was sent

        .. py:attribute:: text
            :type: str

            Text of the message

        .. py:attribute:: participants
            :type: list[User]

            Participants of the conversation

        .. py:attribute:: receiver
            :type: User

            The receiver of this message

        .. py:attribute:: sender
            :type: User

            The sender of this message

        .. py:attribute:: media
            :type: Media | None

            Media in the message

        .. py:attribute:: message
            :type: Message

            Actual message object

        .. py:attribute:: conversation
            :type: Conversation

            Conversation object

    .. py:data:: Methods:

        .. py:method:: respond(text)

            Send Message in this conversation

            .. py:data:: Arguments:

                .. py:data:: text
                    :type: str

                    Content of the message to send

            .. py:data:: Return
                :type: Message

Community
---------------------

.. py:class:: Community

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.twDataTypes.Community`

    .. py:data:: Attributes:

        .. py:attribute:: id
            :type: int

            Id of the Community

        .. py:attribute:: created_at
            :type: datetime.datetime

            DateTime at which the Community was created

        .. py:attribute:: date
            :type: datetime.datetime

            DateTime at which the Tweet was created

        .. py:attribute:: description
            :type: str

            Bio / Description on Community

        .. py:attribute:: name
            :type: str

            Name of the Community

        .. py:attribute:: role
            :type: str

            Role of authenticated user in the community

        .. py:attribute:: member_count
            :type: int

            Number of Members in the Community

        .. py:attribute:: moderator_count
            :type: int

            Number of Moderator in the Community

        .. py:attribute:: admin
            :type: list[User]

            List of Admins of the community

        .. py:attribute:: creator
            :type: list[User]

            List of Creators of the community

        .. py:attribute:: rules
            :type: list[str]

            List of rules of the Community

Symbol
---------------------

.. py:class:: Symbol

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.twDataTypes.Symbol`

    .. py:data:: Attributes:

        .. py:attribute:: indices
            :type: list[int, int]

            The start index of this symbol in the text

        .. py:attribute:: text
            :type: str

            Actual Symbol

Hashtag
---------------------

.. py:class:: Hashtag

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.twDataTypes.Hashtag`

    .. py:data:: Attributes:

        .. py:attribute:: indices
            :type: list[int, int]

            The start index of this hashtag in the text

        .. py:attribute:: text
            :type: str

            Actual hashtag

URL
---------------------

.. py:class:: URL

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.twDataTypes.URL`

    .. py:data:: Attributes:

        .. py:attribute:: indices
            :type: list[int, int]

            The start index of this url in the text

        .. py:attribute:: display_url
            :type: str

            Twitter Short URL

        .. py:attribute:: expanded_url
            :type: str

            Actual Url


RichText
---------------------

.. py:class:: RichText

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.twDataTypes.RichText`

    .. py:data:: Attributes:

        .. py:attribute:: id
            :type: int

            Id of the Tweet

        .. py:attribute:: text
            :type: str

            Text of the tweet

        .. py:attribute:: hashtags
            :type: list[Hashtag]

            List of hashtags in the Tweet

        .. py:attribute:: urls
            :type: list[URL]

            List of URLs in the Tweet

        .. py:attribute:: symbols
            :type: list[Symbol]

             List of Symbols in the Tweet

        .. py:attribute:: user_mentions
            :type: list[ShortUser]

            List of Users mentioned in the Tweet

        .. py:attribute:: media
            :type: list[Media]

            List of Media in the Tweet

        .. py:attribute:: tags
            :type: list[RichTag]

            List of rich text tags in the text

    .. py:data:: Methods:

        .. py:method:: get_html()

            Get HTML version of the text which includes all the tags and elements

            .. py:data:: Return
                :type: str
RichTag
---------------------

.. py:class:: RichTag

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.twDataTypes.RichTag`

    .. py:data:: Attributes:

        .. py:attribute:: from_index
            :type: int

            The start index of this specific tag in the text

        .. py:attribute:: to_index
            :type: int

            The end index of this specific tag in the text

        .. py:attribute:: hashtags
            :type: list[str]

            List of hashtags in the Tweet

        .. py:attribute:: types
            :type: list[str]

            Type of tags included in the range

Pool
---------------------

.. py:class:: Pool

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.twDataTypes.Pool`

    .. py:data:: Attributes:

        .. py:attribute:: id
            :type: str

            Id of the Pool

        .. py:attribute:: name
            :type: str

            Name of the Pool

        .. py:attribute:: choices
            :type: list[Choice]

            List of choices in teh Tweet

        .. py:attribute:: end_time
            :type: datetime.datetime

            End Time of the Pool

        .. py:attribute:: last_updated_time
            :type: datetime.datetime

            Last Updated Time of the Pool

        .. py:attribute:: duration
            :type: str

            Duration of Pool in Minutes

        .. py:attribute:: user_ref
            :type: list[User]

            Users Referred in the Pool

        .. py:attribute:: selected_choice
            :type: Choice | None

            Choice already selected by the authenticated user

        .. py:attribute:: is_final
            :type: bool

            Has pool ended or not

TwList
---------------------

.. py:class:: TwList

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.twDataTypes.TwList`

    .. py:data:: Attributes:

        .. py:attribute:: id
            :type: str

            Id of the List

        .. py:attribute:: name
            :type: str

            Name of the List

        .. py:attribute:: created_at
            :type: datetime.datetime

            Time at which list was created

        .. py:attribute:: description
            :type: str

            Description of List

        .. py:attribute:: is_member
            :type: bool

            is the authenticated member of this list

        .. py:attribute:: member_count
            :type: int

            Number of member List has

        .. py:attribute:: subscriber_count
            :type: int

            Number of subscriber List has

        .. py:attribute:: admin
            :type: User

            Admin of the List

EditControl
---------------------

.. py:class:: EditControl

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.twDataTypes.EditControl`

    .. py:data:: Attributes:

        .. py:attribute:: tweet_ids
            :type: list[str]

            List of Tweet ids

        .. py:attribute:: edits_remaining
            :type: str

            Number of Edits Remaining for this Tweet

        .. py:attribute:: is_latest
            :type: bool

            is this the Latest version of Tweet

        .. py:attribute:: latest_tweet_id
            :type: str

            ID of latest edited Tweet


Broadcast
---------------------

.. py:class:: Broadcast

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.twDataTypes.Broadcast`

    .. py:data:: Attributes:

        .. py:attribute:: id
            :type: int

            ID of Broadcast

        .. py:attribute:: width
            :type: str

            Width of Broadcast

        .. py:attribute:: title
            :type: str

            Title of Broadcast

Topic
---------------------

.. py:class:: Topic

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.twDataTypes.Topic`

    .. py:data:: Attributes:

        .. py:attribute:: id
            :type: int

            ID of Topic

        .. py:attribute:: description
            :type: str

            description of topic

        .. py:attribute:: name
            :type: str

            Title of Topic

        .. py:attribute:: is_following
            :type: bool

            is authenticated user following the topic

TweetTranslate
---------------------

.. py:class:: TweetTranslate

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.twDataTypes.TweetTranslate`

    .. py:data:: Attributes:

        .. py:attribute:: id
            :type: int

            ID of Tweet

        .. py:attribute:: translation
            :type: str

            translated tweet of Tweet

        .. py:attribute:: text
            :type: str

            translated tweet of Tweet

        .. py:attribute:: source_language
            :type: str

            Source Language of Tweet

        .. py:attribute:: destination_language
            :type: str

            Tweet translated of this Language

TweetAnalytics
---------------------

.. py:class:: TweetAnalytics

    Bases : `dict`

    .. note:: **This Object is JSON Serializable**

    :reference: `tweety.types.twDataTypes.TweetAnalytics`

    .. py:data:: Attributes:

        .. py:attribute:: expands
            :type: int

            Number of Expands

        .. py:attribute:: engagements
            :type: int

            Number of Engagements

        .. py:attribute:: follows
            :type: int

            Number of Follows

        .. py:attribute:: impressions
            :type: int

            Number of Impressions

        .. py:attribute:: link_clicks
            :type: int

            Number of Clicks

        .. py:attribute:: profile_visits
            :type: int

            Number of Profile Visits

        .. py:attribute:: cost_per_follower
            :type: int

            Cost Incurred per Follower
