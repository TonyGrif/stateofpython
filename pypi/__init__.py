"""This module defines code for interacting with the PyPi JSON API

Attributes:
    PypiIndexClient: Client for interacting with the Index API
"""

from .index import PypiIndexClient
from .json import PypiJsonClient

__all__ = ["PypiIndexClient", "PypiJsonClient"]
