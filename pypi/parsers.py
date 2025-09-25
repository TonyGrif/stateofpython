"""This module provides methods for parsing sections of a PyPi JSON response

Attributes:
    parse_classifiers: parse classifier tags from a List of values
"""

from typing import Dict, List


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
            * topic
    """
    data = {}

    data["development_status"] = [
        s.split("::")[-1].lstrip(" ") for s in response if "Development Status ::" in s
    ]
    data["environment"] = _handle_environment(
        [s for s in response if "Environment ::" in s]
    )
    data["intended_audience"] = [
        s.split("::")[-1].lstrip(" ") for s in response if "Intended Audience ::" in s
    ]
    data["license"] = [
        s.split("::")[-1].lstrip(" ") for s in response if "License ::" in s
    ]
    data["operating_system"] = [
        s.split("::")[-1].lstrip(" ") for s in response if "Operating System ::" in s
    ]
    data["topic"] = [s.split("::")[-1].lstrip(" ") for s in response if "Topic ::" in s]

    return data


def _handle_environment(data: List[str]) -> List[str]:
    return ["::".join(s.split("::")[1:]).lstrip(" ") for s in data]
