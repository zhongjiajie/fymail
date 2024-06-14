from aiohttp import ClientSession, ClientResponse

from fymail.providers.base.rule_base import RuleBase

import logging

logger = logging.getLogger(__name__)

class Users(RuleBase):
    """Get from user public information

    :seealso: https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28#get-a-user
    """
    name = "GH01"
    path = "users"

    async def parse(self, resp: ClientResponse) -> str | None:
        response = await resp.json()
        logger.debug("Get response from %s is: %s", repr(self), response)
        return response["email"] if "email" in response else None
