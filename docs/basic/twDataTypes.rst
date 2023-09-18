.. _twDataTypes:

=============
TwDataTypes
=============

This page contains all the Data Class returned by the different methods


UserTweets
---------------------

.. py:class:: UserTweets

    Bases : `BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.usertweet.UserTweets`

    .. py:data:: Attributes:

        .. py:attribute:: tweets
            :type: list[Tweet | SelfThread]

            List of User Tweets

        .. py:attribute:: get_replies
            :type: bool

            Either to get replies or Not

        .. py:attribute:: cursor
            :type: str

            Cursor for next page

        .. py:attribute:: is_next_page
            :type: bool

            Is next page of tweets available

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

        .. py:method:: get_next_page()

            Get next page of tweets if available

            .. py:data:: Return
                :type: list[Tweet | SelfThread]


        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :return: ``UserTweets(user={username}, count={number_of_results})``


Search
---------------------
Reference `Search`_.


.. py:class:: Search

    Bases : `BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.search.Search`

    .. py:data:: Attributes:

        .. py:attribute:: tweets
            :type: list[Tweet]

            List of User Tweets if filter isn't User Only

        .. py:attribute:: users
            :type: list

            List of User Tweets if filter is User Only

        .. py:attribute:: keyword
            :type: str

            keyword which is begin searched

        .. py:attribute:: cursor
            :type: str

            Cursor for next page

        .. py:attribute:: is_next_page
            :type: bool

            Is next page of tweets available

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

        .. py:method:: get_next_page()

            Get next page of tweets if available

            .. py:data:: Return
                :type: list[Tweet]


        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :value: ``Search(keyword={keyword}, count={number_of_results}, filter={any_filter_which_is_used})``

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


        .. py:attribute:: cursor
            :type: str

            Cursor for next page

        .. py:attribute:: is_next_page
            :type: bool

            Is next page of tweets available

        .. py:attribute:: user_id
            :type: int

            User ID of the user in question

    .. py:data:: Methods:

        .. py:method:: get_next_page()

            Get next page of tweets if available

            .. py:data:: Return
                :type: list[Tweet]


        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :return: ``TweetLikes(tweet_id={id_of_tweet}, count={number_of_results})``

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


        .. py:attribute:: cursor
            :type: str

            Cursor for next page

        .. py:attribute:: is_next_page
            :type: bool

            Is next page of tweets available

        .. py:attribute:: user_id
            :type: int

            User ID of the user in question

    .. py:data:: Methods:

        .. py:method:: get_next_page()

            Get next page of tweets if available

            .. py:data:: Return
                :type: list[Tweet]


        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :return: ``TweetRetweets(tweet_id={id_of_tweet}, count={number_of_results})``

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

        .. py:attribute:: cursor
            :type: str

            Cursor for next page

        .. py:attribute:: is_next_page
            :type: bool

            Is next page of tweets available

        .. py:attribute:: user_id
            :type: int

            User ID of the user in question

    .. py:data:: Methods:

        .. py:method:: get_next_page()

            Get next page of tweets if available

            .. py:data:: Return
                :type: list[Tweet]


        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :return: ``Mention(user_id={user_id}, count={number_of_results})``


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

        .. py:attribute:: cursor
            :type: str

            Cursor for next page

        .. py:attribute:: is_next_page
            :type: bool

            Is next page of tweets available

        .. py:attribute:: user_id
            :type: int

            User ID of the user in question

    .. py:data:: Methods:

        .. py:method:: get_next_page()

            Get next page of tweets if available

            .. py:data:: Return
                :type: list[Tweet]


        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :return: ``Bookmarks(user_id={user_id}, count={number_of_results})``

CommunityTweets
---------------------

