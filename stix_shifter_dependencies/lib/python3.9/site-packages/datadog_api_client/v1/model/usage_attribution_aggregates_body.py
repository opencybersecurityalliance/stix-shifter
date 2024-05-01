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


class UsageAttributionAggregatesBody(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "agg_type": (str,),
            "field": (str,),
            "value": (float,),
        }

    attribute_map = {
        "agg_type": "agg_type",
        "field": "field",
        "value": "value",
    }

    def __init__(
        self_,
        agg_type: Union[str, UnsetType] = unset,
        field: Union[str, UnsetType] = unset,
        value: Union[float, UnsetType] = unset,
        **kwargs,
    ):
        """
        The object containing the aggregates.

        :param agg_type: The aggregate type.
        :type agg_type: str, optional

        :param field: The field.
        :type field: str, optional

        :param value: The value for a given field.
        :type value: float, optional
        """
        if agg_type is not unset:
            kwargs["agg_type"] = agg_type
        if field is not unset:
            kwargs["field"] = field
        if value is not unset:
            kwargs["value"] = value
        super().__init__(kwargs)
