twDataTypes
================

.. _user_tweets_section:

UserTweets
----------------

``This Object is Iterable and JSON Serializable``

All Tweets included are of type `Tweet <#tweet-section>`_

* Representation:
^^^^^^^^^^^^^^^^^^^

    .. code-block::

       UserTweets(user=username, count=number_of_results)

* Methods:
^^^^^^^^^^

    - get_next_page()

        Use this method to get next of the instance user tweets , it returns the list of Tweet Objects


    - to_xlsx()

        Use this method to convert the resultant tweets to an Excel Sheet , returns Excel Object

        * Optional Parameters:
            :filename: (`str`) Filename of the output file

    - to_dict()

        Get the list of all the tweets

        .. warning::
            This Method is depreciated and will be removed in future, as the object is already JSON serializable


* Attributes:
^^^^^^^^^^^^^

.. list-table::
   :widths: 25 25 60
   :header-rows: 1

   * - Name
     - Type
     - Description

   * - tweets
     - list
     - All the tweets of the user

   * - cursor
     - str
     - Cursor of next page

   * - is_next_page
     - boolean
     - Is next page of tweets available for this user

   * - user_id
     - str
     - Rest User ID of the user in question


Search
----------------

``This Object is Iterable and JSON Serializable``

All Tweets included are of type `Tweet <#tweet-section>`_


* Representation:
^^^^^^^^^^^^^^^^^^^

    .. code-block::

       Search(keyword=keyword, count=number_of_results, filter=filter)

* Methods:
^^^^^^^^^^

    - get_next_page()

        Use this method to get next of the instance user tweets , it returns the list of Tweet Objects


    - to_xlsx()

        Use this method to convert the resultant tweets to an Excel Sheet , returns Excel Object

        .. note::
            This Method isn't available with 'users' filter

        * Optional Parameters:
            :filename: (`str`) Filename of the output file

    - to_dict()

        Get the list of all the tweets

        .. warning::
            This Method is depreciated and will be removed in future, as the object is already JSON serializable


* Attributes:
^^^^^^^^^^^^^

.. list-table::
   :widths: 25 25 60
   :header-rows: 1

   * - Name
     - Type
     - Description

   * - keyword
     - str
     - Keyword which is begin searched

   * - tweets
     - list
     - All the tweets of the search

   * - cursor
     - str
     - Cursor of next page

   * - is_next_page
     - boolean
     - Is next page of tweets available for this search

   * - filter
     - str | None
     - Filter applied to search

.. _tweet_section:

Tweet
----------------

``This Object JSON Serializable``

* Representation:
^^^^^^^^^^^^^^^^^^^

    .. code-block::

       Tweet(id=id_of_tweet, author=author_of_tweet, created_on=tweet_creation_date, threads=number_of_threads)

* Methods:
^^^^^^^^^^

    - to_dict()

        Get the formatted dict object

        .. warning::
            This Method is depreciated and will be removed in future, as the object is already JSON serializable


* Attributes:
^^^^^^^^^^^^^

.. list-table::
   :widths: 25 25 60
   :header-rows: 1

   * - Name
     - Type
     - Description

   * - created_on
     - datetime.datetime
     - Time and Date at which the tweet was created

   * - author
     - `User <#user-userlegacy-section>`_
     - Author of the Tweet

   * - is_retweet
     - boolean
     - Is it a retweeted tweet

   * - is_reply
     - boolean
     - Is this tweet was sent in reply to any other tweet

   * - id
     - str
     - Rest ID of the Tweet

   * - tweet_body | text
     - str
     - Text of the Tweet

   * - language
     - str
     - Language of the Tweet

   * - likes
     - int
     - Number of the Likes on Tweet

   * - card
     - `Card <#card-section>`_
     - Card in the Tweet

   * - place
     - `Place <#place-section>`_
     - Place mentioned in the Tweet

   * - retweet_counts
     - int
     - Number of retweets this Tweet has

   * - source
     - str
     - Source from which platform this tweet was created

   * - media
     - list [`Media <#media-section>`_]
     - Medias in the Tweet

   * - user_mentions
     - list [`ShortUser <#short-user-section>`_]
     - Medias in the Tweet

   * - urls
     - list
     - All the URLs mentioned in the Tweet

   * - hashtags
     - list
     - All the Hashtags mentioned in the Tweet

   * - symbols
     - list
     - All the Symbols mentioned in the Tweet

   * - reply_to
     - str | None
     - Username of the user whom the tweet was sent as reply if ``is_reply`` is ``True``

   * - threads
     - list [`Tweet <#tweet-section>`_]
     - Tweets included as the threads

   * - comments
     - list [`Tweet <#tweet-section>`_]
     - Tweets sent in reply to this Tweet


