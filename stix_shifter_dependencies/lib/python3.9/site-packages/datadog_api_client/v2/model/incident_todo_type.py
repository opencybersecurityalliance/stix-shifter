# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class IncidentTodoType(ModelSimple):
    """
    Todo resource type.

    :param value: If omitted defaults to "incident_todos". Must be one of ["incident_todos"].
    :type value: str
    """

    allowed_values = {
        "incident_todos",
    }
    INCIDENT_TODOS: ClassVar["IncidentTodoType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


IncidentTodoType.INCIDENT_TODOS = IncidentTodoType("incident_todos")
