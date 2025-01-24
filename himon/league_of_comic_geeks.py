"""The League of Comic Geeks module.

This module provides the following classes:

- LeagueofComicGeeks
"""

__all__ = ["LeagueofComicGeeks"]

import platform
from typing import Any, Optional
from urllib.parse import urlencode

from pydantic import TypeAdapter, ValidationError
from ratelimit import limits, sleep_and_retry
from requests import get
from requests.exceptions import (
    ConnectionError,  # noqa: A004
    HTTPError,
    JSONDecodeError,
    ReadTimeout,
)

from himon import __version__
from himon.exceptions import AuthenticationError, ServiceError
from himon.schemas.comic import Comic
from himon.schemas.generic import GenericComic
from himon.schemas.series import Series
from himon.sqlite_cache import SQLiteCache

MINUTE = 60


class LeagueofComicGeeks:
    """Wrapper to allow calling League of Comic Geeks API endpoints.

    Args:
        client_id: User's Client Id to access League of Comic Geeks.
        client_secret: User's Client Secret to access League of Comic Geeks.
        access_token: User's Access Token to access League of Comic Geeks.
        timeout: Set how long requests will wait for a response (in seconds).
        cache: SQLiteCache to use if set.

    Attributes:
        headers (Dict[str, str]): Header used when requesting from League of Comic Geeks.
        timeout (int): How long requests will wait for a response (in seconds).
        cache (Optional[SQLiteCache]): SQLiteCache to use if set.
        client_secret (str): User's Client Secret to access League of Comic Geeks.
        access_token (Optional[str]): User's Access Token to access League of Comic Geeks.
    """

    API_URL = "https://leagueofcomicgeeks.com/api"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        access_token: Optional[str] = None,
        timeout: int = 30,
        cache: Optional[SQLiteCache] = None,
    ):
        self.headers = {
            "Accept": "application/json",
            "User-Agent": f"Himon/{__version__}/{platform.system()}: {platform.release()}",
            "X-API-CLIENT": client_id,
        }
        self.timeout = timeout
        self.cache = cache

        self.client_secret = client_secret
        self.access_token = access_token

    @sleep_and_retry
    @limits(calls=20, period=MINUTE)
    def _perform_get_request(
        self, url: str, params: Optional[dict[str, str]] = None
    ) -> dict[str, Any]:
        """Make GET request to League of Comic Geeks.

        Args:
            url: The url to request information from.
            params: Parameters to add to the request.

        Returns:
            Json response from League of Comic Geeks.

        Raises:
            ServiceError: If there is an issue with the request or response.
            AuthenticationError:
                If League of Comic Geeks returns with an invalid API Key or Client Id response.
        """
        if params is None:
            params = {}

        try:
            response = get(url, params=params, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except ConnectionError as err:
            raise ServiceError("Unable to connect to '%s'", url) from err
        except HTTPError as err:
            if err.response.status_code == 403:
                raise AuthenticationError("Invalid Access Token") from err
            if err.response.status_code == 404:
                raise ServiceError("Unknown Endpoint") from err
            raise ServiceError("%s: %s", err.response.status_code, err.response.text) from err
        except JSONDecodeError as err:
            raise ServiceError("Unable to parse response from '%s' as Json", url) from err
        except ReadTimeout as err:
            raise ServiceError("Service took too long to respond") from err

    def _get_request(
        self, endpoint: str, params: Optional[dict[str, str]] = None, skip_cache: bool = False
    ) -> dict[str, Any]:
        """Check cache or make GET request to League of Comic Geeks.

        Args:
            endpoint: The endpoint to request information from.
            params: Parameters to add to the request.
            skip_cache: Don't save or read from the cache.

        Returns:
            Json response from League of Comic Geeks.

        Raises:
            ServiceError: If there is an issue with the request or response.
            AuthenticationError:
                If League of Comic Geeks returns with an invalid API Key or Client Id response.
        """
        if params is None:
            params = {}

        url = self.API_URL + endpoint
        cache_params = f"?{urlencode(params)}" if params else ""
        cache_key = f"{url}{cache_params}"

        if self.cache and not skip_cache and (cached_response := self.cache.select(cache_key)):
            return cached_response

        response = self._perform_get_request(url=url, params=params)

        if self.cache and not skip_cache:
            self.cache.insert(cache_key, response)

        return response

    @sleep_and_retry
    @limits(calls=20, period=MINUTE)
    def _str_get_request(self, endpoint: str, params: Optional[dict[str, str]] = None) -> str:
        """Make GET request to League of Comic Geeks, expecting a str response.

        Args:
            endpoint: The endpoint to request information from.
            params: Parameters to add to the request.

        Returns:
            String response from League of Comic Geeks.

        Raises:
            ServiceError: If there is an issue with the request or response.
            AuthenticationError:
                If League of Comic Geeks returns with an invalid API Key or Client Id response.
        """
        if params is None:
            params = {}

        url = self.API_URL + endpoint

        try:
            response = get(url, params=params, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except ConnectionError as err:
            raise ServiceError("Unable to connect to '%s'", url) from err
        except HTTPError as err:
            if err.response.status_code == 403:
                raise AuthenticationError("Invalid Access Token") from err
            if err.response.status_code == 404:
                raise ServiceError("Unknown endpoint") from err
            raise ServiceError("%s: %s", err.response.status_code, err.response.text) from err
        except JSONDecodeError as err:
            raise ServiceError("Unable to parse response from '%s' as Json") from err
        except ReadTimeout as err:
            raise ServiceError("Service took too long to respond") from err

    def generate_access_token(self) -> str:
        """Request an access token.

        Returns:
            An access token.

        Raises:
            ServiceError: If there is an issue with the client id or secret.
        """
        self.headers["X-API-KEY"] = self.client_secret
        return self._str_get_request("/authorize/format/json")

    def search(self, search_term: str) -> list[GenericComic]:
        """Request a list of search results.

        Args:
            search_term: Search query string
        Returns:
            A list of results.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            self.headers["X-API-KEY"] = self.access_token
            results = self._get_request("/search/format/json", params={"query": search_term})
            return TypeAdapter(list[GenericComic]).validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_series(self, series_id: int) -> Series:
        """Request data for a Series based on its id.

        Args:
            series_id: The Series id.

        Returns:
            A Series object.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            self.headers["X-API-KEY"] = self.access_token
            result = self._get_request("/series/format/json", params={"series_id": str(series_id)})
            if "details" in result:
                result = result["details"]
            return TypeAdapter(Series).validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_comic(self, comic_id: int) -> Comic:
        """Request data for a Comic based on its id.

        Args:
            comic_id: The Comic id.

        Returns:
            A Comic object.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            self.headers["X-API-KEY"] = self.access_token
            result = self._get_request("/comic/format/json", params={"comic_id": str(comic_id)})
            return TypeAdapter(Comic).validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err
