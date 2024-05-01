# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class TreeMapGroupBy(ModelSimple):
    """
    (deprecated) The attribute formerly used to group elements in the widget.

    :param value: Must be one of ["user", "family", "process"].
    :type value: str
    """

    allowed_values = {
        "user",
        "family",
        "process",
    }
    USER: ClassVar["TreeMapGroupBy"]
    FAMILY: ClassVar["TreeMapGroupBy"]
    PROCESS: ClassVar["TreeMapGroupBy"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


TreeMapGroupBy.USER = TreeMapGroupBy("user")
TreeMapGroupBy.FAMILY = TreeMapGroupBy("family")
TreeMapGroupBy.PROCESS = TreeMapGroupBy("process")
