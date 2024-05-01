# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class LogsAPIError(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "code": (str,),
            "details": ([LogsAPIError],),
            "message": (str,),
        }

    attribute_map = {
        "code": "code",
        "details": "details",
        "message": "message",
    }

    def __init__(
        self_,
        code: Union[str, UnsetType] = unset,
        details: Union[List[LogsAPIError], UnsetType] = unset,
        message: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Error returned by the Logs API

        :param code: Code identifying the error
        :type code: str, optional

        :param details: Additional error details
        :type details: [LogsAPIError], optional

        :param message: Error message
        :type message: str, optional
        """
        if code is not unset:
            kwargs["code"] = code
        if details is not unset:
            kwargs["details"] = details
        if message is not unset:
            kwargs["message"] = message
        super().__init__(kwargs)
