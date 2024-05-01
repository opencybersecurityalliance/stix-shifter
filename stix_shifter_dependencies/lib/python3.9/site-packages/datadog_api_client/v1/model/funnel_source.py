# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class FunnelSource(ModelSimple):
    """
    Source from which to query items to display in the funnel.

    :param value: If omitted defaults to "rum". Must be one of ["rum"].
    :type value: str
    """

    allowed_values = {
        "rum",
    }
    RUM: ClassVar["FunnelSource"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


FunnelSource.RUM = FunnelSource("rum")
