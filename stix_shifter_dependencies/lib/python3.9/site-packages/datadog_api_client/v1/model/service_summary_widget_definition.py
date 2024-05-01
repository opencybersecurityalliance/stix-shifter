# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.widget_service_summary_display_format import WidgetServiceSummaryDisplayFormat
    from datadog_api_client.v1.model.widget_size_format import WidgetSizeFormat
    from datadog_api_client.v1.model.widget_time import WidgetTime
    from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
    from datadog_api_client.v1.model.service_summary_widget_definition_type import ServiceSummaryWidgetDefinitionType


class ServiceSummaryWidgetDefinition(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_service_summary_display_format import WidgetServiceSummaryDisplayFormat
        from datadog_api_client.v1.model.widget_size_format import WidgetSizeFormat
        from datadog_api_client.v1.model.widget_time import WidgetTime
        from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
        from datadog_api_client.v1.model.service_summary_widget_definition_type import (
            ServiceSummaryWidgetDefinitionType,
        )

        return {
            "display_format": (WidgetServiceSummaryDisplayFormat,),
            "env": (str,),
            "service": (str,),
            "show_breakdown": (bool,),
            "show_distribution": (bool,),
            "show_errors": (bool,),
            "show_hits": (bool,),
            "show_latency": (bool,),
            "show_resource_list": (bool,),
            "size_format": (WidgetSizeFormat,),
            "span_name": (str,),
            "time": (WidgetTime,),
            "title": (str,),
            "title_align": (WidgetTextAlign,),
            "title_size": (str,),
            "type": (ServiceSummaryWidgetDefinitionType,),
        }

    attribute_map = {
        "display_format": "display_format",
        "env": "env",
        "service": "service",
        "show_breakdown": "show_breakdown",
        "show_distribution": "show_distribution",
        "show_errors": "show_errors",
        "show_hits": "show_hits",
        "show_latency": "show_latency",
        "show_resource_list": "show_resource_list",
        "size_format": "size_format",
        "span_name": "span_name",
        "time": "time",
        "title": "title",
        "title_align": "title_align",
        "title_size": "title_size",
        "type": "type",
    }

    def __init__(
        self_,
        env: str,
        service: str,
        span_name: str,
        type: ServiceSummaryWidgetDefinitionType,
        display_format: Union[WidgetServiceSummaryDisplayFormat, UnsetType] = unset,
        show_breakdown: Union[bool, UnsetType] = unset,
        show_distribution: Union[bool, UnsetType] = unset,
        show_errors: Union[bool, UnsetType] = unset,
        show_hits: Union[bool, UnsetType] = unset,
        show_latency: Union[bool, UnsetType] = unset,
        show_resource_list: Union[bool, UnsetType] = unset,
        size_format: Union[WidgetSizeFormat, UnsetType] = unset,
        time: Union[WidgetTime, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        title_align: Union[WidgetTextAlign, UnsetType] = unset,
        title_size: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        The service summary displays the graphs of a chosen service in your screenboard. Only available on FREE layout dashboards.

        :param display_format: Number of columns to display.
        :type display_format: WidgetServiceSummaryDisplayFormat, optional

        :param env: APM environment.
        :type env: str

        :param service: APM service.
        :type service: str

        :param show_breakdown: Whether to show the latency breakdown or not.
        :type show_breakdown: bool, optional

        :param show_distribution: Whether to show the latency distribution or not.
        :type show_distribution: bool, optional

        :param show_errors: Whether to show the error metrics or not.
        :type show_errors: bool, optional

        :param show_hits: Whether to show the hits metrics or not.
        :type show_hits: bool, optional

        :param show_latency: Whether to show the latency metrics or not.
        :type show_latency: bool, optional

        :param show_resource_list: Whether to show the resource list or not.
        :type show_resource_list: bool, optional

        :param size_format: Size of the widget.
        :type size_format: WidgetSizeFormat, optional

        :param span_name: APM span name.
        :type span_name: str

        :param time: Time setting for the widget.
        :type time: WidgetTime, optional

        :param title: Title of the widget.
        :type title: str, optional

        :param title_align: How to align the text on the widget.
        :type title_align: WidgetTextAlign, optional

        :param title_size: Size of the title.
        :type title_size: str, optional

        :param type: Type of the service summary widget.
        :type type: ServiceSummaryWidgetDefinitionType
        """
        if display_format is not unset:
            kwargs["display_format"] = display_format
        if show_breakdown is not unset:
            kwargs["show_breakdown"] = show_breakdown
        if show_distribution is not unset:
            kwargs["show_distribution"] = show_distribution
        if show_errors is not unset:
            kwargs["show_errors"] = show_errors
        if show_hits is not unset:
            kwargs["show_hits"] = show_hits
        if show_latency is not unset:
            kwargs["show_latency"] = show_latency
        if show_resource_list is not unset:
            kwargs["show_resource_list"] = show_resource_list
        if size_format is not unset:
            kwargs["size_format"] = size_format
        if time is not unset:
            kwargs["time"] = time
        if title is not unset:
            kwargs["title"] = title
        if title_align is not unset:
            kwargs["title_align"] = title_align
        if title_size is not unset:
            kwargs["title_size"] = title_size
        super().__init__(kwargs)

        self_.env = env
        self_.service = service
        self_.span_name = span_name
        self_.type = type
