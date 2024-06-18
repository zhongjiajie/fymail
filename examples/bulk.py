from __future__ import annotations

import asyncio
import logging
import os
import time

import aiohttp
from aiohttp import ClientSession

from fymail import FyMail

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

# Set the environment variable ``FYMAIL_GH_TOKEN`` to your GitHub token
gh_token = os.environ.get("FYMAIL_GH_TOKEN", None)
if not gh_token:
    msg = "Please set the environment variable ``FYMAIL_GH_TOKEN``"
    raise ValueError(msg)

repos = [
    "python/cpython",
    "pypa/pip",
]

session_header = {
    "Authorization": f"token {gh_token}",
    "X-GitHub-Api-Version": "2022-11-28",
    "Accept": "application/vnd.github+json",
}


async def get_repo_contributors(session: ClientSession, repo: str, *, simple: bool | None = False) -> list[str]:
    contributors = []
    url = f"https://api.github.com/repos/{repo}/contributors"

    page = 1
    while True:
        async with session.get(url, params={"page": page}) as response:
            response.raise_for_status()
            data = await response.json()
            if not data:
                break
            contributors.extend([d.get("login") for d in data if "login" in d])
            page += 1

            # break current loop
            if simple:
                break
    return contributors


async def main():
    async with aiohttp.ClientSession() as session:
        session.headers.update(session_header)

        fymail = FyMail()
        task_emails = []
        contributors = []
        for repo in repos:
            contributors.extend(await get_repo_contributors(session, repo, simple=True))
            task_emails.extend([fymail.get(iden=c, provider="github", auth=gh_token) for c in contributors])

        time.perf_counter()
        await asyncio.gather(*task_emails)
        time.perf_counter()


if __name__ == "__main__":
    asyncio.run(main())
