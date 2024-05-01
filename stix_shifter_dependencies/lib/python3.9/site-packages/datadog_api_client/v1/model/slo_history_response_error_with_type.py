# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


class SLOHistoryResponseErrorWithType(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "error_message": (str,),
            "error_type": (str,),
        }

    attribute_map = {
        "error_message": "error_message",
        "error_type": "error_type",
    }

    def __init__(self_, error_message: str, error_type: str, **kwargs):
        """
        An object describing the error with error type and error message.

        :param error_message: A message with more details about the error.
        :type error_message: str

        :param error_type: Type of the error.
        :type error_type: str
        """
        super().__init__(kwargs)

        self_.error_message = error_message
        self_.error_type = error_type
