# -*- coding: utf-8 -*-#

from uuid import uuid4
from .gsuite import GSuiteClient


class GSuiteChannelGenerator:
    def __init__(self, client: GSuiteClient):
        self._client = client

    def create_channel(
        self, url: str, domain: str, event: str, time_to_live: int
    ) -> None:
        param = {
            "domain": domain,
            "event": event,
            "body": {
                "type": "web_hook",
                "id": str(uuid4()),
                "address": url,
                "params": {"ttl": time_to_live},
            },
        }
        self._client.user_service.watch(**param).execute()
