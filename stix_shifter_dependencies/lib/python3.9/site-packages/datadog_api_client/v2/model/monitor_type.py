# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class MonitorType(ModelNormal):
    validations = {
        "group_status": {
            "inclusive_maximum": 2147483647,
        },
    }
    _nullable = True

    @cached_property
    def openapi_types(_):
        return {
            "created_at": (int,),
            "group_status": (int,),
            "groups": ([str],),
            "id": (int,),
            "message": (str,),
            "modified": (int,),
            "name": (str,),
            "query": (str,),
            "tags": ([str],),
            "templated_name": (str,),
            "type": (str,),
        }

    attribute_map = {
        "created_at": "created_at",
        "group_status": "group_status",
        "groups": "groups",
        "id": "id",
        "message": "message",
        "modified": "modified",
        "name": "name",
        "query": "query",
        "tags": "tags",
        "templated_name": "templated_name",
        "type": "type",
    }

    def __init__(
        self_,
        created_at: Union[int, UnsetType] = unset,
        group_status: Union[int, UnsetType] = unset,
        groups: Union[List[str], UnsetType] = unset,
        id: Union[int, UnsetType] = unset,
        message: Union[str, UnsetType] = unset,
        modified: Union[int, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        query: Union[str, UnsetType] = unset,
        tags: Union[List[str], UnsetType] = unset,
        templated_name: Union[str, UnsetType] = unset,
        type: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Attributes from the monitor that triggered the event.

        :param created_at: The POSIX timestamp of the monitor's creation in nanoseconds.
        :type created_at: int, optional

        :param group_status: Monitor group status used when there is no ``result_groups``.
        :type group_status: int, optional

        :param groups: Groups to which the monitor belongs.
        :type groups: [str], optional

        :param id: The monitor ID.
        :type id: int, optional

        :param message: The monitor message.
        :type message: str, optional

        :param modified: The monitor's last-modified timestamp.
        :type modified: int, optional

        :param name: The monitor name.
        :type name: str, optional

        :param query: The query that triggers the alert.
        :type query: str, optional

        :param tags: A list of tags attached to the monitor.
        :type tags: [str], optional

        :param templated_name: The templated name of the monitor before resolving any template variables.
        :type templated_name: str, optional

        :param type: The monitor type.
        :type type: str, optional
        """
        if created_at is not unset:
            kwargs["created_at"] = created_at
        if group_status is not unset:
            kwargs["group_status"] = group_status
        if groups is not unset:
            kwargs["groups"] = groups
        if id is not unset:
            kwargs["id"] = id
        if message is not unset:
            kwargs["message"] = message
        if modified is not unset:
            kwargs["modified"] = modified
        if name is not unset:
            kwargs["name"] = name
        if query is not unset:
            kwargs["query"] = query
        if tags is not unset:
            kwargs["tags"] = tags
        if templated_name is not unset:
            kwargs["templated_name"] = templated_name
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
