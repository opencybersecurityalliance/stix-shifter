# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.spans_metric_response_attributes import SpansMetricResponseAttributes
    from datadog_api_client.v2.model.spans_metric_type import SpansMetricType


class SpansMetricResponseData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.spans_metric_response_attributes import SpansMetricResponseAttributes
        from datadog_api_client.v2.model.spans_metric_type import SpansMetricType

        return {
            "attributes": (SpansMetricResponseAttributes,),
            "id": (str,),
            "type": (SpansMetricType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: Union[SpansMetricResponseAttributes, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        type: Union[SpansMetricType, UnsetType] = unset,
        **kwargs,
    ):
        """
        The span-based metric properties.

        :param attributes: The object describing a Datadog span-based metric.
        :type attributes: SpansMetricResponseAttributes, optional

        :param id: The name of the span-based metric.
        :type id: str, optional

        :param type: The type of resource. The value should always be spans_metrics.
        :type type: SpansMetricType, optional
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if id is not unset:
            kwargs["id"] = id
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
