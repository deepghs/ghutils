from base64 import b64encode
from functools import lru_cache

from nacl import encoding, public

from ..base import _ClientProxy


def _secret_value_encrypt(public_key: str, secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")


class ActionsSecretsClientProxy(_ClientProxy):
    def get_public_key(self, repository: str):
        return self._get(f'/repos/{repository}/actions/secrets/public-key')

    @lru_cache()
    def _get_cached_public_key(self, repository: str):
        return self.get_public_key(repository)

    def put_secret(self, repository: str, secret_name: str, secret_value: str):
        _public_key = self._get_cached_public_key(repository)
        key_id, key = _public_key['key_id'], _public_key['key']
        return self._put(
            f'https://api.github.com/repos/{repository}/actions/secrets/{secret_name}',
            json={
                "encrypted_value": _secret_value_encrypt(key, secret_value),
                "key_id": key_id
            },
            has_result=False
        )

    def delete_secret(self, repository: str, secret_name: str):
        return self._delete(
            f'https://api.github.com/repos/{repository}/actions/secrets/{secret_name}',
            has_result=False
        )
