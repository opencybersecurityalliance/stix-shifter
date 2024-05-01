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


class HTTPLogError(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "detail": (str,),
            "status": (str,),
            "title": (str,),
        }

    attribute_map = {
        "detail": "detail",
        "status": "status",
        "title": "title",
    }

    def __init__(
        self_,
        detail: Union[str, UnsetType] = unset,
        status: Union[str, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        List of errors.

        :param detail: Error message.
        :type detail: str, optional

        :param status: Error code.
        :type status: str, optional

        :param title: Error title.
        :type title: str, optional
        """
        if detail is not unset:
            kwargs["detail"] = detail
        if status is not unset:
            kwargs["status"] = status
        if title is not unset:
            kwargs["title"] = title
        super().__init__(kwargs)
