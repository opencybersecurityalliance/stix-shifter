# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.dashboard_template_variable_preset_value import (
        DashboardTemplateVariablePresetValue,
    )


class DashboardTemplateVariablePreset(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.dashboard_template_variable_preset_value import (
            DashboardTemplateVariablePresetValue,
        )

        return {
            "name": (str,),
            "template_variables": ([DashboardTemplateVariablePresetValue],),
        }

    attribute_map = {
        "name": "name",
        "template_variables": "template_variables",
    }

    def __init__(
        self_,
        name: Union[str, UnsetType] = unset,
        template_variables: Union[List[DashboardTemplateVariablePresetValue], UnsetType] = unset,
        **kwargs,
    ):
        """
        Template variables saved views.

        :param name: The name of the variable.
        :type name: str, optional

        :param template_variables: List of variables.
        :type template_variables: [DashboardTemplateVariablePresetValue], optional
        """
        if name is not unset:
            kwargs["name"] = name
        if template_variables is not unset:
            kwargs["template_variables"] = template_variables
        super().__init__(kwargs)
