# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SLOTypeNumeric(ModelSimple):
    """
    A numeric representation of the type of the service level objective (`0` for
        monitor, `1` for metric). Always included in service level objective responses.
        Ignored in create/update requests.

    :param value: Must be one of [0, 1].
    :type value: int
    """

    allowed_values = {
        0,
        1,
    }
    MONITOR: ClassVar["SLOTypeNumeric"]
    METRIC: ClassVar["SLOTypeNumeric"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (int,),
        }


SLOTypeNumeric.MONITOR = SLOTypeNumeric(0)
SLOTypeNumeric.METRIC = SLOTypeNumeric(1)
