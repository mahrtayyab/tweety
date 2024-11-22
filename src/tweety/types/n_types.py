import datetime
import os
import time
from http.cookiejar import MozillaCookieJar
from httpx._content import encode_multipart_data
from .. import constants
from . import Gif
from ..utils import calculate_md5, get_random_string, check_if_file_is_supported
from ..exceptions import *


class Proxy:
    def __init__(self, host: str, port: int, proxy_type: int, username: str = None, password: str = None):
        self.host = host
        self.password = password
        self.proxy_type = proxy_type
        self.username = username
        self.port = port
        self.proxy = self.__parse__()

    def __iter__(self):
        for k, v in self.proxy.items():
            yield k, v

    def __proxy_url__(self):
        if self.username and self.password:
            return "{}:{}@{}:{}".format(
                self.username, self.password, self.host, self.port
            )
        else:
            return "{}:{}".format(self.host, self.port)

    def __parse__(self):
        proxy_url = self.__proxy_url__()
        if self.proxy_type == constants.HTTP:
            http_url = "http://{}".format(proxy_url)
            return dict.fromkeys(['http://', 'https://'], http_url)
        elif self.proxy_type == constants.SOCKS4:
            socks_url = "socks4://{}".format(proxy_url)
            return dict.fromkeys(['http://', 'https://'], socks_url)
        elif self.proxy_type == constants.SOCKS5:
            socks_url = "socks5://{}".format(proxy_url)
            return dict.fromkeys(['http://', 'https://'], socks_url)

        raise ProxyParseError()

    def get_dict(self):
        return self.proxy


class GenericError:
    EXCEPTIONS = {
        32: InvalidCredentials,
        # 37: SuspendedAccount,
        64: SuspendedAccount,
        88: RateLimitReached,
        141: SuspendedAccount,
        144: InvalidTweetIdentifier,
        214: InvalidBroadcast,
        220: InvalidCredentials,
        326: LockedAccount,
        366: InvalidTweetIdentifier,
        399: InvalidCredentials,
        477: RateLimitReached
    }

    def __init__(self, response, error_code, message=None):
        self.response = response
        self.error_code = error_code
        self.message = message
        self.retry_after = self._get_retry_after()
        self._raise_exception()

    def _get_retry_after(self):
        if all(key in self.response.headers for key in ['x-rate-limit-reset', 'x-rate-limit-remaining']):
            epochLimitTime = int(self.response.headers['x-rate-limit-reset'])
            epochCurrentTime = int(datetime.datetime.now().timestamp())
            return epochLimitTime - epochCurrentTime

        return 0

    def _raise_exception(self):
        if self.EXCEPTIONS.get(self.error_code):
            raise self.EXCEPTIONS[self.error_code](
                error_code=self.error_code,
                error_name=TWITTER_ERRORS[self.error_code],
                response=self.response,
                message=self.message,
                retry_after=self.retry_after
            )

        raise TwitterError(
            error_code=self.error_code,
            error_name=TWITTER_ERRORS.get(self.error_code, 0),
            response=self.response,
            message="[{}] {}".format(self.error_code, self.message)
        )


class Cookies:
    def __init__(self, cookies):
        self._raw_cookies = cookies
        self.parse_cookies()

    def parse_cookies(self):
        if isinstance(self._raw_cookies, MozillaCookieJar):
            for i in self._raw_cookies:
                setattr(self, i.name, i.value)
        else:
            true_cookies = dict()
            if isinstance(self._raw_cookies, str):
                cookie_list = self._raw_cookies.split(";")
                for cookie in cookie_list:
                    split_cookie = cookie.strip().split("=", 1)

                    if len(split_cookie) >= 2:
                        cookie_key = split_cookie[0]
                        cookie_value = split_cookie[1]
                        true_cookies[cookie_key] = cookie_value
            elif isinstance(self._raw_cookies, dict):
                true_cookies = self._raw_cookies
            else:
                raise TypeError("cookies should be of class 'str', 'dict' or 'MozillaCookieJar' not {}".format(self._raw_cookies.__class__))

            for key, value in true_cookies.items():
                setattr(self, key.strip(), value.strip())

    def to_dict(self):
        result = {}
        for k, v in vars(self).items():

            if not k.startswith("_"):
                result[k] = v

        return result

    def __str__(self):
        string = ""
        for k, v in vars(self).items():

            if not k.startswith("_"):
                string += f"{k}={v};"

        return string


