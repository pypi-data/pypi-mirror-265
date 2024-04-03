# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module for emitting and disabling warnings at top level.

"""
import warnings

import urllib3

from .exceptions import QbraidException
from .system import get_latest_package_version, get_local_package_version


def _warn_new_version(local: str, latest: str) -> bool:
    """Returns True if you should warn user about updated package version,
    False otherwise."""
    installed_major, installed_minor = map(int, local.split(".")[:2])
    latest_major, latest_minor = map(int, latest.split(".")[:2])

    return (installed_major, installed_minor) < (latest_major, latest_minor)


def _check_version(package: str) -> None:
    """Emits UserWarning if updated package version exists."""
    try:
        latest_version = get_latest_package_version(package)
        local_version = get_local_package_version(package)

        if _warn_new_version(local_version, latest_version):
            warnings.warn(
                f"You are using {package} version {local_version}, however, version "
                f"{latest_version} is available. To avoid compatibility issues, consider "
                "upgrading.",
                UserWarning,
            )
    except QbraidException:
        pass


# coverage: ignore
def _disable_urllib3() -> None:
    """Disables urllib3 InsecureRequestWarning warning."""
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
