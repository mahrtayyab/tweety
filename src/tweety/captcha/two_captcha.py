from twocaptcha import TwoCaptcha as TwoCaptchaSolver
from .base import BaseCaptchaSolver
from ..utils import unpack_proxy


class TwoCaptcha(BaseCaptchaSolver):
    def __init__(self, api_key, proxy=None):
        self._api_key = api_key
        super().__init__(self._api_key, proxy)

    def __call__(self, twitter_client):
        super().init(cookies=twitter_client.session.cookies_dict, proxy=twitter_client._proxy)
        return self

    def get_solved_token(
            self,
            websitePublicKey,
            websiteUrl,
            blob_data=None
    ) -> str:
        solver = TwoCaptchaSolver(self._api_key)
        request = dict(
            sitekey=websitePublicKey,
            url=websiteUrl,
            data=blob_data
        )

        if self._proxy is not None:
            this_proxy = unpack_proxy(self._proxy)
            proxy_uri = f"{this_proxy['host']}:{this_proxy['port']}"

            if this_proxy.get("username"):
                proxy_uri = f"{this_proxy['username']}:{this_proxy['password']}@{proxy_uri}"

            request["proxy"] = {"type": this_proxy["type"].upper(), "uri": proxy_uri}

        token = solver.funcaptcha(**request)

        return token.get("code")