# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class AccessRole(ModelSimple):
    """
    The access role of the user. Options are **st** (standard user), **adm** (admin user), or **ro** (read-only user).

    :param value: If omitted defaults to "st". Must be one of ["st", "adm", "ro", "ERROR"].
    :type value: str
    """

    allowed_values = {
        "st",
        "adm",
        "ro",
        "ERROR",
    }
    STANDARD: ClassVar["AccessRole"]
    ADMIN: ClassVar["AccessRole"]
    READ_ONLY: ClassVar["AccessRole"]
    ERROR: ClassVar["AccessRole"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


AccessRole.STANDARD = AccessRole("st")
AccessRole.ADMIN = AccessRole("adm")
AccessRole.READ_ONLY = AccessRole("ro")
AccessRole.ERROR = AccessRole("ERROR")
