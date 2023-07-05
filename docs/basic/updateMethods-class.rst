
.. _updateMethod-class:

===================
UpdateMethod Class
===================


.. py:class:: UpdateMethod()

    This is the main class for the update methods

    .. py:method:: add_event_handler(callback ,event)

        Add a new event handler to listen

        .. py:data:: Arguments:

            .. py:data:: callback
                :type: func

                callback function to call when event happens

            .. py:data:: event
                :type: func

                Actual Event

        .. py:data:: Return
            :type: None

    .. py:method:: on(event)

        This Method is decorated version of `add_event_handler`

        .. py:data:: Return
            :type: None

    .. py:method:: run_until_disconnected()

        Call this function to block the script from exiting when listening for an event

        .. py:data:: Return
            :type: None

    More about events are Here :ref:`events`!
