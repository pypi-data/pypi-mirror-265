# -*- coding: utf-8 -*-

from monkey.crawler.crawler import Crawler
import requests
from requests.auth import AuthBase
import json


class RESTAPICrawler(Crawler):

    def __init__(self, source_name: str, api_url: str, response_key_name: str, request_params: dict = None,
                 request_headers: dict = None, auth: AuthBase = None, default_offset: int = 0):
        super().__init__(source_name, default_offset)
        self.api_url = api_url
        self.response_key_name = response_key_name
        self.request_headers = request_headers if not None else {}
        self.request_params = request_params if not None else {}
        self.auth: AuthBase = auth

    def _build_get_request_url(self) -> str:
        return self.api_url

    def _get_records(self, offset: int = 0):
        response = requests.get(self.api_url, params=self.request_params, headers=self.request_headers, auth=self.auth)
        json_data = response.json()
        data = json.loads(json_data)
        return data[self.response_key_name]

    def _get_start_message(self):
        return f'Crawling {self.source_name} from {self.api_url}.'
