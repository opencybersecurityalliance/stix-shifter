# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class RunWorkflowWidgetDefinitionType(ModelSimple):
    """
    Type of the run workflow widget.

    :param value: If omitted defaults to "run_workflow". Must be one of ["run_workflow"].
    :type value: str
    """

    allowed_values = {
        "run_workflow",
    }
    RUN_WORKFLOW: ClassVar["RunWorkflowWidgetDefinitionType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


RunWorkflowWidgetDefinitionType.RUN_WORKFLOW = RunWorkflowWidgetDefinitionType("run_workflow")
