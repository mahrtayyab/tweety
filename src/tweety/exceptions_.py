import traceback


class UserNotFound(Exception):
    """Exception raised when user isn't found.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class GuestTokenNotFound(Exception):
    """
    Exception Raised when the guest token wasn't found after specific number of retires

    Attributes:
        message -- explanation of the error
    """

    def __init__(self,message):
        self.message = message
        super().__init__(self.message)


class InvalidTweetIdentifier(Exception):
    """
        Exception Raised when the tweet identifier is invalid

        Attributes:
            message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ProxyParseError(Exception):
    """
    Exception Raised when an error occurs while parsing the provided proxy

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Error while parsing the Proxy, please make sure you are passing the right formatted proxy"):
        self.message = message
        super().__init__(self.message)


class UserProtected(Exception):
    """
    Exception Raised when an error occurs when the queried User isn't available / Protected

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UnknownError(Exception):
    """
        Exception Raised when an unknown error occurs

        Attributes:
            message -- explanation of the error
        """

    def __init__(self, message):
        if not isinstance(message,UserProtected) or not isinstance(message,UserNotFound):
            error = traceback.format_exc().splitlines()[-1]
            self.message = error
            super().__init__(self.message)

