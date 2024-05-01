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
    from datadog_api_client.v1.model.widget_time_windows import WidgetTimeWindows
    from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
    from datadog_api_client.v1.model.slo_widget_definition_type import SLOWidgetDefinitionType
    from datadog_api_client.v1.model.widget_view_mode import WidgetViewMode


class SLOWidgetDefinition(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_time_windows import WidgetTimeWindows
        from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
        from datadog_api_client.v1.model.slo_widget_definition_type import SLOWidgetDefinitionType
        from datadog_api_client.v1.model.widget_view_mode import WidgetViewMode

        return {
            "global_time_target": (str,),
            "show_error_budget": (bool,),
            "slo_id": (str,),
            "time_windows": ([WidgetTimeWindows],),
            "title": (str,),
            "title_align": (WidgetTextAlign,),
            "title_size": (str,),
            "type": (SLOWidgetDefinitionType,),
            "view_mode": (WidgetViewMode,),
            "view_type": (str,),
        }

    attribute_map = {
        "global_time_target": "global_time_target",
        "show_error_budget": "show_error_budget",
        "slo_id": "slo_id",
        "time_windows": "time_windows",
        "title": "title",
        "title_align": "title_align",
        "title_size": "title_size",
        "type": "type",
        "view_mode": "view_mode",
        "view_type": "view_type",
    }

    def __init__(
        self_,
        type: SLOWidgetDefinitionType,
        global_time_target: Union[str, UnsetType] = unset,
        show_error_budget: Union[bool, UnsetType] = unset,
        slo_id: Union[str, UnsetType] = unset,
        time_windows: Union[List[WidgetTimeWindows], UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        title_align: Union[WidgetTextAlign, UnsetType] = unset,
        title_size: Union[str, UnsetType] = unset,
        view_mode: Union[WidgetViewMode, UnsetType] = unset,
        **kwargs,
    ):
        """
        Use the SLO and uptime widget to track your SLOs (Service Level Objectives) and uptime on screenboards and timeboards.

        :param global_time_target: Defined global time target.
        :type global_time_target: str, optional

        :param show_error_budget: Defined error budget.
        :type show_error_budget: bool, optional

        :param slo_id: ID of the SLO displayed.
        :type slo_id: str, optional

        :param time_windows: Times being monitored.
        :type time_windows: [WidgetTimeWindows], optional

        :param title: Title of the widget.
        :type title: str, optional

        :param title_align: How to align the text on the widget.
        :type title_align: WidgetTextAlign, optional

        :param title_size: Size of the title.
        :type title_size: str, optional

        :param type: Type of the SLO widget.
        :type type: SLOWidgetDefinitionType

        :param view_mode: Define how you want the SLO to be displayed.
        :type view_mode: WidgetViewMode, optional

        :param view_type: Type of view displayed by the widget.
        :type view_type: str
        """
        if global_time_target is not unset:
            kwargs["global_time_target"] = global_time_target
        if show_error_budget is not unset:
            kwargs["show_error_budget"] = show_error_budget
        if slo_id is not unset:
            kwargs["slo_id"] = slo_id
        if time_windows is not unset:
            kwargs["time_windows"] = time_windows
        if title is not unset:
            kwargs["title"] = title
        if title_align is not unset:
            kwargs["title_align"] = title_align
        if title_size is not unset:
            kwargs["title_size"] = title_size
        if view_mode is not unset:
            kwargs["view_mode"] = view_mode
        super().__init__(kwargs)
        view_type = kwargs.get("view_type", "detail")

        self_.type = type
        self_.view_type = view_type
