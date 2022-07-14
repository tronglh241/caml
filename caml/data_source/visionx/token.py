import requests
from __future__ import annotations

KEYCLOAK_TOKEN_URL = 'https://keys.smart-data.ml/auth/realms/vinai/protocol/openid-connect/token'
GRANT_TYPE = 'password'
CLIENT_ID = 'sd-client'
CLIENT_SECRET = 'c5248237-adac-43dd-8e27-726e4d5e6c79'


class Token:
    def __init__(
        self,
        access_token: str,
        expires_in: str,
        refresh_expires_in: str,
        refresh_token: str,
    ):
        super(Token, self).__init__()
        self.access_token = access_token
        self.expires_in = expires_in
        self.refresh_expires_in = refresh_expires_in
        self.refresh_token = refresh_token

    def get(self) -> str:
        return self.access_token

    @classmethod
    def request(
        cls,
        username: str,
        password: str,
    ) -> Token:
        res = requests.post(
            url=KEYCLOAK_TOKEN_URL,
            data={
                'username': username,
                'password': password,
                'client_id': CLIENT_ID,
                'grant_type': GRANT_TYPE,
                'client_secret': CLIENT_SECRET,
            },
        )
        res.raise_for_status()
        data = res.json()

        return cls(
            access_token=data['access_token'],
            expires_in=data['expires_in'],
            refresh_expires_in=data['refresh_expires_in'],
            refresh_token=data['refresh_token'],
        )
