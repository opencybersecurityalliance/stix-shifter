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
    from datadog_api_client.v2.model.event_response_attributes import EventResponseAttributes
    from datadog_api_client.v2.model.event_type import EventType


class EventResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.event_response_attributes import EventResponseAttributes
        from datadog_api_client.v2.model.event_type import EventType

        return {
            "attributes": (EventResponseAttributes,),
            "id": (str,),
            "type": (EventType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: Union[EventResponseAttributes, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        type: Union[EventType, UnsetType] = unset,
        **kwargs,
    ):
        """
        The object description of an event after being processed and stored by Datadog.

        :param attributes: The object description of an event response attribute.
        :type attributes: EventResponseAttributes, optional

        :param id: the unique ID of the event.
        :type id: str, optional

        :param type: Type of the event.
        :type type: EventType, optional
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if id is not unset:
            kwargs["id"] = id
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
