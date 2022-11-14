import os
import dataclasses
import json
import typing

import keyring


@dataclasses.dataclass
class ApiCredential:
    apiKey: str
    secretKey: str


class CredentialManager:
    service_id = os.getenv('CREDENTIAL_MANAGER_SERVICE_ID', 'API_KEYS_STORAGE')

    @classmethod
    def set(cls, account: str, *, keys: ApiCredential):
        item = keyring.get_password(cls.service_id, account)
        if item is None:
            keyring.set_password(
                cls.service_id,
                account,
                json.dumps(dataclasses.asdict(keys))
            )

    @classmethod
    def get(cls, account: str) -> typing.Optional[ApiCredential]:
        keys = keyring.get_password(cls.service_id, account)
        if keys is not None:
            return ApiCredential(**json.loads(keys))

    @classmethod
    def remove(cls, account: str):
        keys = keyring.get_password(cls.service_id, account)
        if keys is not None:
            keyring.delete_password(cls.service_id, account)


__all__ = [
    'ApiCredential',
    'CredentialManager'
]
