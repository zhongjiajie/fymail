import asyncio
import logging
import os

from fymail import FyMail

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

# Set the environment variable ``FYMAIL_GH_TOKEN`` to your GitHub token
gh_token = os.environ.get("FYMAIL_GH_TOKEN", None)
if not gh_token:
    msg = "Please set the environment variable ``FYMAIL_GH_TOKEN``"
    raise ValueError(msg)


async def main():
    fymail = FyMail()
    return await fymail.get(iden="zhongjiajie", provider="github", auth=gh_token)


if __name__ == "__main__":
    print(asyncio.run(main()))
