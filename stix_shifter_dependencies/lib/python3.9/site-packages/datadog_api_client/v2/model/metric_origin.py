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


class MetricOrigin(ModelNormal):
    validations = {
        "metric_type": {
            "inclusive_maximum": 1000,
        },
        "product": {
            "inclusive_maximum": 1000,
        },
        "service": {
            "inclusive_maximum": 1000,
        },
    }

    @cached_property
    def openapi_types(_):
        return {
            "metric_type": (int,),
            "product": (int,),
            "service": (int,),
        }

    attribute_map = {
        "metric_type": "metric_type",
        "product": "product",
        "service": "service",
    }

    def __init__(
        self_,
        metric_type: Union[int, UnsetType] = unset,
        product: Union[int, UnsetType] = unset,
        service: Union[int, UnsetType] = unset,
        **kwargs,
    ):
        """
        Metric origin information.

        :param metric_type: The origin metric type code
        :type metric_type: int, optional

        :param product: The origin product code
        :type product: int, optional

        :param service: The origin service code
        :type service: int, optional
        """
        if metric_type is not unset:
            kwargs["metric_type"] = metric_type
        if product is not unset:
            kwargs["product"] = product
        if service is not unset:
            kwargs["service"] = service
        super().__init__(kwargs)
