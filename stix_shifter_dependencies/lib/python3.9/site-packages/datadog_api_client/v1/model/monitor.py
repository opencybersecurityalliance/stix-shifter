# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    datetime,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.creator import Creator
    from datadog_api_client.v1.model.monitor_options import MonitorOptions
    from datadog_api_client.v1.model.monitor_overall_states import MonitorOverallStates
    from datadog_api_client.v1.model.monitor_state import MonitorState
    from datadog_api_client.v1.model.monitor_type import MonitorType


class Monitor(ModelNormal):
    validations = {
        "priority": {
            "inclusive_maximum": 5,
            "inclusive_minimum": 1,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.creator import Creator
        from datadog_api_client.v1.model.monitor_options import MonitorOptions
        from datadog_api_client.v1.model.monitor_overall_states import MonitorOverallStates
        from datadog_api_client.v1.model.monitor_state import MonitorState
        from datadog_api_client.v1.model.monitor_type import MonitorType

        return {
            "created": (datetime,),
            "creator": (Creator,),
            "deleted": (datetime, none_type),
            "id": (int,),
            "message": (str,),
            "modified": (datetime,),
            "multi": (bool,),
            "name": (str,),
            "options": (MonitorOptions,),
            "overall_state": (MonitorOverallStates,),
            "priority": (int, none_type),
            "query": (str,),
            "restricted_roles": ([str], none_type),
            "state": (MonitorState,),
            "tags": ([str],),
            "type": (MonitorType,),
        }

    attribute_map = {
        "created": "created",
        "creator": "creator",
        "deleted": "deleted",
        "id": "id",
        "message": "message",
        "modified": "modified",
        "multi": "multi",
        "name": "name",
        "options": "options",
        "overall_state": "overall_state",
        "priority": "priority",
        "query": "query",
        "restricted_roles": "restricted_roles",
        "state": "state",
        "tags": "tags",
        "type": "type",
    }
    read_only_vars = {
        "created",
        "creator",
        "deleted",
        "id",
        "modified",
        "multi",
        "overall_state",
        "state",
    }

    def __init__(
        self_,
        query: str,
        type: MonitorType,
        created: Union[datetime, UnsetType] = unset,
        creator: Union[Creator, UnsetType] = unset,
        deleted: Union[datetime, none_type, UnsetType] = unset,
        id: Union[int, UnsetType] = unset,
        message: Union[str, UnsetType] = unset,
        modified: Union[datetime, UnsetType] = unset,
        multi: Union[bool, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        options: Union[MonitorOptions, UnsetType] = unset,
        overall_state: Union[MonitorOverallStates, UnsetType] = unset,
        priority: Union[int, none_type, UnsetType] = unset,
        restricted_roles: Union[List[str], none_type, UnsetType] = unset,
        state: Union[MonitorState, UnsetType] = unset,
        tags: Union[List[str], UnsetType] = unset,
        **kwargs,
    ):
        """
        Object describing a monitor.

        :param created: Timestamp of the monitor creation.
        :type created: datetime, optional

        :param creator: Object describing the creator of the shared element.
        :type creator: Creator, optional

        :param deleted: Whether or not the monitor is deleted. (Always ``null`` )
        :type deleted: datetime, none_type, optional

        :param id: ID of this monitor.
        :type id: int, optional

        :param message: A message to include with notifications for this monitor.
        :type message: str, optional

        :param modified: Last timestamp when the monitor was edited.
        :type modified: datetime, optional

        :param multi: Whether or not the monitor is broken down on different groups.
        :type multi: bool, optional

        :param name: The monitor name.
        :type name: str, optional

        :param options: List of options associated with your monitor.
        :type options: MonitorOptions, optional

        :param overall_state: The different states your monitor can be in.
        :type overall_state: MonitorOverallStates, optional

        :param priority: Integer from 1 (high) to 5 (low) indicating alert severity.
        :type priority: int, none_type, optional

        :param query: The monitor query.
        :type query: str

        :param restricted_roles: A list of unique role identifiers to define which roles are allowed to edit the monitor. The unique identifiers for all roles can be pulled from the `Roles API <https://docs.datadoghq.com/api/latest/roles/#list-roles>`_ and are located in the ``data.id`` field. Editing a monitor includes any updates to the monitor configuration, monitor deletion, and muting of the monitor for any amount of time. ``restricted_roles`` is the successor of ``locked``. For more information about ``locked`` and ``restricted_roles`` , see the `monitor options docs <https://docs.datadoghq.com/monitors/guide/monitor_api_options/#permissions-options>`_.
        :type restricted_roles: [str], none_type, optional

        :param state: Wrapper object with the different monitor states.
        :type state: MonitorState, optional

        :param tags: Tags associated to your monitor.
        :type tags: [str], optional

        :param type: The type of the monitor. For more information about ``type`` , see the `monitor options <https://docs.datadoghq.com/monitors/guide/monitor_api_options/>`_ docs.
        :type type: MonitorType
        """
        if created is not unset:
            kwargs["created"] = created
        if creator is not unset:
            kwargs["creator"] = creator
        if deleted is not unset:
            kwargs["deleted"] = deleted
        if id is not unset:
            kwargs["id"] = id
        if message is not unset:
            kwargs["message"] = message
        if modified is not unset:
            kwargs["modified"] = modified
        if multi is not unset:
            kwargs["multi"] = multi
        if name is not unset:
            kwargs["name"] = name
        if options is not unset:
            kwargs["options"] = options
        if overall_state is not unset:
            kwargs["overall_state"] = overall_state
        if priority is not unset:
            kwargs["priority"] = priority
        if restricted_roles is not unset:
            kwargs["restricted_roles"] = restricted_roles
        if state is not unset:
            kwargs["state"] = state
        if tags is not unset:
            kwargs["tags"] = tags
        super().__init__(kwargs)

        self_.query = query
        self_.type = type
