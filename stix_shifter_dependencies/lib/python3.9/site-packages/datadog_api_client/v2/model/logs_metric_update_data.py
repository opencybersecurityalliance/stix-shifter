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
    from datadog_api_client.v2.model.logs_metric_update_attributes import LogsMetricUpdateAttributes
    from datadog_api_client.v2.model.logs_metric_type import LogsMetricType


class LogsMetricUpdateData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.logs_metric_update_attributes import LogsMetricUpdateAttributes
        from datadog_api_client.v2.model.logs_metric_type import LogsMetricType

        return {
            "attributes": (LogsMetricUpdateAttributes,),
            "type": (LogsMetricType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "type": "type",
    }

    def __init__(self_, attributes: LogsMetricUpdateAttributes, type: LogsMetricType, **kwargs):
        """
        The new log-based metric properties.

        :param attributes: The log-based metric properties that will be updated.
        :type attributes: LogsMetricUpdateAttributes

        :param type: The type of the resource. The value should always be logs_metrics.
        :type type: LogsMetricType
        """
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.type = type
