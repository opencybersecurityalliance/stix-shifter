# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class RUMApplicationUpdateType(ModelSimple):
    """
    RUM application update type.

    :param value: If omitted defaults to "rum_application_update". Must be one of ["rum_application_update"].
    :type value: str
    """

    allowed_values = {
        "rum_application_update",
    }
    RUM_APPLICATION_UPDATE: ClassVar["RUMApplicationUpdateType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


RUMApplicationUpdateType.RUM_APPLICATION_UPDATE = RUMApplicationUpdateType("rum_application_update")
