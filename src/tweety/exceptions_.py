class UserNotFound(Exception):
    """Exception raised when user isn't found.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Either User not Found or is Restricted"):
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


class UnknownError(Exception):
    """
        Exception Raised when an unknown error occurs

        Attributes:
            message -- explanation of the error
        """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

