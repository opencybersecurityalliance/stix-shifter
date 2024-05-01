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


class MetricsQueryUnit(ModelNormal):
    _nullable = True

    @cached_property
    def openapi_types(_):
        return {
            "family": (str,),
            "name": (str,),
            "plural": (str,),
            "scale_factor": (float,),
            "short_name": (str,),
        }

    attribute_map = {
        "family": "family",
        "name": "name",
        "plural": "plural",
        "scale_factor": "scale_factor",
        "short_name": "short_name",
    }
    read_only_vars = {
        "family",
        "name",
        "plural",
        "scale_factor",
        "short_name",
    }

    def __init__(
        self_,
        family: Union[str, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        plural: Union[str, UnsetType] = unset,
        scale_factor: Union[float, UnsetType] = unset,
        short_name: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object containing the metric unit family, scale factor, name, and short name.

        :param family: Unit family, allows for conversion between units of the same family, for scaling.
        :type family: str, optional

        :param name: Unit name
        :type name: str, optional

        :param plural: Plural form of the unit name.
        :type plural: str, optional

        :param scale_factor: Factor for scaling between units of the same family.
        :type scale_factor: float, optional

        :param short_name: Abbreviation of the unit.
        :type short_name: str, optional
        """
        if family is not unset:
            kwargs["family"] = family
        if name is not unset:
            kwargs["name"] = name
        if plural is not unset:
            kwargs["plural"] = plural
        if scale_factor is not unset:
            kwargs["scale_factor"] = scale_factor
        if short_name is not unset:
            kwargs["short_name"] = short_name
        super().__init__(kwargs)
