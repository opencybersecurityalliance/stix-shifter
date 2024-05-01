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
    from datadog_api_client.v2.model.metric_metadata import MetricMetadata
    from datadog_api_client.v2.model.metric_point import MetricPoint
    from datadog_api_client.v2.model.metric_resource import MetricResource
    from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType


class MetricSeries(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.metric_metadata import MetricMetadata
        from datadog_api_client.v2.model.metric_point import MetricPoint
        from datadog_api_client.v2.model.metric_resource import MetricResource
        from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType

        return {
            "interval": (int,),
            "metadata": (MetricMetadata,),
            "metric": (str,),
            "points": ([MetricPoint],),
            "resources": ([MetricResource],),
            "source_type_name": (str,),
            "tags": ([str],),
            "type": (MetricIntakeType,),
            "unit": (str,),
        }

    attribute_map = {
        "interval": "interval",
        "metadata": "metadata",
        "metric": "metric",
        "points": "points",
        "resources": "resources",
        "source_type_name": "source_type_name",
        "tags": "tags",
        "type": "type",
        "unit": "unit",
    }

    def __init__(
        self_,
        metric: str,
        points: List[MetricPoint],
        interval: Union[int, UnsetType] = unset,
        metadata: Union[MetricMetadata, UnsetType] = unset,
        resources: Union[List[MetricResource], UnsetType] = unset,
        source_type_name: Union[str, UnsetType] = unset,
        tags: Union[List[str], UnsetType] = unset,
        type: Union[MetricIntakeType, UnsetType] = unset,
        unit: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        A metric to submit to Datadog.
        See `Datadog metrics <https://docs.datadoghq.com/developers/metrics/#custom-metrics-properties>`_.

        :param interval: If the type of the metric is rate or count, define the corresponding interval.
        :type interval: int, optional

        :param metadata: Metadata for the metric.
        :type metadata: MetricMetadata, optional

        :param metric: The name of the timeseries.
        :type metric: str

        :param points: Points relating to a metric. All points must be objects with timestamp and a scalar value (cannot be a string). Timestamps should be in POSIX time in seconds, and cannot be more than ten minutes in the future or more than one hour in the past.
        :type points: [MetricPoint]

        :param resources: A list of resources to associate with this metric.
        :type resources: [MetricResource], optional

        :param source_type_name: The source type name.
        :type source_type_name: str, optional

        :param tags: A list of tags associated with the metric.
        :type tags: [str], optional

        :param type: The type of metric. The available types are ``0`` (unspecified), ``1`` (count), ``2`` (rate), and ``3`` (gauge).
        :type type: MetricIntakeType, optional

        :param unit: The unit of point value.
        :type unit: str, optional
        """
        if interval is not unset:
            kwargs["interval"] = interval
        if metadata is not unset:
            kwargs["metadata"] = metadata
        if resources is not unset:
            kwargs["resources"] = resources
        if source_type_name is not unset:
            kwargs["source_type_name"] = source_type_name
        if tags is not unset:
            kwargs["tags"] = tags
        if type is not unset:
            kwargs["type"] = type
        if unit is not unset:
            kwargs["unit"] = unit
        super().__init__(kwargs)

        self_.metric = metric
        self_.points = points