class UploadedMedia:
    FILE_CHUNK_SIZE = 2 * 1024 * 1024  # 2 mb

    def __init__(
            self,
            file_path,
            client,
            alt_text=None,
            sensitive_media_warning=None,
            media_category=constants.UPLOAD_TYPE_TWEET_IMAGE
    ):
        self.media_id = None
        self._file = file_path
        self._client = client
        self._alt_text = alt_text
        self._sensitive_media_warning = sensitive_media_warning if sensitive_media_warning else []
        self._source_url = self._get_source_url()
        self.size = self._get_size()
        self.mime_type = self.get_mime_type()
        self._media_category = self._get_media_category(media_category)
        self.md5_hash = calculate_md5(self._file)

    def _get_source_url(self):
        if isinstance(self._file, Gif):
            return self._file.url
        elif str(self._file).startswith("https://"):
            return self._file

        return None

    def _get_media_category(self, category):
        media_for = category.split("_")[0]
        media_type = self.mime_type.split("/")[0]
        return f"{media_for}_{media_type}" if "gif" not in self.mime_type else f"{media_for}_gif"

    def _get_size(self):
        if not self._source_url:
            return os.path.getsize(self._file)
        return 0

    def get_mime_type(self):
        return check_if_file_is_supported(self._file)

    @staticmethod
    def _create_boundary():
        return bytes(f'----WebKitFormBoundary{get_random_string(16)}', "utf-8")

    async def _initiate_upload(self):
        response = await self._client.http.upload_media_init(self.size, self.mime_type, self._media_category, source_url=self._source_url)
        media_id = response.get('media_id_string')

        if not media_id:
            raise ValueError(f"Unable to Initiate the Media Upload: {response}")

        return media_id

    @staticmethod
    def get_multipart_headers(multipart) -> dict[str, str]:
        content_length = multipart.get_content_length()
        content_type = multipart.content_type
        if content_length is None:
            return {"transfer-encoding": "chunked", "content-type": content_type}
        return {"content-length": str(content_length), "content-type": content_type}

    async def _append_upload(self, media_id):
        with open(self._file, "rb") as f:
            segments, remainder = divmod(self.size, self.FILE_CHUNK_SIZE)
            segments += bool(remainder)

            for segment_index in range(segments):
                boundary = self._create_boundary()
                _, multipart = encode_multipart_data({}, {"media": ('blob', f.read(self.FILE_CHUNK_SIZE), "application/octet-stream")}, boundary)
                headers = self.get_multipart_headers(multipart)
                headers.update({"x-media-type": self.mime_type})
                await self._client.http.upload_media_append(media_id, b"".join([i for i in multipart.iter_chunks()]), headers, segment_index)

    async def set_metadata(self):
        await self._client.http.set_media_set_metadata(self.media_id, self._alt_text, self._sensitive_media_warning)

    async def _finish_upload(self, media_id):
        if not self._source_url:
            response = await self._client.http.upload_media_finalize(media_id, self.md5_hash)
        else:
            response = {"processing_info": {"state": "pending", "check_after_secs": 1}}

        if not response.get('processing_info'):
            return

        while True:
            processing_info = response['processing_info']

            if processing_info.get('state') in ('pending', 'in_progress') and 'error' not in processing_info:
                time.sleep(processing_info['check_after_secs'])
                response = await self._client.http.upload_media_status(self.media_id)
            elif processing_info.get("error"):
                error = processing_info["error"]
                code, name, message = error.get("code", 1), error.get("name", ""), error.get("message", "")
                raise TwitterError(
                    error_code=code,
                    error_name=name,
                    response=response,
                    message=message
                )
            else:
                return

    async def upload(self):
        self.media_id = await self._initiate_upload()

        if not self._source_url:
            await self._append_upload(self.media_id)

        await self._finish_upload(self.media_id)

        if self._alt_text:
            await self.set_metadata()

        return self





