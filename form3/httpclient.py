import os
import json
import urllib.parse
import requests
from typing import Union


class Error(Exception):
    pass


class NotFoundError(Error):
    pass


class JSONError(Error):
    pass


class APIError(Error):
    pass


class HTTPClient:
    def __init__(self):
        self._session = requests.Session()
        self.base_uri = os.getenv("API_ENDPOINT", "http://localhost:8080/v1/")
        self.timeout = 5
        self.headers = {"Content-type": "application/json"}

    def _make_request(
        self, url: str, action: str = "GET", payload: dict = None
    ) -> Union[dict, bool]:
        """
            Makes the HTTP request and handles errors and bad status codes.

            Returns True for a 204 response, and the JSON body response for
            other successful codes.
        """
        url = urllib.parse.urljoin(self.base_uri, url)

        if action == "GET":
            res = self._session.get(
                url, headers=self.headers, params=payload, timeout=self.timeout
            )
        elif action == "POST":
            res = self._session.post(
                url,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=self.timeout,
            )
        elif action == "DELETE":
            res = self._session.delete(
                url, headers=self.headers, params=payload, timeout=self.timeout,
            )

        if res.status_code == 204:
            return True

        if res.status_code == 404:
            raise NotFoundError()

        try:
            jsoned = res.json()
        except ValueError as e:
            raise JSONError(f"Failed to parse JSON response from API: {str(e)}")

        if not res.ok:
            msg = f"Error {res.status_code} from API"
            if "error_message" in jsoned:
                msg += f': {jsoned["error_message"]}'
            raise APIError(msg)

        return jsoned

    def get(self, endpoint: str, params: str = None) -> dict:
        """
            Makes a GET request, automagically handles pagination.

            Returns the JSON response.
        """
        jsoned = self._make_request(endpoint, action="GET", payload=params)
        data = jsoned["data"]

        # handle pagination
        while jsoned.get("links", {}).get("next"):
            # update query params
            parsed_next_url = urllib.parse.urlparse(jsoned["links"]["next"])
            parsed_next_query = urllib.parse.parse_qs(parsed_next_url.query)

            for key, value in parsed_next_query.items():
                params[key] = value

            jsoned = self._make_request(endpoint, action="GET", payload=params)
            data += jsoned["data"]

        return data

    def post(self, endpoint: str, data: str = None) -> Union[dict, bool]:
        return self._make_request(endpoint, action="POST", payload=data)

    def delete(self, endpoint: str, params: str = None) -> Union[dict, bool]:
        return self._make_request(endpoint, action="DELETE", payload=params)
