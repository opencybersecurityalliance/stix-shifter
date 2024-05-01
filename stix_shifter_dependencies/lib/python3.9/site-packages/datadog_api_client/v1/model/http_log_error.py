# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


class HTTPLogError(ModelNormal):
    validations = {
        "code": {
            "inclusive_maximum": 2147483647,
        },
    }

    @cached_property
    def openapi_types(_):
        return {
            "code": (int,),
            "message": (str,),
        }

    attribute_map = {
        "code": "code",
        "message": "message",
    }

    def __init__(self_, code: int, message: str, **kwargs):
        """
        Invalid query performed.

        :param code: Error code.
        :type code: int

        :param message: Error message.
        :type message: str
        """
        super().__init__(kwargs)

        self_.code = code
        self_.message = message
