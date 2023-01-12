"""himon package entry file."""
__version__ = "0.3.2"
__all__ = ["__version__", "get_cache_root"]

import os
from pathlib import Path


def get_cache_root() -> Path:
    """
    Create and return the path to the cache for Himon, supports XDG_CACHE_HOME env.

    Returns:
        The path to the Himon cache folder.
    """
    cache_home = os.getenv("XDG_CACHE_HOME", default=str(Path.home() / ".cache"))
    folder = Path(cache_home).resolve() / "simyan"
    folder.mkdir(parents=True, exist_ok=True)
    return folder
