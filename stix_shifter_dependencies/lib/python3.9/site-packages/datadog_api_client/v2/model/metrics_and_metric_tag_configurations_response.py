# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.metrics_and_metric_tag_configurations import MetricsAndMetricTagConfigurations
    from datadog_api_client.v2.model.metric import Metric
    from datadog_api_client.v2.model.metric_tag_configuration import MetricTagConfiguration


class MetricsAndMetricTagConfigurationsResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.metrics_and_metric_tag_configurations import MetricsAndMetricTagConfigurations

        return {
            "data": ([MetricsAndMetricTagConfigurations],),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(
        self_,
        data: Union[List[Union[MetricsAndMetricTagConfigurations, Metric, MetricTagConfiguration]], UnsetType] = unset,
        **kwargs,
    ):
        """
        Response object that includes metrics and metric tag configurations.

        :param data: Array of metrics and metric tag configurations.
        :type data: [MetricsAndMetricTagConfigurations], optional
        """
        if data is not unset:
            kwargs["data"] = data
        super().__init__(kwargs)
