# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.incident_todo_assignee_array import IncidentTodoAssigneeArray


class IncidentTodoAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_todo_assignee_array import IncidentTodoAssigneeArray

        return {
            "assignees": (IncidentTodoAssigneeArray,),
            "completed": (str, none_type),
            "content": (str,),
            "due_date": (str, none_type),
            "incident_id": (str,),
        }

    attribute_map = {
        "assignees": "assignees",
        "completed": "completed",
        "content": "content",
        "due_date": "due_date",
        "incident_id": "incident_id",
    }

    def __init__(
        self_,
        assignees: IncidentTodoAssigneeArray,
        content: str,
        completed: Union[str, none_type, UnsetType] = unset,
        due_date: Union[str, none_type, UnsetType] = unset,
        incident_id: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Incident todo's attributes.

        :param assignees: Array of todo assignees.
        :type assignees: IncidentTodoAssigneeArray

        :param completed: Timestamp when the todo was completed.
        :type completed: str, none_type, optional

        :param content: The follow-up task's content.
        :type content: str

        :param due_date: Timestamp when the todo should be completed by.
        :type due_date: str, none_type, optional

        :param incident_id: UUID of the incident this todo is connected to.
        :type incident_id: str, optional
        """
        if completed is not unset:
            kwargs["completed"] = completed
        if due_date is not unset:
            kwargs["due_date"] = due_date
        if incident_id is not unset:
            kwargs["incident_id"] = incident_id
        super().__init__(kwargs)

        self_.assignees = assignees
        self_.content = content
