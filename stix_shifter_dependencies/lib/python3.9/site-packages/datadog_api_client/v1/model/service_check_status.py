# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class ServiceCheckStatus(ModelSimple):
    """
    The status of a service check. Set to `0` for OK, `1` for warning, `2` for critical, and `3` for unknown.

    :param value: Must be one of [0, 1, 2, 3].
    :type value: int
    """

    allowed_values = {
        0,
        1,
        2,
        3,
    }
    OK: ClassVar["ServiceCheckStatus"]
    WARNING: ClassVar["ServiceCheckStatus"]
    CRITICAL: ClassVar["ServiceCheckStatus"]
    UNKNOWN: ClassVar["ServiceCheckStatus"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (int,),
        }


ServiceCheckStatus.OK = ServiceCheckStatus(0)
ServiceCheckStatus.WARNING = ServiceCheckStatus(1)
ServiceCheckStatus.CRITICAL = ServiceCheckStatus(2)
ServiceCheckStatus.UNKNOWN = ServiceCheckStatus(3)
