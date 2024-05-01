# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    date,
    datetime,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.synthetics_assertion_operator import SyntheticsAssertionOperator
    from datadog_api_client.v1.model.synthetics_assertion_type import SyntheticsAssertionType


class SyntheticsAssertionTarget(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_assertion_operator import SyntheticsAssertionOperator
        from datadog_api_client.v1.model.synthetics_assertion_type import SyntheticsAssertionType

        return {
            "operator": (SyntheticsAssertionOperator,),
            "_property": (str,),
            "target": (
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
            "type": (SyntheticsAssertionType,),
        }

    attribute_map = {
        "operator": "operator",
        "_property": "property",
        "target": "target",
        "type": "type",
    }

    def __init__(
        self_,
        operator: SyntheticsAssertionOperator,
        target: Any,
        type: SyntheticsAssertionType,
        _property: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        An assertion which uses a simple target.

        :param operator: Assertion operator to apply.
        :type operator: SyntheticsAssertionOperator

        :param _property: The associated assertion property.
        :type _property: str, optional

        :param target: Value used by the operator.
        :type target: bool, date, datetime, dict, float, int, list, str, none_type

        :param type: Type of the assertion.
        :type type: SyntheticsAssertionType
        """
        if _property is not unset:
            kwargs["_property"] = _property
        super().__init__(kwargs)

        self_.operator = operator
        self_.target = target
        self_.type = type
