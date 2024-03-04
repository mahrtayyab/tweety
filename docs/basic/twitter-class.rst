
.. _twitter-class:

=============
Twitter Class
=============

The Twitter aggregates several mixin classes to provide all the common functionality in a nice, Pythonic interface. Each mixin has its own methods, which you all can use.

.. py:class:: Twitter(session_name: Union[str, Session], proxy: Union[dict, Proxy] = None)


    Bases : `UpdateMethods` , `BotMethods`, `AuthMethods`, `UserMethods`

    .. py:data:: Arguments

        .. py:data:: session_name
            :type: str | Session

            This is the name of the session which will be saved and can be loaded later

        .. py:data:: proxy (optional)
            :type: dict | Proxy
            :value: None

            Proxy you want to use

    .. py:data:: Methods:

        All Methods are Here :ref:`all-functions`!


=======================
BaseGeneratorClass
=======================
.. py:class:: BaseGeneratorClass

    Bases : `dict`

    :reference: `tweety.types.base.BaseGeneratorClass`

    .. note:: **This Object is JSON Serializable and Iterable**

    This is the Base Class for All Generator Classes

    .. py:data:: Attributes:

        .. py:attribute:: cursor
            :type: str

            Cursor for next page

        .. py:attribute:: is_next_page
            :type: bool

            Is next page of tweets available

        .. py:attribute:: cursor_top
            :type: str

            Cursor for previous page

    .. py:data:: Methods:

        .. py:method:: get_page(cursor: str)

            Get a Page of tweets

            .. py:data:: Arguments:

                .. py:data:: cursor
                    :type: str

                    Cursor of that specific Page

            .. py:data:: Return
                :type: tuple[list[Tweet | SelfThread | User | ConversationThread | List], cursor: str, cursor_top: str]

        .. py:method:: get_next_page()

            Get next page of tweets if available using the saved cursor

            .. py:data:: Return
                :type: list[Tweet | SelfThread | User | ConversationThread | List]