.. _media_section:

Media
----------------

``This Object JSON Serializable``

* Representation:
^^^^^^^^^^^^^^^^^^^

    .. code-block::

       Media(id=id_of_the_media, type=type_of_the_media)

* Methods:
^^^^^^^^^^

    - download()
        Download the best quality media available directly to the Disk

        .. note::
            For this method to work , you need ``wget`` to be installed in the system

        * Required Parameters:
            :filename: (`str`) Filename of the output file

        * Optional Parameters:
            :show_progress: (`boolean`) Either print the download progress or not

    - to_dict()

        Get the original raw response dict object

        .. warning::
            This Method is depreciated and will be removed in future, as the object is already JSON serializable


* Attributes:
^^^^^^^^^^^^^

.. list-table::
   :widths: 25 25 60
   :header-rows: 1

   * - Name
     - Type
     - Description

   * - indices
     - list
     - Indices of the Media

   * - media_url_https
     - str
     - True Media direct url

   * - type
     - str [`video`, `photo`, 'animated_gif']
     - Type of the Media

   * - features
     - list
     - Features of the Media

   * - id
     - str
     - Rest ID of the Tweet

   * - media_key
     - str
     - Internal Twitter Media Key

   * - mediaStats
     - json | dict
     - Language of the Tweet

   * - sizes
     - json | dict
     - All sizes of the media available on Twitter

   * - original_info
     - json | dict
     - Original Info about the media dimensions

   * - streams
     - list [`Stream <#stream-section>`_]
     - List of all the stream (videos) available if the ``type`` is ``video``

   * - display_url
     - str
     - Display URL of the Media

   * - expanded_url
     - str
     - Expanded URL of the Media

.. _stream_section:

Stream
----------------

``This Object JSON Serializable``

* Representation:
^^^^^^^^^^^^^^^^^^^

    .. code-block::

       Stream(content_type=content_type_of_stream, length=length_of_stream_in_millis, bitrate=bitrate_of_media_audio, res=resolution_of_media)

* Methods:
^^^^^^^^^^

    - download()
        Download the best quality media available directly to the Disk

        .. note::
            For this method to work , you need ``wget`` to be installed in the system

        * Optional Parameters:
            :filename: (`str`) Filename of the output file
            :show_progress: (`boolean`) Either print the download progress or not

    - to_dict()

        Get the original raw response dict object

        .. warning::
            This Method is depreciated and will be removed in future, as the object is already JSON serializable


* Attributes:
^^^^^^^^^^^^^

.. list-table::
   :widths: 25 25 60
   :header-rows: 1

   * - Name
     - Type
     - Description

   * - bitrate
     - int
     - Bitrate of the Stream's Audio

   * - content_type
     - str
     - Content Type of the Stream

   * - url
     - str
     - Stream direct URL

   * - length
     - int
     - Length of the Stream in milliseconds

   * - aspect_ratio
     - list [int]
     - Aspect Ratio of the Stream


.. _short_user_section:

ShortUser
----------------

``This Object JSON Serializable``

* Representation:
^^^^^^^^^^^^^^^^^^^

    .. code-block::

       ShortUser(id=id_of_the_user, name=name_of_the_user)

* Methods:
^^^^^^^^^^

    - to_dict()

        Get the original raw response dict object

        .. warning::
            This Method is depreciated and will be removed in future, as the object is already JSON serializable


* Attributes:
^^^^^^^^^^^^^

.. list-table::
   :widths: 25 25 60
   :header-rows: 1

   * - Name
     - Type
     - Description

   * - id
     - str
     - Rest ID of the user

   * - name
     - str
     - Name of the User

   * - screen_name
     - str
     - Username of the user

.. _user_userlegacy_section:

User / UserLegacy
----------------

``This Object JSON Serializable``

* Representation:
^^^^^^^^^^^^^^^^^^^

    .. code-block::

       User(id=rest_id_of_user, name=name_of_the_user, screen_name=username_of_the_user, followers=number_of_followers_of_user, verified=is_user_verified)

* Methods:
^^^^^^^^^^

    - to_dict()

        Get the original raw response dict object

        .. warning::
            This Method is depreciated and will be removed in future, as the object is already JSON serializable


* Attributes:
^^^^^^^^^^^^^

