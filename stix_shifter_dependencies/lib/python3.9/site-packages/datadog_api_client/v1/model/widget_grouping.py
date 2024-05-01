# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class WidgetGrouping(ModelSimple):
    """
    The kind of grouping to use.

    :param value: Must be one of ["check", "cluster"].
    :type value: str
    """

    allowed_values = {
        "check",
        "cluster",
    }
    CHECK: ClassVar["WidgetGrouping"]
    CLUSTER: ClassVar["WidgetGrouping"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


WidgetGrouping.CHECK = WidgetGrouping("check")
WidgetGrouping.CLUSTER = WidgetGrouping("cluster")
