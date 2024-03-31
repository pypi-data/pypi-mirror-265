"""
STRING API client using httpx.
"""

__version__ = "0.1.0"

from typing import List

from .client import Client

__all__ = ["Client"]

DEFAULT_CALLER_IDENTITY = f"{__name__} {__version__}"


# def _build_url():
#     return httpx.URL()


# def _build_request():
#     return httpx.Request(method="POST", url=_build_url())


def map_identifiers(identifiers: List[str], species: int):
    with Client() as client:
        return client.get_string_ids(identifiers=identifiers, species=species)
