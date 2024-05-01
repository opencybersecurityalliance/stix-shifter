# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


class SLOHistoryMetricsSeriesMetadataUnit(ModelNormal):
    _nullable = True

    @cached_property
    def openapi_types(_):
        return {
            "family": (str,),
            "id": (int,),
            "name": (str,),
            "plural": (str, none_type),
            "scale_factor": (float,),
            "short_name": (str, none_type),
        }

    attribute_map = {
        "family": "family",
        "id": "id",
        "name": "name",
        "plural": "plural",
        "scale_factor": "scale_factor",
        "short_name": "short_name",
    }

    def __init__(
        self_,
        family: Union[str, UnsetType] = unset,
        id: Union[int, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        plural: Union[str, none_type, UnsetType] = unset,
        scale_factor: Union[float, UnsetType] = unset,
        short_name: Union[str, none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        An Object of metric units.

        :param family: The family of metric unit, for example ``bytes`` is the family for ``kibibyte`` , ``byte`` , and ``bit`` units.
        :type family: str, optional

        :param id: The ID of the metric unit.
        :type id: int, optional

        :param name: The unit of the metric, for instance ``byte``.
        :type name: str, optional

        :param plural: The plural Unit of metric, for instance ``bytes``.
        :type plural: str, none_type, optional

        :param scale_factor: The scale factor of metric unit, for instance ``1.0``.
        :type scale_factor: float, optional

        :param short_name: A shorter and abbreviated version of the metric unit, for instance ``B``.
        :type short_name: str, none_type, optional
        """
        if family is not unset:
            kwargs["family"] = family
        if id is not unset:
            kwargs["id"] = id
        if name is not unset:
            kwargs["name"] = name
        if plural is not unset:
            kwargs["plural"] = plural
        if scale_factor is not unset:
            kwargs["scale_factor"] = scale_factor
        if short_name is not unset:
            kwargs["short_name"] = short_name
        super().__init__(kwargs)
