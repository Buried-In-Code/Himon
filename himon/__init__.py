"""himon package entry file."""
__version__ = "0.2.0"
__all__ = ["__version__", "get_cache_root"]

from pathlib import Path


def get_cache_root() -> Path:
    """
    Create and return the path to the cache for Himon.

    Returns:
        The path to the Himon cache
    """
    folder = Path.home() / ".cache" / "himon"
    folder.mkdir(parents=True, exist_ok=True)
    return folder
