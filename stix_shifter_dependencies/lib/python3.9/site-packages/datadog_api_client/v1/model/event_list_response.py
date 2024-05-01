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
    from datadog_api_client.v1.model.event import Event


class EventListResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.event import Event

        return {
            "events": ([Event],),
            "status": (str,),
        }

    attribute_map = {
        "events": "events",
        "status": "status",
    }

    def __init__(self_, events: Union[List[Event], UnsetType] = unset, status: Union[str, UnsetType] = unset, **kwargs):
        """
        An event list response.

        :param events: An array of events.
        :type events: [Event], optional

        :param status: A status.
        :type status: str, optional
        """
        if events is not unset:
            kwargs["events"] = events
        if status is not unset:
            kwargs["status"] = status
        super().__init__(kwargs)
