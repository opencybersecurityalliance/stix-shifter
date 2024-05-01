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
    from datadog_api_client.v2.model.event import Event
    from datadog_api_client.v2.model.monitor_type import MonitorType
    from datadog_api_client.v2.model.event_priority import EventPriority
    from datadog_api_client.v2.model.event_status_type import EventStatusType


class EventAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.event import Event
        from datadog_api_client.v2.model.monitor_type import MonitorType
        from datadog_api_client.v2.model.event_priority import EventPriority
        from datadog_api_client.v2.model.event_status_type import EventStatusType

        return {
            "aggregation_key": (str,),
            "date_happened": (int,),
            "device_name": (str,),
            "duration": (int,),
            "event_object": (str,),
            "evt": (Event,),
            "hostname": (str,),
            "monitor": (MonitorType,),
            "monitor_groups": ([str], none_type),
            "monitor_id": (int, none_type),
            "priority": (EventPriority,),
            "related_event_id": (int,),
            "service": (str,),
            "source_type_name": (str,),
            "sourcecategory": (str,),
            "status": (EventStatusType,),
            "tags": ([str],),
            "timestamp": (int,),
            "title": (str,),
        }

    attribute_map = {
        "aggregation_key": "aggregation_key",
        "date_happened": "date_happened",
        "device_name": "device_name",
        "duration": "duration",
        "event_object": "event_object",
        "evt": "evt",
        "hostname": "hostname",
        "monitor": "monitor",
        "monitor_groups": "monitor_groups",
        "monitor_id": "monitor_id",
        "priority": "priority",
        "related_event_id": "related_event_id",
        "service": "service",
        "source_type_name": "source_type_name",
        "sourcecategory": "sourcecategory",
        "status": "status",
        "tags": "tags",
        "timestamp": "timestamp",
        "title": "title",
    }

    def __init__(
        self_,
        aggregation_key: Union[str, UnsetType] = unset,
        date_happened: Union[int, UnsetType] = unset,
        device_name: Union[str, UnsetType] = unset,
        duration: Union[int, UnsetType] = unset,
        event_object: Union[str, UnsetType] = unset,
        evt: Union[Event, UnsetType] = unset,
        hostname: Union[str, UnsetType] = unset,
        monitor: Union[MonitorType, none_type, UnsetType] = unset,
        monitor_groups: Union[List[str], none_type, UnsetType] = unset,
        monitor_id: Union[int, none_type, UnsetType] = unset,
        priority: Union[EventPriority, none_type, UnsetType] = unset,
        related_event_id: Union[int, UnsetType] = unset,
        service: Union[str, UnsetType] = unset,
        source_type_name: Union[str, UnsetType] = unset,
        sourcecategory: Union[str, UnsetType] = unset,
        status: Union[EventStatusType, UnsetType] = unset,
        tags: Union[List[str], UnsetType] = unset,
        timestamp: Union[int, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object description of attributes from your event.

        :param aggregation_key: Aggregation key of the event.
        :type aggregation_key: str, optional

        :param date_happened: POSIX timestamp of the event. Must be sent as an integer (no quotation marks).
            Limited to events no older than 18 hours.
        :type date_happened: int, optional

        :param device_name: A device name.
        :type device_name: str, optional

        :param duration: The duration between the triggering of the event and its recovery in nanoseconds.
        :type duration: int, optional

        :param event_object: The event title.
        :type event_object: str, optional

        :param evt: The metadata associated with a request.
        :type evt: Event, optional

        :param hostname: Host name to associate with the event.
            Any tags associated with the host are also applied to this event.
        :type hostname: str, optional

        :param monitor: Attributes from the monitor that triggered the event.
        :type monitor: MonitorType, none_type, optional

        :param monitor_groups: List of groups referred to in the event.
        :type monitor_groups: [str], none_type, optional

        :param monitor_id: ID of the monitor that triggered the event. When an event isn't related to a monitor, this field is empty.
        :type monitor_id: int, none_type, optional

        :param priority: The priority of the event's monitor. For example, ``normal`` or ``low``.
        :type priority: EventPriority, none_type, optional

        :param related_event_id: Related event ID.
        :type related_event_id: int, optional

        :param service: Service that triggered the event.
        :type service: str, optional

        :param source_type_name: The type of event being posted.
            For example, ``nagios`` , ``hudson`` , ``jenkins`` , ``my_apps`` , ``chef`` , ``puppet`` , ``git`` or ``bitbucket``.
            The list of standard source attribute values is `available here <https://docs.datadoghq.com/integrations/faq/list-of-api-source-attribute-value>`_.
        :type source_type_name: str, optional

        :param sourcecategory: Identifier for the source of the event, such as a monitor alert, an externally-submitted event, or an integration.
        :type sourcecategory: str, optional

        :param status: If an alert event is enabled, its status is one of the following:
            ``failure`` , ``error`` , ``warning`` , ``info`` , ``success`` , ``user_update`` ,
            ``recommendation`` , or ``snapshot``.
        :type status: EventStatusType, optional

        :param tags: A list of tags to apply to the event.
        :type tags: [str], optional

        :param timestamp: POSIX timestamp of your event in milliseconds.
        :type timestamp: int, optional

        :param title: The event title.
        :type title: str, optional
        """
        if aggregation_key is not unset:
            kwargs["aggregation_key"] = aggregation_key
        if date_happened is not unset:
            kwargs["date_happened"] = date_happened
        if device_name is not unset:
            kwargs["device_name"] = device_name
        if duration is not unset:
            kwargs["duration"] = duration
        if event_object is not unset:
            kwargs["event_object"] = event_object
        if evt is not unset:
            kwargs["evt"] = evt
        if hostname is not unset:
            kwargs["hostname"] = hostname
        if monitor is not unset:
            kwargs["monitor"] = monitor
        if monitor_groups is not unset:
            kwargs["monitor_groups"] = monitor_groups
        if monitor_id is not unset:
            kwargs["monitor_id"] = monitor_id
        if priority is not unset:
            kwargs["priority"] = priority
        if related_event_id is not unset:
            kwargs["related_event_id"] = related_event_id
        if service is not unset:
            kwargs["service"] = service
        if source_type_name is not unset:
            kwargs["source_type_name"] = source_type_name
        if sourcecategory is not unset:
            kwargs["sourcecategory"] = sourcecategory
        if status is not unset:
            kwargs["status"] = status
        if tags is not unset:
            kwargs["tags"] = tags
        if timestamp is not unset:
            kwargs["timestamp"] = timestamp
        if title is not unset:
            kwargs["title"] = title
        super().__init__(kwargs)
