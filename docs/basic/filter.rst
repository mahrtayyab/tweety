.. _filter:

===============
Search Filters
===============

You can filter the `Search` function using these methods


Filter Latest Tweets
---------------------

.. py:class:: SearchFilters.Latest()

    :reference: `tweety.filters.SearchFilters.Latest`

    .. code-block:: python

        from tweety.filters import SearchFilters

        # Assuming `app` is Twitter Client Object

        app.search("#pakistan", filter_=SearchFilters.Latest())
        from tweet in tweets:
            print(tweet)

Filter Only Media Tweets
---------------------------

.. py:class:: SearchFilters.Media()

    :reference: `tweety.filters.SearchFilters.Media`

    .. code-block:: python

        from tweety.filters import SearchFilters

        # Assuming `app` is Twitter Client Object

        app.search("#pakistan", filter_=SearchFilters.Media())
        from tweet in tweets:
            print(tweet.media)


Filter Only Users
---------------------

.. py:class:: SearchFilters.Users()

    :reference: `tweety.filters.SearchFilters.Users`

    .. code-block:: python

        from tweety.filters import SearchFilters

        # Assuming `app` is Twitter Client Object

        app.search("#pakistan", filter_=SearchFilters.Users())
        from user in users:
            print(user)



===============
Tweet Audience Filter
===============

You can filter the created Tweet Comment Audience function using these methods


Filter Only People You Mention
--------------------------------

.. py:class:: TweetConversationFilters.PeopleYouMention()

    :reference: `tweety.filters.TweetConversationFilters.PeopleYouMention`

    .. code-block:: python

        from tweety.filters import TweetConversationFilters

        # Assuming `app` is Twitter Client Object

        app.create_tweet("Hi", filter_=TweetConversationFilters.PeopleYouMention())


Filter Only People You Follow
--------------------------------

.. py:class:: TweetConversationFilters.PeopleYouFollow()

    :reference: `tweety.filters.TweetConversationFilters.PeopleYouFollow`

    .. code-block:: python

        from tweety.filters import TweetConversationFilters

        # Assuming `app` is Twitter Client Object

        app.create_tweet("Hi", filter_=TweetConversationFilters.PeopleYouFollow())


===============
Language
===============

