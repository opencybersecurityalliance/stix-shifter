# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.event_alert_type import EventAlertType
    from datadog_api_client.v1.model.event_priority import EventPriority


class EventCreateRequest(ModelNormal):
    validations = {
        "aggregation_key": {
            "max_length": 100,
        },
        "text": {
            "max_length": 4000,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.event_alert_type import EventAlertType
        from datadog_api_client.v1.model.event_priority import EventPriority

        return {
            "aggregation_key": (str,),
            "alert_type": (EventAlertType,),
            "date_happened": (int,),
            "device_name": (str,),
            "host": (str,),
            "priority": (EventPriority,),
            "related_event_id": (int,),
            "source_type_name": (str,),
            "tags": ([str],),
            "text": (str,),
            "title": (str,),
        }

    attribute_map = {
        "aggregation_key": "aggregation_key",
        "alert_type": "alert_type",
        "date_happened": "date_happened",
        "device_name": "device_name",
        "host": "host",
        "priority": "priority",
        "related_event_id": "related_event_id",
        "source_type_name": "source_type_name",
        "tags": "tags",
        "text": "text",
        "title": "title",
    }

    def __init__(
        self_,
        text: str,
        title: str,
        aggregation_key: Union[str, UnsetType] = unset,
        alert_type: Union[EventAlertType, UnsetType] = unset,
        date_happened: Union[int, UnsetType] = unset,
        device_name: Union[str, UnsetType] = unset,
        host: Union[str, UnsetType] = unset,
        priority: Union[EventPriority, none_type, UnsetType] = unset,
        related_event_id: Union[int, UnsetType] = unset,
        source_type_name: Union[str, UnsetType] = unset,
        tags: Union[List[str], UnsetType] = unset,
        **kwargs,
    ):
        """
        Object representing an event.

        :param aggregation_key: An arbitrary string to use for aggregation. Limited to 100 characters.
            If you specify a key, all events using that key are grouped together in the Event Stream.
        :type aggregation_key: str, optional

        :param alert_type: If an alert event is enabled, set its type.
            For example, ``error`` , ``warning`` , ``info`` , ``success`` , ``user_update`` ,
            ``recommendation`` , and ``snapshot``.
        :type alert_type: EventAlertType, optional

        :param date_happened: POSIX timestamp of the event. Must be sent as an integer (that is no quotes).
            Limited to events no older than 18 hours
        :type date_happened: int, optional

        :param device_name: A device name.
        :type device_name: str, optional

        :param host: Host name to associate with the event.
            Any tags associated with the host are also applied to this event.
        :type host: str, optional

        :param priority: The priority of the event. For example, ``normal`` or ``low``.
        :type priority: EventPriority, none_type, optional

        :param related_event_id: ID of the parent event. Must be sent as an integer (that is no quotes).
        :type related_event_id: int, optional

        :param source_type_name: The type of event being posted. Option examples include nagios, hudson, jenkins, my_apps, chef, puppet, git, bitbucket, etc.
            A complete list of source attribute values `available here <https://docs.datadoghq.com/integrations/faq/list-of-api-source-attribute-value>`_.
        :type source_type_name: str, optional

        :param tags: A list of tags to apply to the event.
        :type tags: [str], optional

        :param text: The body of the event. Limited to 4000 characters. The text supports markdown.
            To use markdown in the event text, start the text block with ``%%% \\n`` and end the text block with ``\\n %%%``.
            Use ``msg_text`` with the Datadog Ruby library.
        :type text: str

        :param title: The event title.
        :type title: str
        """
        if aggregation_key is not unset:
            kwargs["aggregation_key"] = aggregation_key
        if alert_type is not unset:
            kwargs["alert_type"] = alert_type
        if date_happened is not unset:
            kwargs["date_happened"] = date_happened
        if device_name is not unset:
            kwargs["device_name"] = device_name
        if host is not unset:
            kwargs["host"] = host
        if priority is not unset:
            kwargs["priority"] = priority
        if related_event_id is not unset:
            kwargs["related_event_id"] = related_event_id
        if source_type_name is not unset:
            kwargs["source_type_name"] = source_type_name
        if tags is not unset:
            kwargs["tags"] = tags
        super().__init__(kwargs)

        self_.text = text
        self_.title = title
