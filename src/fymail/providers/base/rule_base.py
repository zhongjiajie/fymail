from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from fymail.error import NoRuleNameError, NoRuleUrlPathError

if TYPE_CHECKING:
    from aiohttp import ClientResponse, ClientSession


class RuleBaseMeta(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)

        if cls.__name__ == 'RuleBase':
            return

        if getattr(cls, 'name', None) is None:
            raise NoRuleNameError

        if getattr(cls, 'path', None) is None:
            raise NoRuleUrlPathError


class RuleBase(metaclass=RuleBaseMeta):
    name = None
    path = None
    headers = None

    def __init__(self, base_url: str):
        self.base_url = base_url

    def __repr__(self):
        return f'<Rule: class:{self.__class__.__name__}, name:{self.name}>'

    def build_url_path(self) -> str:
        return f'{self.base_url}/{self.path}'

    def build_url(self, iden: str) -> str:
        return f'{self.build_url_path()}/{iden}'

    async def run(self, session: ClientSession, iden: str, params: dict | None = None) -> str | None:
        if self.headers:
            session.headers.update(self.headers)
        async with session.get(self.build_url(iden), params=params) as response:
            return await self.parse(response)

    @abstractmethod
    async def parse(self, response: ClientResponse) -> str | None:
        pass
