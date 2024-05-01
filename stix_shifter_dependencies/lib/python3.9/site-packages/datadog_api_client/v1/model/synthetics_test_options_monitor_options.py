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


class SyntheticsTestOptionsMonitorOptions(ModelNormal):
    validations = {
        "renotify_interval": {
            "inclusive_maximum": 1440,
            "inclusive_minimum": 0,
        },
    }

    @cached_property
    def openapi_types(_):
        return {
            "renotify_interval": (int,),
        }

    attribute_map = {
        "renotify_interval": "renotify_interval",
    }

    def __init__(self_, renotify_interval: Union[int, UnsetType] = unset, **kwargs):
        """
        Object containing the options for a Synthetic test as a monitor
        (for example, renotification).

        :param renotify_interval: Time interval before renotifying if the test is still failing
            (in minutes).
        :type renotify_interval: int, optional
        """
        if renotify_interval is not unset:
            kwargs["renotify_interval"] = renotify_interval
        super().__init__(kwargs)
