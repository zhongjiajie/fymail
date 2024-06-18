from aiohttp import ClientSession

from fymail.providers.base.provider_base import ProviderBase


class GitHub(ProviderBase):
    base_url = "https://api.github.com"
    provider_name = "GitHub"
    package_provider = "fymail.providers.github"

    def __init__(self, *args, **kwargs):
        super(ProviderBase, self).__init__(*args, **kwargs)

    @staticmethod
    def auth_setter(session: ClientSession, auth: str) -> None:
        session.headers.update({
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {auth}",
            "X-GitHub-Api-Version": "2022-11-28",
        })
