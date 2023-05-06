.. _twDataTypes:

=============
TwDataTypes
=============

This page contains all the Data Class returned by the different methods


UserTweets
---------------------

.. py:class:: UserTweets

    Bases : `dict`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.usertweet.UserTweets`

    .. py:data:: Attributes:

        .. py:attribute:: tweets
            :type: list

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
                :type: list[Tweet]


        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :return: ``UserTweets(user={username}, count={number_of_results})``


Search
---------------------
Reference `Search`_.


.. py:class:: Search

    Bases : `dict`

    .. note:: **This Object is JSON Serializable and Iterable**

    :reference: `tweety.types.search.Search`

    .. py:data:: Attributes:

        .. py:attribute:: tweets
            :type: list

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

        .. py:attribute:: threads
            :type: list[Tweet]

            List of Threaded Tweets

        .. py:attribute:: comments
            :type: list[Tweet]

            List of Comments sent in response to this Tweet

    .. py:data:: Methods:

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

        .. py:method:: download(filename=None, show_progress=True)

            Download the Media

            .. py:data:: Arguments:

                .. py:data:: filename (optional)
                    :type: str
                    :value: None

                    Filename of the Media

                .. py:data:: show_progress (optional)
                    :type: bool
                    :value: True

                    Either to show the download progress or not

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

        .. py:method:: download(filename=None, show_progress=True)

            Download the Media

            .. py:data:: Arguments:

                .. py:data:: filename (optional)
                    :type: str
                    :value: None

                    Filename of the Media

                .. py:data:: show_progress (optional)
                    :type: bool
                    :value: True

                    Either to show the download progress or not

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

        .. py:attribute:: name
            :type: str

            Name of the choice

        .. py:attribute:: value
            :type: str

            Value of the choice

        .. py:attribute:: type
            :type: str

            Type of the choice `value`

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

    .. py:data:: Methods:

        .. py:method:: __repr__()

            Developer Representation of the Object

            .. py:data:: Return
                :type: str

                :value: ``User(id=rest_id_of_user, name=name_of_the_user, username=username_of_the_user, followers=number_of_followers_of_user, verified=is_user_verified)``

