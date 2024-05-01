# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class WebhooksIntegrationEncoding(ModelSimple):
    """
    Encoding type. Can be given either `json` or `form`.

    :param value: If omitted defaults to "json". Must be one of ["json", "form"].
    :type value: str
    """

    allowed_values = {
        "json",
        "form",
    }
    JSON: ClassVar["WebhooksIntegrationEncoding"]
    FORM: ClassVar["WebhooksIntegrationEncoding"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


WebhooksIntegrationEncoding.JSON = WebhooksIntegrationEncoding("json")
WebhooksIntegrationEncoding.FORM = WebhooksIntegrationEncoding("form")
