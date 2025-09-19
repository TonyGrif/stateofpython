"""This module defines the client for interacting with the PyPi JSON API

Attributes:
    PypiJsonClient: Client for interacting with the JSON API
"""

import httpx
from typing import Any, Dict, List, Optional


class PypiJsonClient:
    """
    A simple client for accessing the PyPi JSON API.
    Docs: https://docs.pypi.org/api/json/
    """

    _BASE_URL = "https://pypi.org/pypi"

    def __init__(self, client: Optional[httpx.Client] = None) -> None:
        """Constructor for the PyPi JSON client

        Args:
            client: configured httpx client for connection pooling
        """
        self._external_client = client is not None
        self.client = client or httpx.Client()

    def __enter__(self) -> "PypiJsonClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if not self._external_client:
            self.client.close()

    def project_info(self, project: str) -> Dict[str, Any]:
        """Request information and metadata about a project

        Args:
            project: package name on PyPi

        Returns:
            Dictionary containing project metadata and releases
        """
        response = self.client.get(f"{self._BASE_URL}/{project}/json")
        response.raise_for_status()
        return response.json()

    def release_info(self, project: str, version: str) -> Dict[str, Any]:
        """Request information about a specific release of a project

        Args:
            project: package name on PyPi
            version: specific release version string

        Returns:
            Dictionary containing release metadata
        """
        response = self.client.get(f"{self._BASE_URL}/{project}/{version}/json")
        response.raise_for_status()
        return response.json()

    def all_versions(self, project: str) -> List[str]:
        """Request all available versions for a project

        Args:
            project: package name on PyPi

        Returns:
            List of version strings
        """
        data = self.project_info(project)
        return list(data.get("releases", {}).keys())

    def latest_version(self, project: str) -> str:
        """Request the latest release version of a project

        Args:
            project: Package name on PyPi

        Returns:
            Latest version string
        """
        data = self.project_info(project)
        return data["info"]["version"]
