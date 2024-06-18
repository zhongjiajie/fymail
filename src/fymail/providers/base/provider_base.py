from __future__ import annotations

import importlib
import inspect
import logging
import pkgutil
from abc import abstractmethod
from typing import TYPE_CHECKING, ClassVar

from fymail.error import NoProviderBaseUrlPathError, NoProviderNameError
from fymail.providers.base.rule_base import RuleBase

if TYPE_CHECKING:
    from aiohttp import ClientSession

logger = logging.getLogger(__name__)


class ProviderBaseMeta(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)

        if cls.__name__ == 'ProviderBase':
            return

        if getattr(cls, 'base_url', None) is None:
            raise NoProviderBaseUrlPathError

        if getattr(cls, 'provider_name', None) is None:
            raise NoProviderNameError

        # if getattr(cls, 'package_provider', None) is None:
        #     raise NoProviderNameError


class ProviderBase(metaclass=ProviderBaseMeta):
    base_url: str = None
    provider_name: str = None
    package_provider: str = None
    rules: ClassVar[list[RuleBase]] = []

    def __repr__(self):
        return f'<Provider: {self.provider_name}>'

    def name(self) -> str:
        return self.provider_name

    @staticmethod
    @abstractmethod
    def auth_setter(session: ClientSession, auth: str) -> None:
        pass

    @abstractmethod
    async def get(self, session: ClientSession, auth: str, iden: str) -> str | None:
        self.register_rules()
        self.auth_setter(session, auth)

        for rule in self.rules:
            logger.info("Trying to get %s's email with %s", iden, repr(rule))
            result = await rule.run(session, iden)
            if result is not None:
                logger.info("Success get %s's email %s with %s, %s", iden, result, repr(self), repr(rule))
                return result
        return None

    def register_rules(self) -> None:
        if self.rules:
            return

        package = importlib.import_module(self.package_provider)
        for module_info in pkgutil.walk_packages(package.__path__, f'{self.package_provider}.'):
            module = importlib.import_module(module_info.name)
            logger.debug('Registering rules from module %s', module.__name__)

            for _, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, RuleBase) and obj is not RuleBase:
                    logger.debug('Registering rule from rule %s', obj.__name__)
                    self.rules.append(obj(self.base_url))

        # make sure rule keep in manual order
        self.rules.sort(key=lambda x: x.name)
