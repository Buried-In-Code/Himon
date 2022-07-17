import platform
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from pydantic import parse_obj_as
from ratelimit import limits, sleep_and_retry
from requests import get
from requests.exceptions import ConnectionError, HTTPError, JSONDecodeError, ReadTimeout

from himon import __version__
from himon.exceptions import AuthenticationError, ServiceError
from himon.schemas.comic import Comic
from himon.schemas.search_result import SearchResult
from himon.schemas.series import Series
from himon.sqlite_cache import SQLiteCache

MINUTE = 60


class LeagueofComicGeeks:
    API_URL = "https://leagueofcomicgeeks.com/api"

    def __init__(
        self, api_key: str, client_id: str, timeout: int = 30, cache: Optional[SQLiteCache] = None
    ):
        self.headers = {
            "Accept": "application/json",
            "User-Agent": f"Himon/{__version__}/{platform.system()}: {platform.release()}",
            "X-API-KEY": api_key,
            "X-API-CLIENT": client_id,
        }
        self.timeout = timeout
        self.cache = cache

    @sleep_and_retry
    @limits(calls=20, period=MINUTE)
    def _perform_get_request(self, url: str, params: Dict[str, str] = None) -> Dict[str, Any]:
        if params is None:
            params = {}

        try:
            response = get(url, params=params, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except ConnectionError:
            raise ServiceError(f"Unable to connect to `{url}`")
        except HTTPError as err:
            if err.response.status_code == 403:
                raise AuthenticationError("Invalid API Key")
            if err.response.status_code == 404:
                raise ServiceError("Unknown endpoint")
            raise ServiceError(f"{err.response.status_code}: {err.response.text}")
        except JSONDecodeError:
            raise ServiceError(f"Unable to parse response from `{url}` as Json")
        except ReadTimeout:
            raise ServiceError("Service took too long to respond")

    def _get_request(
        self, endpoint: str, params: Dict[str, str] = None, skip_cache: bool = False
    ) -> Dict[str, Any]:
        if params is None:
            params = {}

        url = self.API_URL + endpoint
        cache_params = f"?{urlencode(params)}" if params else ""
        cache_key = f"{url}{cache_params}"

        if self.cache and not skip_cache:
            cached_response = self.cache.select(cache_key)
            if cached_response:
                return cached_response

        response = self._perform_get_request(url=url, params=params)

        if self.cache and not skip_cache:
            self.cache.insert(cache_key, response)

        return response

    def search(self, search_term: str) -> List[SearchResult]:
        results = self._get_request("/search/format/json", params={"query": search_term})
        return parse_obj_as(List[SearchResult], results)

    def series(self, series_id: int) -> Optional[Series]:
        result = self._get_request("/series/format/json", params={"series_id": str(series_id)})
        if "details" in result:
            result = result["details"]
        return parse_obj_as(Series, result)

    def comic(self, comic_id: int) -> Optional[Comic]:
        result = self._get_request("/comic/format/json", params={"comic_id": str(comic_id)})
        return parse_obj_as(Comic, result)
