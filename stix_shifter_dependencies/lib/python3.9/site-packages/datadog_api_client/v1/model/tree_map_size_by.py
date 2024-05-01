# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class TreeMapSizeBy(ModelSimple):
    """
    (deprecated) The attribute formerly used to determine size in the widget.

    :param value: Must be one of ["pct_cpu", "pct_mem"].
    :type value: str
    """

    allowed_values = {
        "pct_cpu",
        "pct_mem",
    }
    PCT_CPU: ClassVar["TreeMapSizeBy"]
    PCT_MEM: ClassVar["TreeMapSizeBy"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


TreeMapSizeBy.PCT_CPU = TreeMapSizeBy("pct_cpu")
TreeMapSizeBy.PCT_MEM = TreeMapSizeBy("pct_mem")
