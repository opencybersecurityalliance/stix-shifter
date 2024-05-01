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


class SecurityMonitoringRuleImpossibleTravelOptions(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "baseline_user_locations": (bool,),
        }

    attribute_map = {
        "baseline_user_locations": "baselineUserLocations",
    }

    def __init__(self_, baseline_user_locations: Union[bool, UnsetType] = unset, **kwargs):
        """
        Options on impossible travel rules.

        :param baseline_user_locations: If true, signals are suppressed for the first 24 hours. In that time, Datadog learns the user's regular
            access locations. This can be helpful to reduce noise and infer VPN usage or credentialed API access.
        :type baseline_user_locations: bool, optional
        """
        if baseline_user_locations is not unset:
            kwargs["baseline_user_locations"] = baseline_user_locations
        super().__init__(kwargs)
