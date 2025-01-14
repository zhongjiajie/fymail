from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING

from fymail.providers.base.rule_base import RuleBase

if TYPE_CHECKING:
    from aiohttp import ClientResponse, ClientSession
from fymail.utils.collect import most_common_element

logger = logging.getLogger(__name__)


class Profile(RuleBase):
    """Get from user's profile repository readme content

    :seealso: https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#get-a-repository-readme
    """

    name = "GH10"
    path = "repos"
    check_resp: bool = False

    def build_url(self, iden: str) -> str:
        return f"{super().build_url(iden)}/{iden}/readme"

    async def run(self, session: ClientSession, iden: str, params: dict | None = None) -> str | None:
        download_url = await super().run(session, iden, params)
        if download_url is None:
            return None

        email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

        # get github profile content
        async with session.get(download_url) as response:
            response.raise_for_status()
            content = await response.text()
            logger.debug("Get profile content from %s is: %s", repr(self), content)

            emails = email_pattern.findall(content)
            email = most_common_element(emails, ignore_none=True)
            logger.debug("Get response from %s is: %s, try to get most common element: %s.", repr(self), emails, email)
            return email

    async def parse(self, resp: ClientResponse) -> str | None:  # noqa: PLR6301
        resp_json = await resp.json()
        if resp_json is None or "download_url" not in resp_json:
            return None
        return resp_json["download_url"]
