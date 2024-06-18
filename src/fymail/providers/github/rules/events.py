from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from fymail.providers.base.rule_base import RuleBase

if TYPE_CHECKING:
    from aiohttp import ClientResponse, ClientSession

logger = logging.getLogger(__name__)


class Events(RuleBase):
    """Get from user push events' payload

    :seealso: https://docs.github.com/en/rest/activity/events?apiVersion=2022-11-28#list-events-for-the-authenticated-user
    """

    name = "GH30"
    path = "users"
    limit = 5

    def build_url(self, iden: str) -> str:
        return f"{super().build_url(iden)}/events"

    async def run(self, session: ClientSession, iden: str, params: dict | None = None) -> str | None:
        for page in range(1, self.limit + 1):
            params = {"page": page}
            return await super().run(session, iden, params)
        return None

    async def parse(self, resp: ClientResponse) -> str | None:
        response: list[dict] = await resp.json()
        logger.debug("Get response from %s is: %s", repr(self), response)
        for event in response:
            # TODO: some push event may merge PR to main branch, should ignore it
            if event and event["type"] == "PushEvent":
                for commit in event["payload"]["commits"]:
                    if (
                        "author" in commit
                        and "email" in commit["author"]
                        and not commit["author"]["email"].endswith("users.noreply.github.com")
                    ):
                        return commit["author"]["email"]
        return None
