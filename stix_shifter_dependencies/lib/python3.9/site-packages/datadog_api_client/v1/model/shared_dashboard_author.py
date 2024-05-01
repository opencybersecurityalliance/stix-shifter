# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


class SharedDashboardAuthor(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "handle": (str,),
            "name": (str, none_type),
        }

    attribute_map = {
        "handle": "handle",
        "name": "name",
    }
    read_only_vars = {
        "handle",
        "name",
    }

    def __init__(
        self_, handle: Union[str, UnsetType] = unset, name: Union[str, none_type, UnsetType] = unset, **kwargs
    ):
        """
        User who shared the dashboard.

        :param handle: Identifier of the user who shared the dashboard.
        :type handle: str, optional

        :param name: Name of the user who shared the dashboard.
        :type name: str, none_type, optional
        """
        if handle is not unset:
            kwargs["handle"] = handle
        if name is not unset:
            kwargs["name"] = name
        super().__init__(kwargs)
