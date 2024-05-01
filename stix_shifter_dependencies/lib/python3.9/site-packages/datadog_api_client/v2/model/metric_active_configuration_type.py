# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class MetricActiveConfigurationType(ModelSimple):
    """
    The metric actively queried configuration resource type.

    :param value: If omitted defaults to "actively_queried_configurations". Must be one of ["actively_queried_configurations"].
    :type value: str
    """

    allowed_values = {
        "actively_queried_configurations",
    }
    ACTIVELY_QUERIED_CONFIGURATIONS: ClassVar["MetricActiveConfigurationType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


MetricActiveConfigurationType.ACTIVELY_QUERIED_CONFIGURATIONS = MetricActiveConfigurationType(
    "actively_queried_configurations"
)
