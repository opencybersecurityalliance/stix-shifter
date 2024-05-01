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
    from datadog_api_client.v2.model.metric_tag_configuration_create_data import MetricTagConfigurationCreateData


class MetricTagConfigurationCreateRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.metric_tag_configuration_create_data import MetricTagConfigurationCreateData

        return {
            "data": (MetricTagConfigurationCreateData,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: MetricTagConfigurationCreateData, **kwargs):
        """
        Request object that includes the metric that you would like to configure tags for.

        :param data: Object for a single metric to be configure tags on.
        :type data: MetricTagConfigurationCreateData
        """
        super().__init__(kwargs)

        self_.data = data
