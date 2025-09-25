"""This module contains clients for interacting with the PyPi APIs

Attributes:
    PypiIndexClient: Client for interacting with the Index API
    PypiJsonClient: Client for interacting with the JSON API
"""

from .index import PypiIndexClient
from .json import PypiJsonClient

__all__ = ["PypiIndexClient", "PypiJsonClient"]
