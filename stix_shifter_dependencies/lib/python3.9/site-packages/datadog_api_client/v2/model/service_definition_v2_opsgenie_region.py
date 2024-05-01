# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class ServiceDefinitionV2OpsgenieRegion(ModelSimple):
    """
    Opsgenie instance region.

    :param value: Must be one of ["US", "EU"].
    :type value: str
    """

    allowed_values = {
        "US",
        "EU",
    }
    US: ClassVar["ServiceDefinitionV2OpsgenieRegion"]
    EU: ClassVar["ServiceDefinitionV2OpsgenieRegion"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


ServiceDefinitionV2OpsgenieRegion.US = ServiceDefinitionV2OpsgenieRegion("US")
ServiceDefinitionV2OpsgenieRegion.EU = ServiceDefinitionV2OpsgenieRegion("EU")
