# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class HourlyUsageType(ModelSimple):
    """
    Usage type that is being measured.

    :param value: Must be one of ["app_sec_host_count", "observability_pipelines_bytes_processed", "lambda_traced_invocations_count"].
    :type value: str
    """

    allowed_values = {
        "app_sec_host_count",
        "observability_pipelines_bytes_processed",
        "lambda_traced_invocations_count",
    }
    APP_SEC_HOST_COUNT: ClassVar["HourlyUsageType"]
    OBSERVABILITY_PIPELINES_BYTES_PROCESSSED: ClassVar["HourlyUsageType"]
    LAMBDA_TRACED_INVOCATIONS_COUNT: ClassVar["HourlyUsageType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


HourlyUsageType.APP_SEC_HOST_COUNT = HourlyUsageType("app_sec_host_count")
HourlyUsageType.OBSERVABILITY_PIPELINES_BYTES_PROCESSSED = HourlyUsageType("observability_pipelines_bytes_processed")
HourlyUsageType.LAMBDA_TRACED_INVOCATIONS_COUNT = HourlyUsageType("lambda_traced_invocations_count")
