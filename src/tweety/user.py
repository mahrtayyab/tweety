from typing import Union, Generator

from .types.inbox import Message
from .utils import create_conversation_id
from .types import User, Mention, Inbox, UploadedMedia, SendMessage, Tweet, Bookmarks


class UserMethods:

    @property
    def me(self) -> User:
        """

        :return:
        """
        return self.user

    def get_mentions(
            self,
            pages: int = 1,
            wait_time: int = 2,
            cursor: str = None
    ) -> Mention:
        """

        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: .types.mention.Mention
        """

        if wait_time is None:
            wait_time = 0

        mentions = Mention(self.user.id, self.request, pages, wait_time, cursor)
        results = list(mentions.generator())

        return mentions

    def iter_mentions(
            self,
            pages: int = 1,
            wait_time: int = 2,
            cursor: str = None
    ):
        """

        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: (.types.mention.Mention, list[.types.twDataTypes.Tweet])
        """

        if wait_time is None:
            wait_time = 0

        mentions = Mention(self.user.id, self.request, pages, wait_time, cursor)

        return mentions.generator()

    def get_bookmarks(
            self,
            pages: int = 1,
            wait_time: int = 2,
            cursor: str = None
    ) -> Bookmarks:
        """

        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: Bookmarks
        """

        if wait_time is None:
            wait_time = 0

        bookmarks = Bookmarks(self.user.id, self.request, pages, wait_time, cursor)
        results = list(bookmarks.generator())

        return bookmarks

    def iter_bookmarks(
            self,
            pages: int = 1,
            wait_time: int = 2,
            cursor: str = None
    ):
        """

        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return: (.types.bookmarks.Bookmarks, list[.types.twDataTypes.Tweet])
        """

        if wait_time is None:
            wait_time = 0

        bookmarks = Bookmarks(self.user.id, self.request, pages, wait_time, cursor)

        return bookmarks.generator()

    def get_inbox(
            self,
            user_id: Union[int, str, User] = None,
            cursor: str = None
    ) -> Inbox:
        """
        :param user_id : (`str`, `int`, `User`) User id or username of the user whom to get the messages of. Default is ALL
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
                                It is used to get the messages updates
        :return:
        """

        if user_id:
            user_id = self._get_user_id(user_id)

        inbox = Inbox(user_id, self.request, cursor)

        return inbox

    def send_message(
            self,
            username: Union[str, int, User],
            text: str,
            file: Union[str, UploadedMedia] = None
    ) -> Message:

        """
        Send Message to a Twitter User
        :param file: (`str`, `UploadedMedia`) File to be sent with message too
        :param username: (`str`, `int`, `User`) Username of the user whom to send message
        :param text: (`str`) Text to be sent as message
        :return: .types.inbox.Message

        :example:
            from tweety import Twitter
            client = Twitter()
            client.send_message("elonmusk", "Hi Musk!")
        """

        user_id = self._get_user_id(username)
        conversation_id = create_conversation_id(self.user.id, user_id)

        if file:
            file = self._upload_media(file, "dm_image")[0].media_id

        return SendMessage(self.request, conversation_id, text, file).send()

    def create_tweet(
            self,
            text: str,
            files: list[Union[str, UploadedMedia, tuple[str, str]]] = None,
            filter_: str = None,
            reply_to: Union[str, Tweet] = None
    ) -> Tweet:

        """
        Create a Tweet

        :param text: (`str`) Text content of Tweet
        :param files: (`list[Union[str, UploadedMedia, tuple[str, str]]]`) Files to be sent with Tweet (max 4)
        :param filter_: (`str`) Filter to applied for Tweet audience
        :param reply_to: (`str` | `Tweet`) ID of tweet to reply to
        :return: Tweet
        """

        if files:
            files = self._upload_media(files)
        else:
            files = []

        if isinstance(reply_to, Tweet):
            reply_to = reply_to.id

        response = self.request.create_tweet(text, files, filter_, reply_to)
        return Tweet(response['data']['create_tweet']['tweet_results']['result'], self.request, response)

    def _upload_media(self, files, _type="tweet_image"):
        if not isinstance(files, list):
            files = [files]

        uploaded = []

        for file in files:
            if isinstance(file, (tuple, list)):
                file_path = file[0]
                alt_text = file[1]
            else:
                file_path = file
                alt_text = None

            if isinstance(file_path, UploadedMedia):
                if file_path.media_id is None:
                    uploaded.append(file_path.upload())
                else:
                    uploaded.append(file_path)
            else:
                uploaded.append(UploadedMedia(file_path, self.request, alt_text, None, _type).upload())

        return uploaded
