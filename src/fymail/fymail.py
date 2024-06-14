import asyncio
import aiohttp
from functools import cached_property, cache

from fymail.provider_manager import ProviderManger
from fymail.providers.base.provider_base import ProviderBase
from functools import cache, cached_property


class FyMail:

    def __init__(self):
        self.pm = ProviderManger()
        self.pm.register_plugin()

    async def get(self,
                  *,
                  iden: str,
                  provider: str,
                  auth: str) -> str:
        provider = self.pm.get_provider(provider)
        async with aiohttp.ClientSession() as session:
            return await provider.get(session, auth, iden)

    async def get_bulk(self,
                       path: str,
                       provider: str,
                       io_type: str = None,
                       delimiter: str = None,
                       col: int = None,
                       ) -> str:
        raise NotImplementedError
