from typing import Dict, Optional
from urllib.parse import urljoin

import requests

from ..utils import get_session


class _ClientLikeObject:
    def _get(self, url, params: Optional[Dict[str, str]] = None,
             return_response: bool = False, has_result: bool = True, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def _put(self, url, json=None, return_response: bool = False, has_result: bool = True, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def _delete(self, url, return_response: bool = False, has_result: bool = True, **kwargs):
        raise NotImplementedError  # pragma: no cover


class _BaseClient(_ClientLikeObject):
    __endpoint__ = 'https://api.github.com'

    def __init__(self, token: Optional[str] = None):
        self._session = get_session()
        headers = {
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
        }
        if token:
            headers['Authorization'] = f'Bearer {token}'
        self._session.headers.update(headers)

    def _resp_postprocess(self, resp: requests.Response, return_response: bool = False, has_result: bool = True):
        if not return_response:
            resp.raise_for_status()
            if has_result:
                return resp.json()
        else:
            return resp

    def _get(self, url, params: Optional[Dict[str, str]] = None,
             return_response: bool = False, has_result: bool = True, **kwargs):
        resp = self._session.get(urljoin(self.__endpoint__, url), params=params, **kwargs)
        return self._resp_postprocess(resp, return_response=return_response, has_result=has_result)

    def _put(self, url, json=None, return_response: bool = False, has_result: bool = True, **kwargs):
        resp = self._session.put(urljoin(self.__endpoint__, url), json=json or {}, **kwargs)
        return self._resp_postprocess(resp, return_response=return_response, has_result=has_result)

    def _delete(self, url, return_response: bool = False, has_result: bool = True, **kwargs):
        resp = self._session.delete(urljoin(self.__endpoint__, url), **kwargs)
        return self._resp_postprocess(resp, return_response=return_response, has_result=has_result)


class _ClientProxy(_ClientLikeObject):
    def __init__(self, parent: _ClientLikeObject):
        self._parent = parent

    def _get(self, url, params: Optional[Dict[str, str]] = None,
             return_response: bool = False, has_result: bool = True, **kwargs):
        return self._parent._get(
            url=url,
            params=params,
            return_response=return_response,
            has_result=has_result,
            **kwargs,
        )

    def _put(self, url, json=None, return_response: bool = False, has_result: bool = True, **kwargs):
        return self._parent._put(
            url=url,
            json=json,
            return_response=return_response,
            has_result=has_result,
            **kwargs,
        )

    def _delete(self, url, return_response: bool = False, has_result: bool = True, **kwargs):
        return self._parent._delete(
            url=url,
            return_response=return_response,
            has_result=has_result,
            **kwargs,
        )