.. py:class:: CommunityTweets

    Bases : `BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.community.CommunityTweets`

    .. py:data:: Attributes:

        .. py:attribute:: tweets
            :type: list[Tweet]

            List of  Tweets

        .. py:attribute:: cursor
            :type: str

            Cursor for next page

        .. py:attribute:: is_next_page
            :type: bool

            Is next page of tweets available

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

        .. py:method:: get_next_page()

            Get next page of tweets if available

            .. py:data:: Return
                :type: list[Tweet]


        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :value: ``CommunityTweets(id={id_of_community}, count={number_of_results})``

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

        .. py:attribute:: cursor
            :type: str

            Cursor for next page

        .. py:attribute:: is_next_page
            :type: bool

            Is next page of tweets available

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

        .. py:method:: get_next_page()

            Get next page of tweets if available

            .. py:data:: Return
                :type: list[Tweet]


        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :value: ``CommunityMembers(id={id_of_community}, count={number_of_results})``

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

        .. py:attribute:: cursor
            :type: str

            Cursor for next page

        .. py:attribute:: is_next_page
            :type: bool

            Is next page of tweets available

    .. py:data:: Methods:

        .. py:method:: get_next_page()

            Get next page of tweets if available

            .. py:data:: Return
                :type: list[Tweet]


        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :value: ``TweetNotifications(user_id={id_of_user}, count={number_of_results})``

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


        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :return: ``Inbox(user_id={user_id}, count={number_of_results})``


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

        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :return: ``SelfThread(tweets=number_of_tweets_in_threads)``

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

        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :return: ``ConversationThread(tweets=number_of_tweets_in_threads)``


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
            :type: list[str]

            URLs mentioned in the Tweet

        .. py:attribute:: hashtags
            :type: list[str]

            Hashtags mentioned in the Tweet

        .. py:attribute:: symbols
            :type: list[str]

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

        .. py:method:: iter_comments(pages=1, wait_time=2, cursor=None)

            Generator method to get the comments / replies posted in response to this tweet

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
                :type:  Generator : (`Tweet` , list[`Tweet`])

        .. py:method:: like()

            Like the Tweet

            .. py:data:: Return
                :type: Bool

        .. py:method:: retweet()

            Retweet the Tweet

            .. py:data:: Return
                :type: Bool

        .. py:method:: get_reply_to()

            Get the Tweet to which this Tweet was sent in reply

            .. py:data:: Return
                :type: Tweet

        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :value: ``Tweet(id=id_of_tweet, author=author_of_tweet, created_on=tweet_creation_date, threads=number_of_threads)``

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

            Type of Media (`video` | `image`)

        .. py:attribute:: url
            :type: str

            Short URL of Tweet

        .. py:attribute:: streams
            :type: list[Stream]

            List of streams available if the `type` is `video`

        .. py:attribute:: mediaStats
            :type: dict

            Stats of the media , usually `viewCount`

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

        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :value: ``Media(id=id_of_media, type=type_of_media)``


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

        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :value: ``Stream(content_type=content_type_of_stream, length=length_of_stream_in_millis, bitrate=bitrate_of_media_audio, res=resolution_of_media)``

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

    .. py:data:: Methods:

        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :value: ``ShortUser(id=id_of_the_user, name=name_of_the_user)``

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

    .. py:data:: Methods:

        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :value: ``Trends(name=name_of_the_trend)``

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

    .. py:data:: Methods:

        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :value: ``Card(id=rest_id_of_card, choices=list_of_choices, end_time=end_time_of_card, duration=duration_of_card)``


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

    .. py:data:: Methods:

        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :value: ``Choice(name=name_of_choice, value=value_of_choice, counts=number_of_votes_this_choice_has)``

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

    .. py:data:: Methods:

        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :value: ``Place(id=id_of_place, name=name_of_place, country=country_of_place, coordinates=coordinates_of_place)``


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

    .. py:data:: Methods:

        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :value: ``Coordinates(latitude=latitude, longitude=longitude)``

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

        .. py:attribute:: entities
            :type: dict

            Additional entities of user , usually links

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
            :type: str

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
            :type: bool | None

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
            :type: list[str]

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


        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :value: ``User(id=rest_id_of_user, name=name_of_the_user, username=username_of_the_user, followers=number_of_followers_of_user, verified=is_user_verified)``


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

        .. py:method:: get_all_messages()

            Force get all the messages of the conversation

            .. py:data:: Return
                :type: list[Message]

        .. py:method:: send_message(text)

            Send Message in this conversation

            .. py:data:: Arguments:

                .. py:data:: text
                    :type: str

                    Content of the message to send

            .. py:data:: Return
                :type: Message

        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :value: ``Conversation(id=id_of_conversation, muted=is muted, nsfw=is nsfw, participants=number of participants)``

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

    .. py:data:: Methods:

        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :value: ``Message(id=id_of_the_message, conversation_id=id_of_the_conversation, time=time_of_the_message)``

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

        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :value: ``Message(id=id_of_the_message, conversation_id=id_of_the_conversation, time=time_of_the_message)``

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


    .. py:data:: Methods:

        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :value: ``Community(id={rest_id_of_user}, name={name_of_the_user}, role={role_of_user}, admin={admin_of_the_community})``

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
            :type: list[str]

            List of hashtags in the Tweet

        .. py:attribute:: urls
            :type: list[str]

            List of URLs in the Tweet

        .. py:attribute:: symbols
            :type: list[str]

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

        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :value: ``RichText(id={rest_id_of_tweet})``

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

    .. py:data:: Methods:

        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :value: ``RichTag(from_index={from_index}, to_index={to_index}, types={types})``

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

    .. py:data:: Methods:

        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :value: ``Card(id={rest_id_of_poll}, choices={list_of_choices}, end_time={end_time_of_pool}, duration={duration_of_pool} minutes)``
