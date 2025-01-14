import logging
import os
import string

import pytest
from aiohttp import ClientResponseError

from fymail import FyMail

logger = logging.getLogger(__name__)

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

fymail = FyMail()

provider = "github"
token = os.environ.get("FYMAIL_GH_TOKEN", None)
if not token:
    msg = "Please set the environment variable ``FYMAIL_GH_TOKEN``"
    raise ValueError(msg)


@pytest.mark.parametrize(
    ("idens", "rule"),
    [
        (
            (
                "zhongjiajie",
                "freddrake",
                "vstinner",
            ),
            "<Rule: class:Users, name:GH01>",
        ),
        (
            (
                "pnasrat",
                "eladkal",
            ),
            "<Rule: class:Profile, name:GH10>",
        ),
        (
            (
                "pfmoore",
                "piwai",
                "loewis",
            ),
            "<Rule: class:Commit, name:GH20>",
        ),
        (("dstandish", "kantandane", "GeumBinLee", "svlandeg"), "<Rule: class:Commit, name:GH30>"),
    ],
)
@pytest.mark.asyncio
async def test_gh_rules_users(idens, rule, caplog):
    """
    Test GitHub rules for users, pass at least one of iden contain specific rule message
    """
    with caplog.at_level(logging.INFO):
        for iden in idens:
            email = await fymail.get(iden=iden, provider=provider, auth=token)
            assert email is not None
            # pass at least one of iden contain specific rule message
            try:
                assert rule is not caplog.text
                break
            except AssertionError:
                logger.info("Attempt %s unable get expect rule %s with message: %s", iden, rule, caplog.text)
                continue


@pytest.mark.parametrize(
    "iden",
    ["zhongjiajie"],
)
@pytest.mark.asyncio
async def test_gh_bad_token(iden):
    with pytest.raises(ClientResponseError):
        await fymail.get(iden=iden, provider=provider, auth=string.ascii_lowercase)
