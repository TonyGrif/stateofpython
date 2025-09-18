"""This module defines the client for interacting with the PyPi Index API

Attributes:
    PypiIndexClient: Client for interacting with the Index API
"""

import httpx
from typing import Any, Dict, List, Optional


class PypiIndexClient:
    """
    A simple client for accessing the PyPi Index API.
    Docs: https://docs.pypi.org/api/index-api/
    """

    _BASE_URL = "https://pypi.org/simple/"
    _HEADERS = {"Accept": "application/vnd.pypi.simple.v1+json"}

    def __init__(self, client: Optional[httpx.Client] = None) -> None:
        """Constructor for the PyPI client

        Args:
            client: configured httpx client for connection pooling
        """
        self._external_client = client is not None
        self.client = client or httpx.Client()

    def __enter__(self) -> "PypiIndexClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if not self._external_client:
            self.client.close()

    def list_projects(self) -> List[str]:
        """Request the list of all available projects on PyPi

        Returns:
            List of repository names
        """
        response = self.client.get(self._BASE_URL, headers=self._HEADERS)
        response.raise_for_status()
        data: Dict[str, Any] = response.json()
        return [proj["name"] for proj in data.get("projects", [])]

    def project_files(self, project: str) -> List[str]:
        """Request a list of distribution file URLs for a specific project

        Args:
            project: pypi package name (case-insensitive)

        Returns:
            A list of URLs for distributions
        """
        response = self.client.get(f"{self._BASE_URL}{project}/", headers=self._HEADERS)
        response.raise_for_status()
        data: Dict[str, Any] = response.json()
        return [file["url"] for file in data.get("files", [])]
