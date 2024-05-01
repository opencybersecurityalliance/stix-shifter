# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.slo_timeframe import SLOTimeframe


class SLOThreshold(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.slo_timeframe import SLOTimeframe

        return {
            "target": (float,),
            "target_display": (str,),
            "timeframe": (SLOTimeframe,),
            "warning": (float,),
            "warning_display": (str,),
        }

    attribute_map = {
        "target": "target",
        "target_display": "target_display",
        "timeframe": "timeframe",
        "warning": "warning",
        "warning_display": "warning_display",
    }

    def __init__(
        self_,
        target: float,
        timeframe: SLOTimeframe,
        target_display: Union[str, UnsetType] = unset,
        warning: Union[float, UnsetType] = unset,
        warning_display: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        SLO thresholds (target and optionally warning) for a single time window.

        :param target: The target value for the service level indicator within the corresponding
            timeframe.
        :type target: float

        :param target_display: A string representation of the target that indicates its precision.
            It uses trailing zeros to show significant decimal places (for example ``98.00`` ).

            Always included in service level objective responses. Ignored in
            create/update requests.
        :type target_display: str, optional

        :param timeframe: The SLO time window options.
        :type timeframe: SLOTimeframe

        :param warning: The warning value for the service level objective.
        :type warning: float, optional

        :param warning_display: A string representation of the warning target (see the description of
            the ``target_display`` field for details).

            Included in service level objective responses if a warning target exists.
            Ignored in create/update requests.
        :type warning_display: str, optional
        """
        if target_display is not unset:
            kwargs["target_display"] = target_display
        if warning is not unset:
            kwargs["warning"] = warning
        if warning_display is not unset:
            kwargs["warning_display"] = warning_display
        super().__init__(kwargs)

        self_.target = target
        self_.timeframe = timeframe
