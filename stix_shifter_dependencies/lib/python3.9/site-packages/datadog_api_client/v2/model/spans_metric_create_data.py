# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.spans_metric_create_attributes import SpansMetricCreateAttributes
    from datadog_api_client.v2.model.spans_metric_type import SpansMetricType


class SpansMetricCreateData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.spans_metric_create_attributes import SpansMetricCreateAttributes
        from datadog_api_client.v2.model.spans_metric_type import SpansMetricType

        return {
            "attributes": (SpansMetricCreateAttributes,),
            "id": (str,),
            "type": (SpansMetricType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(self_, attributes: SpansMetricCreateAttributes, id: str, type: SpansMetricType, **kwargs):
        """
        The new span-based metric properties.

        :param attributes: The object describing the Datadog span-based metric to create.
        :type attributes: SpansMetricCreateAttributes

        :param id: The name of the span-based metric.
        :type id: str

        :param type: The type of resource. The value should always be spans_metrics.
        :type type: SpansMetricType
        """
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.id = id
        self_.type = type
