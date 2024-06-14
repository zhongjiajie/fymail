from aiohttp import ClientSession, ClientResponse

from fymail.providers.base.rule_base import RuleBase

import logging
import asyncio

logger = logging.getLogger(__name__)


class Commit(RuleBase):
    """Get from user owner repository last commits' payload

    :seealso: https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repositories-for-a-user
    :seealso: https://docs.github.com/en/rest/commits/commits?apiVersion=2022-11-28#list-commits
    """

    name = "GH20"
    path = "users"

    def build_url(self, iden: str) -> str:
        return f"{self.build_url_path()}/{iden}/repos"

    async def run(self,
                  session: ClientSession,
                  iden: str,
                  params: dict | None = None) -> str | None:
        if self.headers:
            session.headers.update(self.headers)

        # we only need owner repositories and for latest page
        params = {"type": "owner", "sort": "updated", "author": iden}
        async with session.get(self.build_url(iden), params=params) as response:
            resp: list[dict] = await response.json()
            logger.debug("Get response from %s is: %s", repr(self), resp)
            # fork repo cause wrong result
            url_repo_commits = [f"{repo['url']}/commits" for repo in resp if repo["fork"] is False]

            if not url_repo_commits:
                return None

            tasks = [session.get(url) for url in url_repo_commits]
            tasks_result: list[ClientResponse] = await asyncio.gather(*tasks)
            emails = [await self.parse(resp) for resp in tasks_result]
            logger.debug("Get email from %s is: %s, only pick index=0 if more than one.", repr(self), emails)
            return emails[0] if emails else None

    async def parse(self, resp: ClientResponse) -> str | None:
        response: list[dict] = await resp.json()
        logger.debug("Get response from %s is: %s", repr(self), response)
        for commit in response:
            
            if "commit" not in commit:
                continue
            auther = commit["commit"]["author"]
            if auther and "email" in auther and not auther["email"].endswith("users.noreply.github.com"):
                return auther["email"]
        return None