You can translate Tweet in different Language , get Language code from here.

    .. py:data:: Urdu
        :value: "ur"

    .. py:data:: URDU
        :value: "ur"

    .. py:data:: Russian
        :value: "ru"

    .. py:data:: RUSSIAN
        :value: "ru"

    .. py:data:: Danish
        :value: "da"

    .. py:data:: DANISH
        :value: "da"

    .. py:data:: Filipino
        :value: "fil"

    .. py:data:: FILIPINO
        :value: "fil"

    .. py:data:: Irish
        :value: "ga"

    .. py:data:: IRISH
        :value: "ga"

    .. py:data:: TraditionalChinese
        :value: "zh-tw"

    .. py:data:: TRADITIONAL_CHINESE
        :value: "zh-tw"

    .. py:data:: Hungarian
        :value: "hu"

    .. py:data:: HUNGARIAN
        :value: "hu"

    .. py:data:: Spanish
        :value: "es"

    .. py:data:: SPANISH
        :value: "es"

    .. py:data:: Arabic_Feminine
        :value: "ar-x-fm"

    .. py:data:: ARABIC_FEMININE
        :value: "ar-x-fm"

    .. py:data:: Croatian
        :value: "hr"

    .. py:data:: CROATIAN
        :value: "hr"

    .. py:data:: French
        :value: "fr"

    .. py:data:: FRENCH
        :value: "fr"

    .. py:data:: Kannada
        :value: "kn"

    .. py:data:: KANNADA
        :value: "kn"

    .. py:data:: Italian
        :value: "it"

    .. py:data:: ITALIAN
        :value: "it"

    .. py:data:: Marathi
        :value: "mr"

    .. py:data:: MARATHI
        :value: "mr"

    .. py:data:: Japanese
        :value: "ja"

    .. py:data:: JAPANESE
        :value: "ja"

    .. py:data:: Indonesian
        :value: "id"

    .. py:data:: INDONESIAN
        :value: "id"

    .. py:data:: Gujarati
        :value: "gu"

    .. py:data:: GUJARATI
        :value: "gu"

    .. py:data:: Romanian
        :value: "ro"

    .. py:data:: ROMANIAN
        :value: "ro"

    .. py:data:: Turkish
        :value: "tr"

    .. py:data:: TURKISH
        :value: "tr"

    .. py:data:: Basque
        :value: "eu"

    .. py:data:: BASQUE
        :value: "eu"

    .. py:data:: Swedish
        :value: "sv"

    .. py:data:: SWEDISH
        :value: "sv"

    .. py:data:: Tamil
        :value: "ta"

    .. py:data:: TAMIL
        :value: "ta"

    .. py:data:: Thai
        :value: "th"

    .. py:data:: THAI
        :value: "th"

    .. py:data:: Ukrainian
        :value: "uk"

    .. py:data:: UKRAINIAN
        :value: "uk"

    .. py:data:: Bangla
        :value: "bn"

    .. py:data:: BANGLA
        :value: "bn"

    .. py:data:: German
        :value: "de"

    .. py:data:: GERMAN
        :value: "de"

    .. py:data:: Vietnamese
        :value: "vi"

    .. py:data:: VIETNAMESE
        :value: "vi"

    .. py:data:: Catalan
        :value: "ca"

    .. py:data:: CATALAN
        :value: "ca"

    .. py:data:: Arabic
        :value: "ar"

    .. py:data:: ARABIC
        :value: "ar"

    .. py:data:: Dutch
        :value: "nl"

    .. py:data:: DUTCH
        :value: "nl"

    .. py:data:: SimplifiedChinese
        :value: "zh-cn"

    .. py:data:: SIMPLIFIED_CHINESE
        :value: "zh-cn"

    .. py:data:: Slovak
        :value: "sk"

    .. py:data:: SLOVAK
        :value: "sk"

    .. py:data:: Czech
        :value: "cs"

    .. py:data:: CZECH
        :value: "cs"

    .. py:data:: Greek
        :value: "el"

    .. py:data:: GREEK
        :value: "el"

    .. py:data:: Finnish
        :value: "fi"

    .. py:data:: FINNISH
        :value: "fi"

    .. py:data:: English
        :value: "en"

    .. py:data:: ENGLISH
        :value: "en"

    .. py:data:: Norwegian
        :value: "no"

    .. py:data:: NORWEGIAN
        :value: "no"

    .. py:data:: Polish
        :value: "pl"

    .. py:data:: POLISH
        :value: "pl"

    .. py:data:: Portuguese
        :value: "pt"

    .. py:data:: PORTUGUESE
        :value: "pt"

    .. py:data:: Persian
        :value: "fa"

    .. py:data:: PERSIAN
        :value: "fa"

    .. py:data:: Galician
        :value: "gl"

    .. py:data:: GALICIAN
        :value: "gl"

    .. py:data:: Korean
        :value: "ko"

    .. py:data:: KOREAN
        :value: "ko"

    .. py:data:: Serbian
        :value: "sr"

    .. py:data:: SERBIAN
        :value: "sr"

    .. py:data:: BritishEnglish
        :value: "en-gb"

    .. py:data:: BRITISH_ENGLISH
        :value: "en-gb"

    .. py:data:: Hindi
        :value: "hi"

    .. py:data:: HINDI
        :value: "hi"

    .. py:data:: Hebrew
        :value: "he"

    .. py:data:: HEBREW
        :value: "he"

    .. py:data:: Malay
        :value: "msa"

    .. py:data:: MALAY
        :value: "msa"

    .. py:data:: Bulgarian
        :value: "bg"

    .. py:data:: BULGARIAN
        :value: "bg"

    .. code-block:: python

        from tweety.filters import Language

        # Assuming `app` is Twitter Client Object

        app.translate_tweet("1234", filter_=Language.English)
