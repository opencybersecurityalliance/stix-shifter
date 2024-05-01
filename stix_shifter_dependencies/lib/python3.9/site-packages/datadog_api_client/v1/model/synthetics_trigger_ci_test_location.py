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


class SyntheticsTriggerCITestLocation(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "id": (int,),
            "name": (str,),
        }

    attribute_map = {
        "id": "id",
        "name": "name",
    }

    def __init__(self_, id: Union[int, UnsetType] = unset, name: Union[str, UnsetType] = unset, **kwargs):
        """
        Synthetics location.

        :param id: Unique identifier of the location.
        :type id: int, optional

        :param name: Name of the location.
        :type name: str, optional
        """
        if id is not unset:
            kwargs["id"] = id
        if name is not unset:
            kwargs["name"] = name
        super().__init__(kwargs)
