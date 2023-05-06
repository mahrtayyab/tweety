
.. _twitter-class:

=============
Twitter Class
=============


.. py:class:: Twitter(max_retires: int = 10, proxy: Union[dict, Proxy] = None, cookies: Union[str, dict] = None)

    This is main entry Class for the library you should be importing and using to make further method calls

    .. note:: if `cookies` are provided all requests made to Twitter while be using that cookies.

    .. py:data:: Arguments

        .. py:data:: max_retires (optional)
            :type: int
            :value: 10

            The number of times you want to retry in case the ``Guest Token`` couldn't be obtained

        .. py:data:: proxy (optional)
            :type: dict | Proxy
            :value: None

            Proxy you want to use

            .. warning:: Proxy is not yet fully integrated

        .. py:data:: cookies (optional)
            :type: str | dict
            :value: None

            Cookies you want to use when making the requests to Twitter (as authenticated user)

            .. attention:: Some functions requires user authentication and will not work without it


    .. py:data:: Methods:

        All Methods are Here :ref:`all-functions`!

.. code-block:: python

    from tweety.bot import Twitter
    app = Twitter()


