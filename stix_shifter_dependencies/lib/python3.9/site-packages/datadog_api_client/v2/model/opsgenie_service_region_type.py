# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class OpsgenieServiceRegionType(ModelSimple):
    """
    The region for the Opsgenie service.

    :param value: Must be one of ["us", "eu", "custom"].
    :type value: str
    """

    allowed_values = {
        "us",
        "eu",
        "custom",
    }
    US: ClassVar["OpsgenieServiceRegionType"]
    EU: ClassVar["OpsgenieServiceRegionType"]
    CUSTOM: ClassVar["OpsgenieServiceRegionType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


OpsgenieServiceRegionType.US = OpsgenieServiceRegionType("us")
OpsgenieServiceRegionType.EU = OpsgenieServiceRegionType("eu")
OpsgenieServiceRegionType.CUSTOM = OpsgenieServiceRegionType("custom")
