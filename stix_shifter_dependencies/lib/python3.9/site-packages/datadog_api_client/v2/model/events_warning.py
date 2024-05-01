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


class EventsWarning(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "code": (str,),
            "detail": (str,),
            "title": (str,),
        }

    attribute_map = {
        "code": "code",
        "detail": "detail",
        "title": "title",
    }

    def __init__(
        self_,
        code: Union[str, UnsetType] = unset,
        detail: Union[str, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        A warning message indicating something is wrong with the query.

        :param code: A unique code for this type of warning.
        :type code: str, optional

        :param detail: A detailed explanation of this specific warning.
        :type detail: str, optional

        :param title: A short human-readable summary of the warning.
        :type title: str, optional
        """
        if code is not unset:
            kwargs["code"] = code
        if detail is not unset:
            kwargs["detail"] = detail
        if title is not unset:
            kwargs["title"] = title
        super().__init__(kwargs)
