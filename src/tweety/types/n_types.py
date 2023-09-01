import os
from http.cookiejar import MozillaCookieJar

from httpx._content import encode_multipart_data
from ..utils import calculate_md5, get_random_string, check_if_file_is_image
from ..exceptions_ import *

PROXY_TYPE_SOCKS4 = SOCKS4 = 1
PROXY_TYPE_SOCKS5 = SOCKS5 = 2
PROXY_TYPE_HTTP = HTTP = 3


class Proxy:
    def __init__(self, host: str, port: int, proxy_type: int, username: str = None, password: str = None):
        self.host = host
        self.password = password
        self.proxy_type = proxy_type
        self.username = username
        self.port = port
        self.proxy = self.__parse__()

    def __proxy_url__(self):
        if self.username and self.password:
            return "{}:{}@{}:{}".format(
                self.username, self.password, self.host, self.port
            )
        else:
            return "{}:{}".format(self.host, self.port)

    def __parse__(self):
        proxy_url = self.__proxy_url__()
        if self.proxy_type == HTTP:
            return dict.fromkeys(['http://', 'https://'], proxy_url)
        elif self.proxy_type == SOCKS4:
            socks_url = "socks4://{}".format(proxy_url)
            return dict.fromkeys(['http://', 'https://'], socks_url)
        elif self.proxy_type == SOCKS5:
            socks_url = "socks5://{}".format(proxy_url)
            return dict.fromkeys(['http://', 'https://'], socks_url)

        raise ProxyParseError()

    def get_dict(self):
        return self.proxy


class GenericError:
    EXCEPTIONS = {
        32: InvalidCredentials,
        144: InvalidTweetIdentifier,
        88: RateLimitReached,
        399: InvalidCredentials,
        220: InvalidCredentials,
        214: InvalidBroadcast
    }

    def __init__(self, response, error_code, message=None):
        self.response = response
        self.error_code = error_code
        self.message = message
        self._raise_exception()

    def _raise_exception(self):
        if self.EXCEPTIONS.get(self.error_code):
            raise self.EXCEPTIONS[self.error_code](
                error_code=self.error_code,
                error_name=TWITTER_ERRORS[self.error_code],
                response=self.response,
                message=self.message
            )

        raise UnknownError(
            error_code=self.error_code,
            error_name=TWITTER_ERRORS[self.error_code],
            response=self.response,
            message="[{}] {}".format(self.error_code, self.message)
        )


class Cookies:
    def __init__(self, cookies, is_http_response=False):
        self._raw_cookies = cookies
        self._is_http_response = is_http_response
        self.parse_cookies()

    def parse_cookies(self):
        if isinstance(self._raw_cookies, MozillaCookieJar):
            for i in self._raw_cookies:
                setattr(self, i.name, i.value)
        else:
            if self._is_http_response:
                # TODO : Find a proper way to parse
                n = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
                for k, p in enumerate(self._raw_cookies.split(",")):
                    if k in n:
                        key, value = str(p.split(';')[0]).split("=", 1)
                        setattr(self, key.strip(), value.strip())
            else:
                true_cookies = dict()
                if isinstance(self._raw_cookies, str):
                    cookie_list = self._raw_cookies.split(";")
                    for cookie in cookie_list:
                        split_cookie = cookie.strip().split("=")

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

    def __str__(self):
        string = ""
        for k, v in vars(self).items():

            if not k.startswith("_"):
                string += f"{k}={v};"

        return string


class UploadedMedia:
    FILE_CHUNK_SIZE = 2 * 1024 * 1024  # 2 mb

    def __init__(self, file_path, client, alt_text=None, sensitive_media_warning=None, media_category="tweet_image"):
        self.media_id = None
        self._file = file_path
        self._client = client
        self._alt_text = alt_text
        self._media_category = media_category
        self._sensitive_media_warning = sensitive_media_warning if sensitive_media_warning else []
        self.size = self._get_size()
        self.mime_type = self.get_mime_type()
        self.md5_hash = calculate_md5(self._file)

    def _get_size(self):
        return os.path.getsize(self._file)

    def get_mime_type(self):
        return check_if_file_is_image(self._file)

    @staticmethod
    def _create_boundary():
        return bytes(f'------WebKitFormBoundary{get_random_string(16)}', "utf-8")

    def _initiate_upload(self):
        response = self._client.http.upload_media_init(self.size, self.mime_type, self._media_category)
        return response['media_id_string']

    def _append_upload(self, media_id):
        with open(self._file, "rb") as f:
            segments, remainder = divmod(self.size, self.FILE_CHUNK_SIZE)
            segments += bool(remainder)

            for segment_index in range(segments):
                boundary = self._create_boundary()
                headers, multipart = encode_multipart_data({}, {"media": ('blob', f.read(self.FILE_CHUNK_SIZE), "application/octet-stream")}, boundary)
                self._client.http.upload_media_append(media_id, multipart, headers, segment_index)

    def set_metadata(self):
        self._client.http.set_media_set_metadata(self.media_id, self._alt_text, self._sensitive_media_warning)

    def _finish_upload(self, media_id):
        self._client.http.upload_media_finalize(media_id, self.md5_hash)

    def upload(self):
        self.media_id = self._initiate_upload()
        self._append_upload(self.media_id)
        self._finish_upload(self.media_id)

        if self._alt_text:
            self.set_metadata()

        return self





