import logging as logger
import os

import requests
from dotenv import load_dotenv

from src.hosts_config import API_HOSTS

load_dotenv()


class RequestUtilities:
    def __init__(self):
        self.__env = os.getenv("ENV", "test")
        self.base_url: str = API_HOSTS[self.__env]

        self.status_code: int | None = None
        self.expected_status_code: int | None = None
        self.url: str | None = None

        self.response_api = None
        self.response_json = None

        self.EMPTY_CONTENT_LENGTH = "0"

    def __assert_status_code(self):
        logger.debug("Status code check.")
        assert self.status_code == self.expected_status_code, (
            f"Bad status code. Expected status code: {self.expected_status_code}, "
            f"actual status code: {self.status_code}"
        )
        logger.debug(f"Status is {self.status_code}")

    def get(self, endpoint: str, headers: dict | None = None, expected_status_code=200):
        logger.debug("Starting GET method.")

        if not headers:
            headers = {"Content-Type": "application/json"}
        else:
            headers.update({"Content-Type": "application/json"})

        self.url = self.base_url + endpoint
        logger.debug(f"URL: {self.url}")

        self.expected_status_code = expected_status_code

        self.response_api = requests.get(
            url=self.url,
            headers=headers,
        )
        self.status_code = self.response_api.status_code
        self.__assert_status_code()

        if self.response_api.headers.get("Content-Length") == self.EMPTY_CONTENT_LENGTH:
            logger.debug("Response has empty body (Content-Length: 0)")
            return self.response_api

        self.response_json = self.response_api.json()

        logger.debug(f"GET API response {self.response_json}")

        return self.response_json

    def post(
            self,
            endpoint: str,
            payload: dict | None = None,
            headers: dict | None = None,
            expected_status_code=200,
    ):
        logger.debug("Starting POST method.")

        if not headers:
            headers = {"Content-Type": "application/json"}
        else:
            headers.update({"Content-Type": "application/json"})

        self.url = self.base_url + endpoint
        logger.debug(f"URL: {self.url}")

        self.expected_status_code = expected_status_code

        self.response_api = requests.post(
            url=self.url,
            json=payload,
            headers=headers,
        )

        self.status_code = self.response_api.status_code

        self.__assert_status_code()

        if self.response_api.headers.get("Content-Length") == self.EMPTY_CONTENT_LENGTH:
            logger.debug("Response has empty body (Content-Length: 0)")
            return self.response_api

        if payload is None:
            return self.response_api

        self.response_json = self.response_api.json()

        logger.debug(f"POST API response {self.response_json}")

        return self.response_json

    def patch(
            self,
            endpoint: str,
            payload: dict | None = None,
            headers: dict | None = None,
            expected_status_code=200,
    ):
        logger.debug("Starting PATCH method.")

        if not headers:
            headers = {"Content-Type": "application/json"}
        else:
            headers.update({"Content-Type": "application/json"})

        self.url = self.base_url + endpoint
        logger.debug(f"URL: {self.url}")

        self.expected_status_code = expected_status_code

        self.response_api = requests.patch(
            url=self.url,
            json=payload,
            headers=headers,
        )

        self.status_code = self.response_api.status_code

        self.__assert_status_code()

        if self.response_api.headers.get("Content-Length") == self.EMPTY_CONTENT_LENGTH:
            logger.debug("Response has empty body (Content-Length: 0)")
            return self.response_api

        if payload is None:
            return self.response_api

        self.response_json = self.response_api.json()

        logger.debug(f"PATCH API response {self.response_json}")

        return self.response_json

    def delete(
            self, endpoint: str, headers: dict | None = None, expected_status_code=200
    ):
        logger.debug("Starting DELETE method.")

        if not headers:
            headers = {"Content-Type": "application/json"}

        self.url = self.base_url + endpoint
        logger.debug(f"URL: {self.url}")

        self.expected_status_code = expected_status_code

        self.response_api = requests.delete(
            url=self.url,
            headers=headers,
        )
        self.status_code = self.response_api.status_code
        self.__assert_status_code()

        return self.response_api
