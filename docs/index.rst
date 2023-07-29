========================
Tweety's Documentation
========================

.. code-block:: python

   from tweety import Twitter

   app = Twitter("session")
   app.sign_in(username, password)

   all_tweets = app.get_tweets("elonmusk")
   for tweet in all_tweets:
       print(tweet)


* Are you new here? Jump straight into :ref:`installation`!
* Looking for All Available Functions? See :ref:`all-functions`.
* Did you upgrade the library? Please read :ref:`changelog`.


What is this?
-------------

Twitter is a popular social media platform used by millions of people
even the Governments too. This library is meant to scrape the Tweets,
Users , Trends and Search Results from Twitter.

How should I use the documentation?
-----------------------------------

If you are getting started with the library, you should follow the
documentation in order by pressing the "Next" button at the bottom-right
of every page.

You can also use the menu on the left to quickly skip over sections.

.. toctree::
    :hidden:
    :caption: Get Started

    basic/installation
    basic/quick-start

.. toctree::
    :hidden:
    :caption: Base Class

    basic/twitter-class


.. toctree::
    :hidden:
    :caption: References

    basic/singing-in
    basic/all-functions
    basic/twDataTypes
    basic/exceptions
    basic/events

.. toctree::
    :hidden:
    :caption: Filters

    basic/filter

.. toctree::
    :hidden:
    :caption: Miscellaneous

    misc/changelog
