from typing import Optional, Any
import os
import requests
from stony.config import Config


class Client:
    def __init__(self, config: Config) -> None:
        self.config = config

    @property
    def api_url(self):
        return self.config.api_url

    def get_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def get_page(self, page_id: str) -> dict[str, Any]:
        url = self.api_url + f"/pages/{page_id}"
        headers = self.get_headers()
        resp = requests.get(url, headers=headers)
        return resp.json()

    def get_block(self, block_id: str) -> dict[str, Any]:
        url = self.api_url + f"/blocks/{block_id}/"
        headers = self.get_headers()
        resp = requests.get(url, headers=headers)
        return resp.json()

    def get_block_children(self, block_id: str) -> dict[str, Any]:
        url = self.api_url + f"/blocks/{block_id}/children"
        headers = self.get_headers()
        resp = requests.get(url, headers=headers)
        return resp.json()
