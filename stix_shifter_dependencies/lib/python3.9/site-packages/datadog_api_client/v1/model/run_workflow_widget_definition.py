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
    from datadog_api_client.v1.model.widget_custom_link import WidgetCustomLink
    from datadog_api_client.v1.model.run_workflow_widget_input import RunWorkflowWidgetInput
    from datadog_api_client.v1.model.widget_time import WidgetTime
    from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
    from datadog_api_client.v1.model.run_workflow_widget_definition_type import RunWorkflowWidgetDefinitionType


class RunWorkflowWidgetDefinition(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_custom_link import WidgetCustomLink
        from datadog_api_client.v1.model.run_workflow_widget_input import RunWorkflowWidgetInput
        from datadog_api_client.v1.model.widget_time import WidgetTime
        from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
        from datadog_api_client.v1.model.run_workflow_widget_definition_type import RunWorkflowWidgetDefinitionType

        return {
            "custom_links": ([WidgetCustomLink],),
            "inputs": ([RunWorkflowWidgetInput],),
            "time": (WidgetTime,),
            "title": (str,),
            "title_align": (WidgetTextAlign,),
            "title_size": (str,),
            "type": (RunWorkflowWidgetDefinitionType,),
            "workflow_id": (str,),
        }

    attribute_map = {
        "custom_links": "custom_links",
        "inputs": "inputs",
        "time": "time",
        "title": "title",
        "title_align": "title_align",
        "title_size": "title_size",
        "type": "type",
        "workflow_id": "workflow_id",
    }

    def __init__(
        self_,
        type: RunWorkflowWidgetDefinitionType,
        workflow_id: str,
        custom_links: Union[List[WidgetCustomLink], UnsetType] = unset,
        inputs: Union[List[RunWorkflowWidgetInput], UnsetType] = unset,
        time: Union[WidgetTime, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        title_align: Union[WidgetTextAlign, UnsetType] = unset,
        title_size: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Run workflow is widget that allows you to run a workflow from a dashboard.

        :param custom_links: List of custom links.
        :type custom_links: [WidgetCustomLink], optional

        :param inputs: Array of workflow inputs to map to dashboard template variables.
        :type inputs: [RunWorkflowWidgetInput], optional

        :param time: Time setting for the widget.
        :type time: WidgetTime, optional

        :param title: Title of your widget.
        :type title: str, optional

        :param title_align: How to align the text on the widget.
        :type title_align: WidgetTextAlign, optional

        :param title_size: Size of the title.
        :type title_size: str, optional

        :param type: Type of the run workflow widget.
        :type type: RunWorkflowWidgetDefinitionType

        :param workflow_id: Workflow id.
        :type workflow_id: str
        """
        if custom_links is not unset:
            kwargs["custom_links"] = custom_links
        if inputs is not unset:
            kwargs["inputs"] = inputs
        if time is not unset:
            kwargs["time"] = time
        if title is not unset:
            kwargs["title"] = title
        if title_align is not unset:
            kwargs["title_align"] = title_align
        if title_size is not unset:
            kwargs["title_size"] = title_size
        super().__init__(kwargs)

        self_.type = type
        self_.workflow_id = workflow_id
