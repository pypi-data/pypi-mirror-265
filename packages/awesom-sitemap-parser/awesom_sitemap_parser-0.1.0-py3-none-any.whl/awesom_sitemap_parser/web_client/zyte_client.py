"""requests-based implementation of web client class."""

import base64
from http import HTTPStatus
from typing import Optional

import requests

from awesom_sitemap_parser.web_client.abstract_client import (
    AbstractWebClient,
    AbstractWebClientResponse,
    AbstractWebClientSuccessResponse,
    WebClientErrorResponse,
    RETRYABLE_HTTP_STATUS_CODES,
)


class ZyteWebClientSuccessResponse(AbstractWebClientSuccessResponse):
    """
    zyte-based successful response.
    """

    __slots__ = ['__requests_response', ]

    def __init__(self, requests_response: requests.Response, max_response_data_length: Optional[int] = None):
        self.__max_response_data_length = max_response_data_length
        self.__requests_response = requests_response

    def status_code(self) -> int:
        return int(self.__requests_response.status_code)

    def status_message(self) -> str:
        message = self.__requests_response.reason
        if not message:
            message = HTTPStatus(self.status_code(), None).phrase
        return message

    @property
    def headers(self):
        return {i["name"]: i["value"] for i in self.__requests_response.json()["httpResponseHeaders"]}

    def header(self, case_insensitive_name: str) -> Optional[str]:
        return self.headers.get(case_insensitive_name.lower(), None)

    def raw_data(self) -> bytes:
        data = base64.b64decode(self.__requests_response.json()["httpResponseBody"])
        if self.__max_response_data_length:
            return data[:self.__max_response_data_length]

        return data


class ZyteWebClientErrorResponse(WebClientErrorResponse):
    """
    zyte-based error response.
    """
    pass


class ZyteWebClient(AbstractWebClient):
    """zyte-based web client to be used by the sitemap fetcher."""

    __slots__ = ['__timeout', ]

    def __init__(self, zyte_auth: str, timeout=60, max_response_data_length: int = None):
        self.__max_response_data_length = max_response_data_length
        self.__auth = zyte_auth
        self.__timeout = timeout

    def set_max_response_data_length(self, max_response_data_length: int) -> None:
        self.__max_response_data_length = max_response_data_length

    def get(self, url: str) -> AbstractWebClientResponse:
        try:
            response = requests.post(
                "https://api.zyte.com/v1/extract",
                auth=(self.__auth, ""),
                json={
                    "url": url,
                    "httpResponseBody": True,
                    "httpResponseHeaders": True,
                },
                timeout=self.__timeout
            )
            response.raise_for_status()
            response.headers.update({i["name"]: i["value"] for i in response.json()["httpResponseHeaders"]})


        except requests.exceptions.Timeout as ex:
            # Retryable timeouts
            return ZyteWebClientErrorResponse(message=str(ex), retryable=True)

        except requests.exceptions.RequestException as ex:
            # Other errors, e.g. redirect loops
            return ZyteWebClientErrorResponse(message=str(ex), retryable=False)

        else:

            if 200 <= response.status_code < 300:
                return ZyteWebClientSuccessResponse(
                    requests_response=response,
                    max_response_data_length=self.__max_response_data_length,
                )
            else:

                message = '{} {}'.format(response.status_code, response.reason)

                if response.status_code in RETRYABLE_HTTP_STATUS_CODES:
                    return ZyteWebClientErrorResponse(message=message, retryable=True)
                else:
                    return ZyteWebClientErrorResponse(message=message, retryable=False)
