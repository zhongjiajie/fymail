import importlib
import inspect
import pkgutil


from fymail.error import ProvideNotExistsError
from fymail.providers.base.provider_base import ProviderBase
import logging

logger = logging.getLogger(__name__)


class ProviderManger:
    providers = {}

    package_provider = "fymail.providers"
    skip_modules = ["base"]

    def register_plugin(self) -> None:
        package = importlib.import_module(self.package_provider)
        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            if module_name in self.skip_modules:
                continue

            logger.debug("Trying register provider from module %s", module_name)
            module = importlib.import_module(f"{self.package_provider}.{module_name}")
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, ProviderBase):
                    logger.debug("Registering provider from %s", obj.__name__)
                    self.providers[name.lower()] = obj()

    def get_provider(self, provider: str) -> ProviderBase:
        provider = provider.lower()
        if provider not in self.providers:
            raise ProvideNotExistsError(provider_name=provider)
        return self.providers[provider]
