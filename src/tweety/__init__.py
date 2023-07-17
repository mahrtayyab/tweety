__version__ = "0.9"
__author__ = "mahrtayyab"

from .bot import BotMethods
from .updates import UpdateMethods
from .auth import AuthMethods


class Twitter(
    BotMethods, UpdateMethods, AuthMethods
):
    pass



