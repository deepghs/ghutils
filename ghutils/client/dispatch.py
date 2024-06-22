from functools import lru_cache
from typing import Optional

from .actions import ActionsClientProxy
from .base import _BaseClient


class GithubClient(_BaseClient):
    def __init__(self, token: Optional[str] = None):
        _BaseClient.__init__(self, token)

    def whoami(self):
        return self._get('/user')

    @property
    @lru_cache()
    def actions(self):
        return ActionsClientProxy(self)
