import warnings
import httpx
import re
from ..types.n_types import Proxy
from ..constants import LOGIN_SITE_KEY
from ..exceptions import CaptchaSolverFailed

"""
Modified Code from : https://github.com/ZakariaMQ/twitter-account-unlocker
"""


class BaseCaptchaSolver:
    def __init__(self, api_key, proxy) -> None:
        self._cookies = None
        self._proxy = proxy
        self._api_key = api_key
        self.url = "https://x.com/account/access"
        self.client = None
        self.headers = None
        self._tokens = {}

    def init(self, cookies, proxy):
        self._cookies = cookies
        proxy_from_client = proxy

        if isinstance(self._proxy, bool) and self._proxy is True:
            if proxy_from_client is None:
                warnings.warn("No Proxy was found in Client , Captcha will be solved without Proxy")
                proxy = None
            else:
                proxy = proxy_from_client
        elif isinstance(self._proxy, (dict, Proxy)):
            proxy = self._proxy
        else:
            proxy = None

        if isinstance(proxy, str):
            self._proxy = dict.fromkeys(["http://", "https://"], proxy)
        elif isinstance(proxy, Proxy):
            self._proxy = proxy.get_dict()
        else:
            self._proxy = proxy

        self.client = httpx.Client(timeout=30, follow_redirects=True, proxies=self._proxy)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Accept": "*/*",
            "Accept-Language": "en-GB,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Sec-GPC": "1",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "script",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers"
        }

    def __extract_tokens_from_access_html_page(self, html: str):
        pattern = re.compile(r'name="authenticity_token" value="([^"]+)"|name="assignment_token" value="([^"]+)"')
        matches = pattern.findall(html)
        if matches:
            authenticity_token = matches[0][0] if matches[0][0] else matches[0][1]
            assignment_token = matches[1][0] if matches[1][0] else matches[1][1]
            self._tokens = {"authenticity_token": authenticity_token,
                            "assignment_token": assignment_token}

    def __js_inst(self):
        js_script = self.client.get(
            url="https://x.com/i/js_inst?c_name=ui_metrics"
        ).text
        pattern = re.compile(r'return\s*({.*?});', re.DOTALL)
        js_instr = pattern.search(js_script)

        return js_instr.group(1)

    def __get_access_page(self):
        res = self.client.get(self.url, headers=self.headers, cookies=self._cookies)
        self._cookies.update(dict(res.cookies))
        self.__extract_tokens_from_access_html_page(html=res.text)

    def __post_to_access_page(self, data: dict):
        headers = self.headers
        headers["Host"] = "x.com"
        headers["Origin"] = "https://x.com"
        headers["Referer"] = "https://x.com/account/access"

        res = self.client.post(f"{self.url}?lang=en", data=data, headers=headers, cookies=self._cookies)
        self._cookies.update(dict(res.cookies))
        self.__extract_tokens_from_access_html_page(html=res.text)

    def __data_with_js_inst(self, tokens: dict) -> dict:
        return {
            "authenticity_token": tokens["authenticity_token"],
            "assignment_token": tokens["assignment_token"],
            "lang": "en",
            "flow": "",
            "ui_metrics": self.__js_inst()
        }

    @staticmethod
    def __data_with_funcaptcha(tokens: dict, fun_captcha_token: str) -> dict:
        return {
            "authenticity_token": tokens["authenticity_token"],
            "assignment_token": tokens["assignment_token"],
            'lang': 'en',
            'flow': '',
            'verification_string': fun_captcha_token,
            'language_code': 'en'
        }

    def __post_data_with_token(self, fun_captcha_token: str):
        data = self.__data_with_funcaptcha(tokens=self._tokens, fun_captcha_token=fun_captcha_token)
        self.__post_to_access_page(data=data)

    def __post_data_with_js_inst(self):
        data = self.__data_with_js_inst(tokens=self._tokens)
        self.__post_to_access_page(data=data)

    def unlock(self, websitePublicKey="0152B4EB-D2DC-460A-89A1-629838B529C9", websiteUrl="https://twitter.com/", blob_data=None):
        try:
            if not blob_data and websitePublicKey != LOGIN_SITE_KEY:
                self.__get_access_page()

                self.__post_data_with_js_inst()

                fun_captcha_token = self.get_solved_token(websitePublicKey=websitePublicKey, websiteUrl=websiteUrl)

                self.__post_data_with_token(fun_captcha_token=fun_captcha_token)

                fun_captcha_token = self.get_solved_token(websitePublicKey=websitePublicKey, websiteUrl=websiteUrl)

                self.__post_data_with_token(fun_captcha_token=fun_captcha_token)

                self.__post_data_with_js_inst()
                return fun_captcha_token
            else:
                fun_captcha_token = self.get_solved_token(websitePublicKey=websitePublicKey, websiteUrl=websiteUrl, blob_data=blob_data)
                return fun_captcha_token
        except Exception as e:
            raise CaptchaSolverFailed(message=str(e))
