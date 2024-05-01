# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    date,
    datetime,
    none_type,
    unset,
    UnsetType,
)


class SyntheticsAssertionJSONPathTargetTarget(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "json_path": (str,),
            "operator": (str,),
            "target_value": (
                bool,
                date,
                datetime,
                dict,
                float,
                int,
                list,
                str,
                none_type,
            ),
        }

    attribute_map = {
        "json_path": "jsonPath",
        "operator": "operator",
        "target_value": "targetValue",
    }

    def __init__(
        self_,
        json_path: Union[str, UnsetType] = unset,
        operator: Union[str, UnsetType] = unset,
        target_value: Union[Any, UnsetType] = unset,
        **kwargs,
    ):
        """
        Composed target for ``validatesJSONPath`` operator.

        :param json_path: The JSON path to assert.
        :type json_path: str, optional

        :param operator: The specific operator to use on the path.
        :type operator: str, optional

        :param target_value: The path target value to compare to.
        :type target_value: bool, date, datetime, dict, float, int, list, str, none_type, optional
        """
        if json_path is not unset:
            kwargs["json_path"] = json_path
        if operator is not unset:
            kwargs["operator"] = operator
        if target_value is not unset:
            kwargs["target_value"] = target_value
        super().__init__(kwargs)
