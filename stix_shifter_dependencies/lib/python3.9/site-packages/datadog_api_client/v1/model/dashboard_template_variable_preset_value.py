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


class DashboardTemplateVariablePresetValue(ModelNormal):
    validations = {
        "values": {
            "min_items": 1,
        },
    }

    @cached_property
    def openapi_types(_):
        return {
            "name": (str,),
            "value": (str,),
            "values": ([str],),
        }

    attribute_map = {
        "name": "name",
        "value": "value",
        "values": "values",
    }

    def __init__(
        self_,
        name: Union[str, UnsetType] = unset,
        value: Union[str, UnsetType] = unset,
        values: Union[List[str], UnsetType] = unset,
        **kwargs,
    ):
        """
        Template variables saved views.

        :param name: The name of the variable.
        :type name: str, optional

        :param value: (deprecated) The value of the template variable within the saved view. Cannot be used in conjunction with ``values``. **Deprecated**.
        :type value: str, optional

        :param values: One or many template variable values within the saved view, which will be unioned together using ``OR`` if more than one is specified. Cannot be used in conjunction with ``value``.
        :type values: [str], optional
        """
        if name is not unset:
            kwargs["name"] = name
        if value is not unset:
            kwargs["value"] = value
        if values is not unset:
            kwargs["values"] = values
        super().__init__(kwargs)
