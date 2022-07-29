from __future__ import annotations

import os
import time

import requests

GRANT_TYPE_PASSWORD = 'password'
GRANT_TYPE_REFRESH_TOKEN = 'refresh_token'
KEYCLOAK_TOKEN_URL = os.getenv(
    'KEYCLOAK_TOKEN_URL',
    'https://keys.smart-data.ml/auth/realms/vinai/protocol/openid-connect/token',
)
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


class Token:
    def __init__(
        self,
        access_token: str,
        expires_in: int,
        refresh_expires_in: int,
        refresh_token: str,
        request_time: float,
    ):
        super(Token, self).__init__()
        self.access_token = access_token
        self.expires_in = expires_in
        self.refresh_expires_in = refresh_expires_in
        self.refresh_token = refresh_token
        self.request_time = request_time

    def get(self) -> str:
        if self.expired:
            self.refresh()

        return self.access_token

    @property
    def expired(self) -> bool:
        return time.time() - self.request_time > self.expires_in * 0.5

    def refresh(self) -> None:
        if time.time() - self.request_time > self.refresh_expires_in:
            raise RuntimeError('Token expired.')

        request_time = time.time()
        res = requests.post(
            url=KEYCLOAK_TOKEN_URL,
            data={
                'client_id': CLIENT_ID,
                'grant_type': GRANT_TYPE_REFRESH_TOKEN,
                'client_secret': CLIENT_SECRET,
                'refresh_token': self.refresh_token,
            },
        )
        res.raise_for_status()
        data = res.json()

        self.access_token = data['access_token']
        self.expires_in = data['expires_in']
        self.refresh_expires_in = data['refresh_expires_in']
        self.refresh_token = data['refresh_token']
        self.request_time = request_time

    @classmethod
    def request(
        cls,
        username: str,
        password: str,
    ) -> Token:
        request_time = time.time()
        res = requests.post(
            url=KEYCLOAK_TOKEN_URL,
            data={
                'username': username,
                'password': password,
                'client_id': CLIENT_ID,
                'grant_type': GRANT_TYPE_PASSWORD,
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
            request_time=request_time,
        )
