from __future__ import annotations

import aiohttp

from fymail.provider_manager import ProviderManger


class FyMail:
    def __init__(self):
        self.pm = ProviderManger()
        self.pm.register_plugin()

    async def get(self, *, iden: str, provider: str, auth: str) -> str:
        provider = self.pm.get_provider(provider)
        async with aiohttp.ClientSession() as session:
            return await provider.get(session, auth, iden)

    async def get_bulk(
        self,
        path: str,
        provider: str,
        io_type: str | None = None,
        delimiter: str | None = None,
        col: int | None = None,
    ) -> str:
        raise NotImplementedError
