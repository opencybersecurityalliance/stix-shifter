# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.incident_field_attributes_single_value_type import (
        IncidentFieldAttributesSingleValueType,
    )


class IncidentFieldAttributesSingleValue(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_field_attributes_single_value_type import (
            IncidentFieldAttributesSingleValueType,
        )

        return {
            "type": (IncidentFieldAttributesSingleValueType,),
            "value": (str, none_type),
        }

    attribute_map = {
        "type": "type",
        "value": "value",
    }

    def __init__(
        self_,
        type: Union[IncidentFieldAttributesSingleValueType, UnsetType] = unset,
        value: Union[str, none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        A field with a single value selected.

        :param type: Type of the single value field definitions.
        :type type: IncidentFieldAttributesSingleValueType, optional

        :param value: The single value selected for this field.
        :type value: str, none_type, optional
        """
        if type is not unset:
            kwargs["type"] = type
        if value is not unset:
            kwargs["value"] = value
        super().__init__(kwargs)
