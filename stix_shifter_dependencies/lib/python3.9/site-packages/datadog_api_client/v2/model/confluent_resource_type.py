# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class ConfluentResourceType(ModelSimple):
    """
    The JSON:API type for this request.

    :param value: If omitted defaults to "confluent-cloud-resources". Must be one of ["confluent-cloud-resources"].
    :type value: str
    """

    allowed_values = {
        "confluent-cloud-resources",
    }
    CONFLUENT_CLOUD_RESOURCES: ClassVar["ConfluentResourceType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


ConfluentResourceType.CONFLUENT_CLOUD_RESOURCES = ConfluentResourceType("confluent-cloud-resources")
