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


class GroupScalarColumn(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "name": (str,),
            "type": (str,),
            "values": ([[str]],),
        }

    attribute_map = {
        "name": "name",
        "type": "type",
        "values": "values",
    }

    def __init__(
        self_,
        name: Union[str, UnsetType] = unset,
        type: Union[str, UnsetType] = unset,
        values: Union[List[List[str]], UnsetType] = unset,
        **kwargs,
    ):
        """
        A column containing the tag keys and values in a group.

        :param name: The name of the tag key or group.
        :type name: str, optional

        :param type: The type of column present.
        :type type: str, optional

        :param values: The array of tag values for each group found for the results of the formulas or queries.
        :type values: [[str]], optional
        """
        if name is not unset:
            kwargs["name"] = name
        if type is not unset:
            kwargs["type"] = type
        if values is not unset:
            kwargs["values"] = values
        super().__init__(kwargs)
