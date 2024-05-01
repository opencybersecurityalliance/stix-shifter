# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class MetricIngestedIndexedVolumeType(ModelSimple):
    """
    The metric ingested and indexed volume type.

    :param value: If omitted defaults to "metric_volumes". Must be one of ["metric_volumes"].
    :type value: str
    """

    allowed_values = {
        "metric_volumes",
    }
    METRIC_VOLUMES: ClassVar["MetricIngestedIndexedVolumeType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


MetricIngestedIndexedVolumeType.METRIC_VOLUMES = MetricIngestedIndexedVolumeType("metric_volumes")
