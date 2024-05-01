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
    from datadog_api_client.v2.model.incident_todo_attributes import IncidentTodoAttributes
    from datadog_api_client.v2.model.incident_todo_type import IncidentTodoType


class IncidentTodoCreateData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_todo_attributes import IncidentTodoAttributes
        from datadog_api_client.v2.model.incident_todo_type import IncidentTodoType

        return {
            "attributes": (IncidentTodoAttributes,),
            "type": (IncidentTodoType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "type": "type",
    }

    def __init__(self_, attributes: IncidentTodoAttributes, type: IncidentTodoType, **kwargs):
        """
        Incident todo data for a create request.

        :param attributes: Incident todo's attributes.
        :type attributes: IncidentTodoAttributes

        :param type: Todo resource type.
        :type type: IncidentTodoType
        """
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.type = type
