# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


class RunWorkflowWidgetInput(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "name": (str,),
            "value": (str,),
        }

    attribute_map = {
        "name": "name",
        "value": "value",
    }

    def __init__(self_, name: str, value: str, **kwargs):
        """
        Object to map a dashboard template variable to a workflow input.

        :param name: Name of the workflow input.
        :type name: str

        :param value: Dashboard template variable. Can be suffixed with '.value' or '.key'.
        :type value: str
        """
        super().__init__(kwargs)

        self_.name = name
        self_.value = value
