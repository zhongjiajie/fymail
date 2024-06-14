import re

from aiohttp import ClientSession, ClientResponse

from fymail.providers.base.rule_base import RuleBase
import logging


logger = logging.getLogger(__name__)

class Profile(RuleBase):
    """Get from user's profile repository readme content

    :seealso: https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#get-a-repository-readme
    """
    name = "GH10"
    path = "repos"

    def build_url(self, iden: str) -> str:
        return f"{super().build_url(iden)}/{iden}/readme"

    async def run(self,
                  session: ClientSession,
                  iden: str,
                  params: dict | None = None) -> str | None:
        download_url = await super().run(session, iden)
        if download_url is None:
            return None

        email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

        # get github profile content
        async with session.get(download_url) as response:
            content = await response.text()
            logger.debug("Get profile content from %s is: %s", repr(self), content)

            emails = email_pattern.findall(content)
            logger.debug("Get response from %s is: %s, only pick index=0 if more than one.", repr(self), emails)
            return emails[0] if emails else None

    async def parse(self, resp: ClientResponse) -> str | None:
        resp_json = await resp.json()
        if resp_json is None or "download_url" not in resp_json:
            return None
        return resp_json["download_url"]