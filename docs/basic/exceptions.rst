.. _exceptions:

=============
Exceptions
=============

This page contains all the Exceptions raised by the different methods

AuthenticationRequired
------------------------

.. py:class:: AuthenticationRequired

    Bases : `Exception`

    :description: **This Exception is raised when you use a method which required the user to be authenticated.**

    :reference: `tweety.exceptions_.AuthenticationRequired`

    .. py:data:: Attributes:

        .. py:attribute:: message
            :type: str
            :value: You need to be authenticated to make this request

            Main Exception Message

        .. py:attribute:: error_code
            :type: int
            :value: 200

            Exception Error Code

        .. py:attribute:: error_name
            :type: str
            :value: GenericForbidden

            Twitter Internal Error Name

        .. py:attribute:: response
            :type: httpx.Response

            Raw Response returned by the Twitter

UserNotFound
---------------------

.. py:class:: UserNotFound

    Bases : `Exception`

    :description: **This Exception is raised when you use a method which required the user to be authenticated.**

    :reference: `tweety.exceptions_.UserNotFound`

    .. py:data:: Attributes:

        .. py:attribute:: message
            :type: str
            :value: The User Account wasn't Found

            Main Exception Message

        .. py:attribute:: error_code
            :type: int
            :value: 50

            Exception Error Code

        .. py:attribute:: error_name
            :type: str
            :value: GenericUserNotFound

            Twitter Internal Error Name

        .. py:attribute:: response
            :type: httpx.Response

            Raw Response returned by the Twitter


InvalidTweetIdentifier
------------------------

.. py:class:: InvalidTweetIdentifier

    Bases : `Exception`

    :description: **This Exception is raised when the tweet which is begin queried is not Found / Invalid**.

    :reference: `tweety.exceptions_.InvalidTweetIdentifier`

    .. py:data:: Attributes:

        .. py:attribute:: message
            :type: str
            :value: The Tweet Identifier is Invalid

            Main Exception Message

        .. py:attribute:: error_code
            :type: int
            :value: 144

            Exception Error Code

        .. py:attribute:: error_name
            :type: str
            :value: StatusNotFound

            Twitter Internal Error Name

        .. py:attribute:: response
            :type: httpx.Response

            Raw Response returned by the Twitter

GuestTokenNotFound
---------------------

.. py:class:: GuestTokenNotFound

    Bases : `Exception`

    :description: **This Exception is raised when guest token couldn't be obtained.**

    :reference: `tweety.exceptions_.GuestTokenNotFound`

    .. py:data:: Attributes:

        .. py:attribute:: message
            :type: str
            :value: The Guest Token couldn't be obtained

            Main Exception Message

        .. py:attribute:: error_code
            :type: None
            :value: None

            Exception Error Code

        .. py:attribute:: error_name
            :type: None
            :value: None

            Twitter Internal Error Name

        .. py:attribute:: response
            :type: httpx.Response

            Raw Response returned by the Twitter

UserProtected
---------------------

.. py:class:: UserProtected

    Bases : `Exception`

    :description: **This Exception is raised when the user which is begin queried has private profile.This can be fixed by authenticating the request using cookies**

    :reference: `tweety.exceptions_.UserProtected`

    .. py:data:: Attributes:

        .. py:attribute:: message
            :type: str
            :value: The User is Protected , please make sure you are authenticated and authorized

            Main Exception Message

        .. py:attribute:: error_code
            :type: int
            :value: 403

            Exception Error Code

        .. py:attribute:: error_name
            :type: str
            :value: UserUnavailable

            Twitter Internal Error Name

        .. py:attribute:: response
            :type: httpx.Response

            Raw Response returned by the Twitter

InvalidCredentials
---------------------

.. py:class:: InvalidCredentials

    Bases : `Exception`

    :description: **This Exception is raised when the cookies provided for authentication are invalid**

    :reference: `tweety.exceptions_.InvalidCredentials`

    .. py:data:: Attributes:

        .. py:attribute:: message
            :type: str
            :value: The Cookies are Invalid

            Main Exception Message

        .. py:attribute:: error_code
            :type: int
            :value: 403

            Exception Error Code

        .. py:attribute:: error_name
            :type: str
            :value: UserUnavailable

            Twitter Internal Error Name

        .. py:attribute:: response
            :type: httpx.Response

            Raw Response returned by the Twitter

RateLimitReached
---------------------

.. py:class:: RateLimitReached

    Bases : `Exception`

    :description: **This Exception is raised when you have exceeded the Twitter Rate Limit**

    :reference: `tweety.exceptions_.RateLimitReached`

    .. py:data:: Attributes:

        .. py:attribute:: message
            :type: str
            :value: You have exceeded the Twitter Rate Limit

            Main Exception Message

        .. py:attribute:: error_code
            :type: int
            :value: 88

            Exception Error Code

        .. py:attribute:: error_name
            :type: str
            :value: RateLimitExceeded

            Twitter Internal Error Name

        .. py:attribute:: response
            :type: httpx.Response

            Raw Response returned by the Twitter

UnknownError
---------------------

.. py:class:: UnknownError

    Bases : `Exception`

    :description: **This Exception is raised when a error unknown to Tweety occurs**
    :reference: `tweety.exceptions_.UnknownError`

    .. py:data:: Attributes:

        .. py:attribute:: message
            :type: str

            Main Exception Message

        .. py:attribute:: error_code
            :type: int

            Exception Error Code

        .. py:attribute:: error_name
            :type: str

            Twitter Internal Error Name

        .. py:attribute:: response
            :type: httpx.Response

            Raw Response returned by the Twitter