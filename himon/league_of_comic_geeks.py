"""The League of Comic Geeks module.

This module provides the following classes:

- LeagueOfComicGeeks
"""

__all__ = ["LeagueOfComicGeeks"]

import platform
from json import JSONDecodeError
from typing import Any, ClassVar, Final
from urllib.parse import urlencode

from httpx import Client, HTTPStatusError, RequestError, TimeoutException, codes
from pydantic import TypeAdapter, ValidationError
from pyrate_limiter import Duration, Limiter, Rate, SQLiteBucket

from himon import __version__
from himon.exceptions import AuthenticationError, RateLimitError, ServiceError
from himon.schemas.comic import Comic
from himon.schemas.generic import GenericComic
from himon.schemas.series import Series
from himon.sqlite_cache import SQLiteCache

# Constants
MINUTE_RATE: Final[int] = 20
SECONDS_PER_HOUR: Final[int] = 3_600
SECONDS_PER_MINUTE: Final[int] = 60


def rate_mapping(*args: Any, **kwargs: Any) -> tuple[str, int]:
    return "league_of_comic_geeks", 1


def format_time(seconds: str | float) -> str:
    """Format seconds into a verbose human-readable time string.

    Args:
        seconds (int or float): Number of seconds to format

    Returns:
        str: Formatted time string (e.g., "2 hours, 30 minutes, 45 seconds")
    """
    total_seconds = int(seconds)
    if total_seconds < 0:
        return "0 seconds"

    hours = total_seconds // SECONDS_PER_HOUR
    minutes = (total_seconds % SECONDS_PER_HOUR) // SECONDS_PER_MINUTE
    remaining_seconds = total_seconds % SECONDS_PER_MINUTE

    parts = []
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if remaining_seconds > 0 or not parts:
        parts.append(f"{remaining_seconds} second{'s' if remaining_seconds != 1 else ''}")
    return ", ".join(parts)


class LeagueOfComicGeeks:
    """Wrapper to allow calling League of Comic Geeks API endpoints.

    Args:
        client_id: User's Client Id to access League of Comic Geeks.
        client_secret: User's Client Secret to access League of Comic Geeks.
        access_token: User's Access Token to access League of Comic Geeks.
        timeout: Set how long requests will wait for a response (in seconds).
        cache: SQLiteCache to use if set.

    Attributes:
        cache (SQLiteCache | None): SQLiteCache to use if set.
        access_token (str | None): User's Access Token to access League of Comic Geeks.
    """

    _minute_rate = Rate(MINUTE_RATE, Duration.MINUTE)
    _rates: ClassVar[list[Rate]] = [_minute_rate]
    _bucket = SQLiteBucket.init_from_file(_rates)  # Save between sessions
    # Can a `BucketFullException` be raised when used as a decorator?
    _limiter = Limiter(_bucket, raise_when_fail=False, max_delay=Duration.DAY)
    decorator = _limiter.as_decorator()

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        access_token: str | None = None,
        timeout: float = 30,
        cache: SQLiteCache | None = None,
    ):
        self._client = Client(
            base_url="https://leagueofcomicgeeks.com/api",
            headers={
                "Accept": "application/json",
                "User-Agent": f"Himon/{__version__}/{platform.system()}: {platform.release()}",
                "X-API-CLIENT": client_id,
            },
            timeout=timeout,
        )
        self.cache = cache

        self._client_secret = client_secret
        self.access_token = access_token

    @decorator(rate_mapping)
    def _perform_get_request(
        self, endpoint: str, params: dict[str, str] | None = None
    ) -> dict[str, Any]:
        """Make GET request to League of Comic Geeks.

        Args:
            endpoint: The endpoint to request information from.
            params: Parameters to add to the request.

        Returns:
            Json response from League of Comic Geeks.

        Raises:
            RateLimitError: If the API rate limit is exceeded.
            ServiceError: If there is an issue with the request or response.
            AuthenticationError:
                If League of Comic Geeks returns with an invalid API Key or Client Id response.
        """
        if params is None:
            params = {}

        try:
            response = self._client.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except RequestError as err:
            raise ServiceError("Unable to connect to '%s'", err.request.url.path) from err
        except HTTPStatusError as err:
            if err.response.status_code == codes.FORBIDDEN:
                raise AuthenticationError("Invalid Access Token") from err
            if err.response.status_code == codes.NOT_FOUND:
                raise ServiceError("Unknown Endpoint") from err
            if err.response.status_code == codes.TOO_MANY_REQUESTS:
                period = format_time(err.response.headers["Retry-After"])
                raise RateLimitError("Too Many API Requests: Need to wait %s.", period) from err
            raise ServiceError(err) from err
        except JSONDecodeError as err:
            raise ServiceError("Unable to parse response from as Json") from err
        except TimeoutException as err:
            raise ServiceError("Service took too long to respond") from err

    def _get_request(
        self, endpoint: str, params: dict[str, str] | None = None, skip_cache: bool = False
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

        cache_params = f"?{urlencode(params)}" if params else ""
        cache_key = endpoint + cache_params

        if self.cache and not skip_cache:
            cached_response = self.cache.select(query=cache_key)
            if cached_response:
                return cached_response
        response = self._perform_get_request(endpoint=endpoint, params=params)
        if self.cache and not skip_cache:
            self.cache.insert(query=cache_key, response=response)
        return response

    @decorator(rate_mapping)
    def _str_get_request(self, endpoint: str, params: dict[str, str] | None = None) -> str:
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

        try:
            response = self._client.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except RequestError as err:
            raise ServiceError("Unable to connect to '%s'", err.request.url.path) from err
        except HTTPStatusError as err:
            if err.response.status_code == codes.FORBIDDEN:
                raise AuthenticationError("Invalid Access Token") from err
            if err.response.status_code == codes.NOT_FOUND:
                raise ServiceError("Unknown Endpoint") from err
            if err.response.status_code == codes.TOO_MANY_REQUESTS:
                period = format_time(err.response.headers["Retry-After"])
                raise RateLimitError("Too Many API Requests: Need to wait %s.", period) from err
            raise ServiceError(err) from err
        except JSONDecodeError as err:
            raise ServiceError("Unable to parse response from as Json") from err
        except TimeoutException as err:
            raise ServiceError("Service took too long to respond") from err

    def generate_access_token(self) -> str:
        """Request an access token.

        Returns:
            An access token.

        Raises:
            ServiceError: If there is an issue with the client id or secret.
        """
        if self._client_secret:
            self._client.headers["X-API-KEY"] = self._client_secret
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
            if self.access_token:
                self._client.headers["X-API-KEY"] = self.access_token
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
            if self.access_token:
                self._client.headers["X-API-KEY"] = self.access_token
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
            if self.access_token:
                self._client.headers["X-API-KEY"] = self.access_token
            result = self._get_request("/comic/format/json", params={"comic_id": str(comic_id)})
            return TypeAdapter(Comic).validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err
