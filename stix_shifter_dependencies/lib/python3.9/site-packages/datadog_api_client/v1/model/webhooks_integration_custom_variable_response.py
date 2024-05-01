# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class WebhooksIntegrationCustomVariableResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "is_secret": (bool,),
            "name": (str,),
            "value": (str,),
        }

    attribute_map = {
        "is_secret": "is_secret",
        "name": "name",
        "value": "value",
    }

    def __init__(self_, is_secret: bool, name: str, value: Union[str, UnsetType] = unset, **kwargs):
        """
        Custom variable for Webhook integration.

        :param is_secret: Make custom variable is secret or not.
            If the custom variable is secret, the value is not returned in the response payload.
        :type is_secret: bool

        :param name: The name of the variable. It corresponds with ``<CUSTOM_VARIABLE_NAME>``. It must only contains upper-case characters, integers or underscores.
        :type name: str

        :param value: Value of the custom variable. It won't be returned if the variable is secret.
        :type value: str, optional
        """
        if value is not unset:
            kwargs["value"] = value
        super().__init__(kwargs)

        self_.is_secret = is_secret
        self_.name = name
