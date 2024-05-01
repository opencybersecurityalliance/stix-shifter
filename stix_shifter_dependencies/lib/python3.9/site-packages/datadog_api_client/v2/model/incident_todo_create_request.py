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
    from datadog_api_client.v2.model.incident_todo_create_data import IncidentTodoCreateData


class IncidentTodoCreateRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.incident_todo_create_data import IncidentTodoCreateData

        return {
            "data": (IncidentTodoCreateData,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: IncidentTodoCreateData, **kwargs):
        """
        Create request for an incident todo.

        :param data: Incident todo data for a create request.
        :type data: IncidentTodoCreateData
        """
        super().__init__(kwargs)

        self_.data = data
