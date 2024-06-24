from .base import BaseCaptchaSolver
import capsolver
from ..utils import unpack_proxy


class CapSolver(BaseCaptchaSolver):
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
        capsolver.api_key = self._api_key

        request = {
            "type": "FunCaptchaTaskProxyLess",
            "websitePublicKey": websitePublicKey,
            "websiteURL": websiteUrl,
        }
        if self._proxy is not None:
            proxy_dict = unpack_proxy(self._proxy)
            request.update({
                "type": "FunCaptchaTask",
                "proxyType": proxy_dict.get("type"),
                "proxyAddress": proxy_dict.get("host"),
                "proxyPort": proxy_dict.get("port"),
                "proxyLogin": proxy_dict.get("username"),
                "proxyPassword": proxy_dict.get("password")
            })

        if blob_data:
            request["data"] = "{{\"blob\": \"{}\"}}".format(blob_data)

        return capsolver.solve(request)["token"]

