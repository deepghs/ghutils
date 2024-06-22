from functools import lru_cache

from .secrets import ActionsSecretsClientProxy
from ..base import _ClientProxy


class ActionsClientProxy(_ClientProxy):
    @property
    @lru_cache()
    def secrets(self) -> ActionsSecretsClientProxy:
        return ActionsSecretsClientProxy(self)
