# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.incident_todo_anonymous_assignee_source import IncidentTodoAnonymousAssigneeSource


class IncidentTodoAnonymousAssignee(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_todo_anonymous_assignee_source import (
            IncidentTodoAnonymousAssigneeSource,
        )

        return {
            "icon": (str,),
            "id": (str,),
            "name": (str,),
            "source": (IncidentTodoAnonymousAssigneeSource,),
        }

    attribute_map = {
        "icon": "icon",
        "id": "id",
        "name": "name",
        "source": "source",
    }

    def __init__(self_, icon: str, id: str, name: str, source: IncidentTodoAnonymousAssigneeSource, **kwargs):
        """
        Anonymous assignee entity.

        :param icon: URL for assignee's icon.
        :type icon: str

        :param id: Anonymous assignee's ID.
        :type id: str

        :param name: Assignee's name.
        :type name: str

        :param source: The source of the anonymous assignee.
        :type source: IncidentTodoAnonymousAssigneeSource
        """
        super().__init__(kwargs)

        self_.icon = icon
        self_.id = id
        self_.name = name
        self_.source = source
