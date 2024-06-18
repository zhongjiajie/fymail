class FyMailError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"FyMailError::{self.__class__.__name__}: {self.message}"


class NoProviderNameError(FyMailError):
    message = "Provider name is required"

    def __init__(self):
        super().__init__(self.message)


class NoProviderPackageError(FyMailError):
    message = "Provider package path is required"

    def __init__(self):
        super().__init__(self.message)


class NoRuleNameError(FyMailError):
    message = "Rule name is required"

    def __init__(self):
        super().__init__(self.message)


class NoRuleUrlPathError(FyMailError):
    message = "Rule Path is required"

    def __init__(self):
        super().__init__(self.message)


class NoProviderBaseUrlPathError(FyMailError):
    message = "Provider base path is required"

    def __init__(self):
        super().__init__(self.message)


class ProvideNotExistsError(FyMailError):
    def __init__(self, *, provider_name):
        self.message = f"Provider {provider_name} not exists"
        super().__init__(self.message)
