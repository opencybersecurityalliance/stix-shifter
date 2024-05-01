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
    from datadog_api_client.v2.model.logs_metric_update_data import LogsMetricUpdateData


class LogsMetricUpdateRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.logs_metric_update_data import LogsMetricUpdateData

        return {
            "data": (LogsMetricUpdateData,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: LogsMetricUpdateData, **kwargs):
        """
        The new log-based metric body.

        :param data: The new log-based metric properties.
        :type data: LogsMetricUpdateData
        """
        super().__init__(kwargs)

        self_.data = data
