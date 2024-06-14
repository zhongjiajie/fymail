import pytest
from fymail import FyMail
import os
import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

fymail = FyMail()

provider = "github"
token = os.environ.get("FYMAIL_GH_TOKEN", None)
if not token:
    raise ValueError("Please set the environment variable ``FYMAIL_GH_TOKEN``")


@pytest.mark.parametrize(
    "iden, rule",
    [
        ("zhongjiajie", "<Rule: class:Users, name:GH01>"),
        ("pnasrat", "<Rule: class:Profile, name:GH10>"),
        ("pfmoore", "<Rule: class:Commit, name:GH20>"),
        ("piwai", "<Rule: class:Events, name:GH30>"),
    ]
)
@pytest.mark.asyncio
async def test_gh_rules_users(iden, rule, caplog):
    with caplog.at_level(logging.INFO):
        email = await fymail.get(iden=iden, provider=provider, auth=token)
        assert email is not None and rule in caplog.text

