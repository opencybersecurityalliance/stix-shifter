# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.incident_field_attributes_value_type import IncidentFieldAttributesValueType


class IncidentFieldAttributesMultipleValue(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_field_attributes_value_type import IncidentFieldAttributesValueType

        return {
            "type": (IncidentFieldAttributesValueType,),
            "value": ([str], none_type),
        }

    attribute_map = {
        "type": "type",
        "value": "value",
    }

    def __init__(
        self_,
        type: Union[IncidentFieldAttributesValueType, UnsetType] = unset,
        value: Union[List[str], none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        A field with potentially multiple values selected.

        :param type: Type of the multiple value field definitions.
        :type type: IncidentFieldAttributesValueType, optional

        :param value: The multiple values selected for this field.
        :type value: [str], none_type, optional
        """
        if type is not unset:
            kwargs["type"] = type
        if value is not unset:
            kwargs["value"] = value
        super().__init__(kwargs)
