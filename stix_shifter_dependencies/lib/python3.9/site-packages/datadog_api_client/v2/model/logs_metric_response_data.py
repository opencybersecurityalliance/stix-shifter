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
    from datadog_api_client.v2.model.logs_metric_response_attributes import LogsMetricResponseAttributes
    from datadog_api_client.v2.model.logs_metric_type import LogsMetricType


class LogsMetricResponseData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.logs_metric_response_attributes import LogsMetricResponseAttributes
        from datadog_api_client.v2.model.logs_metric_type import LogsMetricType

        return {
            "attributes": (LogsMetricResponseAttributes,),
            "id": (str,),
            "type": (LogsMetricType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: Union[LogsMetricResponseAttributes, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        type: Union[LogsMetricType, UnsetType] = unset,
        **kwargs,
    ):
        """
        The log-based metric properties.

        :param attributes: The object describing a Datadog log-based metric.
        :type attributes: LogsMetricResponseAttributes, optional

        :param id: The name of the log-based metric.
        :type id: str, optional

        :param type: The type of the resource. The value should always be logs_metrics.
        :type type: LogsMetricType, optional
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if id is not unset:
            kwargs["id"] = id
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
