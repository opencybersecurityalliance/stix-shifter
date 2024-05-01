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
    from datadog_api_client.v1.model.widget_marker import WidgetMarker
    from datadog_api_client.v1.model.distribution_widget_request import DistributionWidgetRequest
    from datadog_api_client.v1.model.widget_time import WidgetTime
    from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
    from datadog_api_client.v1.model.distribution_widget_definition_type import DistributionWidgetDefinitionType
    from datadog_api_client.v1.model.distribution_widget_x_axis import DistributionWidgetXAxis
    from datadog_api_client.v1.model.distribution_widget_y_axis import DistributionWidgetYAxis


class DistributionWidgetDefinition(ModelNormal):
    validations = {
        "requests": {
            "max_items": 1,
            "min_items": 1,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_marker import WidgetMarker
        from datadog_api_client.v1.model.distribution_widget_request import DistributionWidgetRequest
        from datadog_api_client.v1.model.widget_time import WidgetTime
        from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
        from datadog_api_client.v1.model.distribution_widget_definition_type import DistributionWidgetDefinitionType
        from datadog_api_client.v1.model.distribution_widget_x_axis import DistributionWidgetXAxis
        from datadog_api_client.v1.model.distribution_widget_y_axis import DistributionWidgetYAxis

        return {
            "legend_size": (str,),
            "markers": ([WidgetMarker],),
            "requests": ([DistributionWidgetRequest],),
            "show_legend": (bool,),
            "time": (WidgetTime,),
            "title": (str,),
            "title_align": (WidgetTextAlign,),
            "title_size": (str,),
            "type": (DistributionWidgetDefinitionType,),
            "xaxis": (DistributionWidgetXAxis,),
            "yaxis": (DistributionWidgetYAxis,),
        }

    attribute_map = {
        "legend_size": "legend_size",
        "markers": "markers",
        "requests": "requests",
        "show_legend": "show_legend",
        "time": "time",
        "title": "title",
        "title_align": "title_align",
        "title_size": "title_size",
        "type": "type",
        "xaxis": "xaxis",
        "yaxis": "yaxis",
    }

    def __init__(
        self_,
        requests: List[DistributionWidgetRequest],
        type: DistributionWidgetDefinitionType,
        legend_size: Union[str, UnsetType] = unset,
        markers: Union[List[WidgetMarker], UnsetType] = unset,
        show_legend: Union[bool, UnsetType] = unset,
        time: Union[WidgetTime, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        title_align: Union[WidgetTextAlign, UnsetType] = unset,
        title_size: Union[str, UnsetType] = unset,
        xaxis: Union[DistributionWidgetXAxis, UnsetType] = unset,
        yaxis: Union[DistributionWidgetYAxis, UnsetType] = unset,
        **kwargs,
    ):
        """
        The Distribution visualization is another way of showing metrics
        aggregated across one or several tags, such as hosts.
        Unlike the heat map, a distribution graph’s x-axis is quantity rather than time.

        :param legend_size: (Deprecated) The widget legend was replaced by a tooltip and sidebar. **Deprecated**.
        :type legend_size: str, optional

        :param markers: List of markers.
        :type markers: [WidgetMarker], optional

        :param requests: Array of one request object to display in the widget.

            See the dedicated `Request JSON schema documentation <https://docs.datadoghq.com/dashboards/graphing_json/request_json>`_
             to learn how to build the ``REQUEST_SCHEMA``.
        :type requests: [DistributionWidgetRequest]

        :param show_legend: (Deprecated) The widget legend was replaced by a tooltip and sidebar. **Deprecated**.
        :type show_legend: bool, optional

        :param time: Time setting for the widget.
        :type time: WidgetTime, optional

        :param title: Title of the widget.
        :type title: str, optional

        :param title_align: How to align the text on the widget.
        :type title_align: WidgetTextAlign, optional

        :param title_size: Size of the title.
        :type title_size: str, optional

        :param type: Type of the distribution widget.
        :type type: DistributionWidgetDefinitionType

        :param xaxis: X Axis controls for the distribution widget.
        :type xaxis: DistributionWidgetXAxis, optional

        :param yaxis: Y Axis controls for the distribution widget.
        :type yaxis: DistributionWidgetYAxis, optional
        """
        if legend_size is not unset:
            kwargs["legend_size"] = legend_size
        if markers is not unset:
            kwargs["markers"] = markers
        if show_legend is not unset:
            kwargs["show_legend"] = show_legend
        if time is not unset:
            kwargs["time"] = time
        if title is not unset:
            kwargs["title"] = title
        if title_align is not unset:
            kwargs["title_align"] = title_align
        if title_size is not unset:
            kwargs["title_size"] = title_size
        if xaxis is not unset:
            kwargs["xaxis"] = xaxis
        if yaxis is not unset:
            kwargs["yaxis"] = yaxis
        super().__init__(kwargs)

        self_.requests = requests
        self_.type = type
