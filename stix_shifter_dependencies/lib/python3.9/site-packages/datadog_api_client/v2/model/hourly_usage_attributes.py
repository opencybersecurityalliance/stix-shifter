# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    datetime,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.hourly_usage_measurement import HourlyUsageMeasurement


class HourlyUsageAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.hourly_usage_measurement import HourlyUsageMeasurement

        return {
            "measurements": ([HourlyUsageMeasurement],),
            "org_name": (str,),
            "product_family": (str,),
            "public_id": (str,),
            "region": (str,),
            "timestamp": (datetime,),
        }

    attribute_map = {
        "measurements": "measurements",
        "org_name": "org_name",
        "product_family": "product_family",
        "public_id": "public_id",
        "region": "region",
        "timestamp": "timestamp",
    }

    def __init__(
        self_,
        measurements: Union[List[HourlyUsageMeasurement], UnsetType] = unset,
        org_name: Union[str, UnsetType] = unset,
        product_family: Union[str, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        region: Union[str, UnsetType] = unset,
        timestamp: Union[datetime, UnsetType] = unset,
        **kwargs,
    ):
        """
        Attributes of hourly usage for a product family for an org for a time period.

        :param measurements: List of the measured usage values for the product family for the org for the time period.
        :type measurements: [HourlyUsageMeasurement], optional

        :param org_name: The organization name.
        :type org_name: str, optional

        :param product_family: The product for which usage is being reported.
        :type product_family: str, optional

        :param public_id: The organization public ID.
        :type public_id: str, optional

        :param region: The region of the Datadog instance that the organization belongs to.
        :type region: str, optional

        :param timestamp: Datetime in ISO-8601 format, UTC. The hour for the usage.
        :type timestamp: datetime, optional
        """
        if measurements is not unset:
            kwargs["measurements"] = measurements
        if org_name is not unset:
            kwargs["org_name"] = org_name
        if product_family is not unset:
            kwargs["product_family"] = product_family
        if public_id is not unset:
            kwargs["public_id"] = public_id
        if region is not unset:
            kwargs["region"] = region
        if timestamp is not unset:
            kwargs["timestamp"] = timestamp
        super().__init__(kwargs)
