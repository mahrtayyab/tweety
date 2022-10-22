Filters
================

Search Filters
------------------
You can filter your search results using these filters

* **Filter Latest Tweet**
^^^^^^^^^^^^^^^^^^^

    Get the latest tweets for the keyword instead of Twitter Default Popular Tweets

    To use this filter
       *  you can pass ``latest`` directly to ``filter_`` parameter of search

       OR

       *  pass ``SearchFilters.Latest()`` method from filters module

    *Example:*

    .. code-block:: python

        from tweety.bot import Twitter
        from tweety.filters import SearchFilters
        app = Twitter()

        all_searches = app.search("Pakistan",filter_='latest')

        # Or you can use the filter module
        all_searches = app.search("Pakistan",filter_=SearchFilters.Latest())

* **Filter Users**
^^^^^^^^^^^^^^^^^^^

    Search only Users with corresponding keyword

    To use this filter
       *  you can pass ``users`` directly to ``filter_`` parameter of search

       OR

       *  pass ``SearchFilters.Users()`` method from filters module

    *Example:*

    .. code-block:: python

        from tweety.bot import Twitter
        from tweety.filters import SearchFilters
        app = Twitter()

        all_searches = app.search("Pakistan",filter_='users')

        # Or you can use the filter module
        all_searches = app.search("Pakistan",filter_=SearchFilters.Users())

* **Filter Only Photos**
^^^^^^^^^^^^^^^^^^^

    Get the latest tweets for the keyword instead of Twitter Default Popular Tweets

    To use this filter
       *  you can pass ``photos`` directly to ``filter_`` parameter of search

       OR

       *  pass ``SearchFilters.Photos()`` method from filters module

    *Example:*

    .. code-block:: python

        from tweety.bot import Twitter
        from tweety.filters import SearchFilters
        app = Twitter()

        all_searches = app.search("Pakistan",filter_='photos')

        # Or you can use the filter module
        all_searches = app.search("Pakistan",filter_=SearchFilters.Photos())

* **Filter Only Videos**
^^^^^^^^^^^^^^^^^^^

    Get the latest tweets for the keyword instead of Twitter Default Popular Tweets

    To use this filter
       *  you can pass ``videos`` directly to ``filter_`` parameter of search

       OR

       *  pass ``SearchFilters.Videos()`` method from filters module

    *Example:*

    .. code-block:: python

        from tweety.bot import Twitter
        from tweety.filters import SearchFilters
        app = Twitter()

        all_searches = app.search("Pakistan",filter_='videos')

        # Or you can use the filter module
        all_searches = app.search("Pakistan",filter_=SearchFilters.Videos())