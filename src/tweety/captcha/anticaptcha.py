from anticaptchaofficial.funcaptchaproxyless import funcaptchaProxyless
from anticaptchaofficial.funcaptchaproxyon import funcaptchaProxyon
from .base import BaseCaptchaSolver
from ..utils import unpack_proxy
from ..constants import REQUEST_USER_AGENT
from ..exceptions import CaptchaSolverFailed


class AntiCaptcha(BaseCaptchaSolver):
    def __init__(self, api_key, proxy=None, verbose=False):
        self._api_key = api_key
        self._verbose = verbose
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
        if self._proxy is None:
            solver = funcaptchaProxyless()
        else:
            solver = funcaptchaProxyon()
            proxy_dict = unpack_proxy(self._proxy)
            solver.set_user_agent(REQUEST_USER_AGENT)
            solver.set_proxy_type(proxy_dict.get("type"))
            solver.set_proxy_address(proxy_dict.get("host"))
            solver.set_proxy_port(proxy_dict.get("port"))

            if proxy_dict.get("username"):
                solver.set_proxy_login(proxy_dict.get("username"))
                solver.set_proxy_password(proxy_dict.get("password"))

        solver.set_verbose(1 if self._verbose is True else 0)
        solver.set_key(self._api_key)
        solver.set_website_url(websiteUrl)
        solver.set_website_key(websitePublicKey)
        solver.set_js_api_domain("client-api.arkoselabs.com")

        if blob_data:
            solver.set_data_blob(blob_data)

        token = solver.solve_and_return_solution()

        if token != 0:
            return token

        raise CaptchaSolverFailed(message=f"Unable to Solve Captcha using 'AntiCaptcha' : [{solver.error_code}] {solver.err_string}")

