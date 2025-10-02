"""This module provides methods for parsing sections of a PyPi JSON response

Attributes:
    parse_classifiers: parse classifier tags from a List of values
"""

from typing import Dict, List, Optional


# TODO: Programming Languages
# TODO: Frameworks
def parse_classifiers(response: List[str]) -> Dict[str, List[str]]:
    """Parse classifier tags from a List of values

    Args:
        response: List of all classifiers in the response

    Returns:
        A parsed dictionary containing the following keys if present:
            * development_status
            * environment
            * intended_audience
            * license
            * operating_system
            * programming_language
            * topic
    """
    data = {}

    data["development_status"] = _handle_dev_status(
        [
            s.split("::")[-1].lstrip(" ")
            for s in response
            if "Development Status ::" in s
        ]
    )
    data["environment"] = _handle_environment(
        [s for s in response if "Environment ::" in s]
    )
    data["intended_audience"] = _simple_null_check(
        [s.split("::")[-1].lstrip(" ") for s in response if "Intended Audience ::" in s]
    )
    data["license"] = _simple_null_check(
        [s.split("::")[-1].lstrip(" ") for s in response if "License ::" in s]
    )
    data["operating_system"] = _simple_null_check(
        [s.split("::")[-1].lstrip(" ") for s in response if "Operating System ::" in s]
    )

    data["programming_language"] = _handle_languages(
        [s for s in response if "Programming Language ::" in s]
    )
    data["topic"] = _simple_null_check(
        [s.split("::")[-1].lstrip(" ") for s in response if "Topic ::" in s]
    )

    return data


def parse_keywords(response: Optional[str]) -> Optional[List]:
    """Parse the keywords of a repository

    Args:
        response: string text of all keywords

    Returns:
        List of keywords or an empty list
    """
    return (
        None if response is None else [word.lstrip(" ") for word in response.split(",")]
    )


def _handle_dev_status(data: List[str]) -> Optional[str]:
    return None if data == [] else data[0]


def _handle_environment(data: List[str]) -> Optional[List[str]]:
    data = ["::".join(s.split("::")[1:]).lstrip(" ") for s in data]
    return _simple_null_check(data)


def _handle_languages(data: List[str]) -> Optional[List[str]]:
    if _simple_null_check(data) is None:
        return None
    selection = [s.split("::")[1].strip(" ") for s in data]
    selection = list(set(selection))
    return selection


def _simple_null_check(data: List[str]) -> Optional[List[str]]:
    return None if data == [] else data
