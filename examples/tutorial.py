import asyncio
from fymail import FyMail
import logging
import os

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

# Set the environment variable ``FYMAIL_GH_TOKEN`` to your GitHub token
gh_token = os.environ.get("FYMAIL_GH_TOKEN", None)
if not gh_token:
    raise ValueError("Please set the environment variable ``FYMAIL_GH_TOKEN``")


async def main():
    fymail = FyMail()
    email = await fymail.get(iden="zhongjiajie", provider="github", auth=gh_token)
    print(email)


if __name__ == "__main__":
    asyncio.run(main())
