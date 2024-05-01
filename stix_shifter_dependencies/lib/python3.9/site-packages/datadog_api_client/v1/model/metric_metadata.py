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


class MetricMetadata(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "description": (str,),
            "integration": (str,),
            "per_unit": (str,),
            "short_name": (str,),
            "statsd_interval": (int,),
            "type": (str,),
            "unit": (str,),
        }

    attribute_map = {
        "description": "description",
        "integration": "integration",
        "per_unit": "per_unit",
        "short_name": "short_name",
        "statsd_interval": "statsd_interval",
        "type": "type",
        "unit": "unit",
    }
    read_only_vars = {
        "integration",
    }

    def __init__(
        self_,
        description: Union[str, UnsetType] = unset,
        integration: Union[str, UnsetType] = unset,
        per_unit: Union[str, UnsetType] = unset,
        short_name: Union[str, UnsetType] = unset,
        statsd_interval: Union[int, UnsetType] = unset,
        type: Union[str, UnsetType] = unset,
        unit: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object with all metric related metadata.

        :param description: Metric description.
        :type description: str, optional

        :param integration: Name of the integration that sent the metric if applicable.
        :type integration: str, optional

        :param per_unit: Per unit of the metric such as ``second`` in ``bytes per second``.
        :type per_unit: str, optional

        :param short_name: A more human-readable and abbreviated version of the metric name.
        :type short_name: str, optional

        :param statsd_interval: StatsD flush interval of the metric in seconds if applicable.
        :type statsd_interval: int, optional

        :param type: Metric type such as ``gauge`` or ``rate``.
        :type type: str, optional

        :param unit: Primary unit of the metric such as ``byte`` or ``operation``.
        :type unit: str, optional
        """
        if description is not unset:
            kwargs["description"] = description
        if integration is not unset:
            kwargs["integration"] = integration
        if per_unit is not unset:
            kwargs["per_unit"] = per_unit
        if short_name is not unset:
            kwargs["short_name"] = short_name
        if statsd_interval is not unset:
            kwargs["statsd_interval"] = statsd_interval
        if type is not unset:
            kwargs["type"] = type
        if unit is not unset:
            kwargs["unit"] = unit
        super().__init__(kwargs)