.. list-table::
   :widths: 25 25 60
   :header-rows: 1

   * - Name
     - Type
     - Description

   * - id
     - str
     - AlphaNumeric ID of the user

   * - rest_id
     - str
     - Rest ID of the user

   * - created_at
     - datetime.datetime
     - Date and Time at which the user was created

   * - name
     - str
     - Name of the User

   * - screen_name
     - str
     - Username of the user

   * - entities
     - json | dict
     - Entities of the user

   * - fast_followers_count
     - int
     - Fast Followers Count of the user

   * - favourites_count
     - int
     - Number of followings of the user

   * - followers_count
     - int
     - Number of followers of the user

   * - friends_count
     - int
     - Number of Friends of the user

   * - listed_count
     - int
     - Number of List created by user

   * - location
     - str
     - Location of the user

   * - media_count
     - int
     - Number of Media this user has shared

   * - protected
     - boolean
     - User has private profile or Not

   * - verified
     - boolean
     - Is the user verified or Not

   * - profile_url
     - str
     - Profile URL of the User

.. _trends_section:

Trends
----------------

* Representation:
^^^^^^^^^^^^^^^^^^^

    .. code-block::

       Trends(name=name_of_the_trend)

* Methods:
^^^^^^^^^^

    - to_dict()

        Get the original raw response dict object


* Attributes:
^^^^^^^^^^^^^

.. list-table::
   :widths: 25 25 60
   :header-rows: 1

   * - Name
     - Type
     - Description

   * - url
     - str
     - URL of the Trend

   * - name
     - str
     - Name of the Trend

   * - tweet_count
     - str
     - Number of Tweet this Trend has

.. _card_section:

Card (Usually Poll)
----------------

``This Object JSON Serializable``

* Representation:
^^^^^^^^^^^^^^^^^^^

    .. code-block::

       Card(id=rest_id_of_card, choices=list_of_choices, end_time=end_time_of_card, duration=duration_of_card)

* Methods:
^^^^^^^^^^


* Attributes:
^^^^^^^^^^^^^

.. list-table::
   :widths: 25 25 60
   :header-rows: 1

   * - Name
     - Type
     - Description

   * - rest_id
     - str
     - Rest ID of the Card

   * - name
     - str
     - Name of the Card

   * - choices
     - list [`Choice <#choice-section>`_]
     - List of Choices in the Card/Poll

   * - end_time
     - datetime.datetime
     - End Time of the Poll

   * - last_updated_time
     - datetime.datetime
     - Last Date and Time at which the Card/Poll was updated

   * - duration
     - str
     - Duration of the Poll in minutes

   * - user_ref
     - list [`User <#user-userlegacy-section>`_]
     - List of Users referred in the Card/Poll


.. _choice_section:

Choice
----------------

``This Object JSON Serializable``

* Representation:
^^^^^^^^^^^^^^^^^^^

    .. code-block::

       Choice(name=name_of_choice, value=value_of_choice, counts=number_of_votes_this_choice_has)

* Methods:
^^^^^^^^^^


* Attributes:
^^^^^^^^^^^^^

.. list-table::
   :widths: 25 25 60
   :header-rows: 1

   * - Name
     - Type
     - Description

   * - value
     - str
     - Value of the Choice

   * - name
     - str
     - Name of the Choice

   * - type
     - str
     - Type of the Value

   * - counts
     - str
     - Number of the Votes this Choice has

.. _place_section:

Place
----------------

``This Object JSON Serializable``

* Representation:
^^^^^^^^^^^^^^^^^^^

    .. code-block::

       Place(id=id_of_place, name=name_of_place, country=country_of_place, coordinates=coordinates_of_place)

* Methods:
^^^^^^^^^^


* Attributes:
^^^^^^^^^^^^^

.. list-table::
   :widths: 25 25 60
   :header-rows: 1

   * - Name
     - Type
     - Description

   * - id
     - str
     - ID of the Place

   * - country
     - str
     - Country of the Place

   * - country_code
     - str
     - Country Code of the Place

   * - full_name
     - str
     - Full Name of the Place

   * - name
     - str
     - Name of the Place

   * - url
     - str
     - URL of the Place

   * - coordinates
     - list [`Coordinates <#coordinates-section>`_]
     - Coordinates of the Place

.. _coordinates_section:

Coordinates
----------------

``This Object JSON Serializable``

* Representation:
^^^^^^^^^^^^^^^^^^^

    .. code-block::

       Coordinates(latitude=latitude, longitude=longitude)

* Methods:
^^^^^^^^^^


* Attributes:
^^^^^^^^^^^^^

.. list-table::
   :widths: 25 25 60
   :header-rows: 1

   * - Name
     - Type
     - Description

   * - latitude
     - float
     - Latitude of the Coordinates

   * - longitude
     - float
     - Longitude of the Coordinates



