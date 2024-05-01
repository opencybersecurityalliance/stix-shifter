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
    from datadog_api_client.v1.model.widget_definition import WidgetDefinition
    from datadog_api_client.v1.model.widget_layout import WidgetLayout
    from datadog_api_client.v1.model.alert_graph_widget_definition import AlertGraphWidgetDefinition
    from datadog_api_client.v1.model.alert_value_widget_definition import AlertValueWidgetDefinition
    from datadog_api_client.v1.model.change_widget_definition import ChangeWidgetDefinition
    from datadog_api_client.v1.model.check_status_widget_definition import CheckStatusWidgetDefinition
    from datadog_api_client.v1.model.distribution_widget_definition import DistributionWidgetDefinition
    from datadog_api_client.v1.model.event_stream_widget_definition import EventStreamWidgetDefinition
    from datadog_api_client.v1.model.event_timeline_widget_definition import EventTimelineWidgetDefinition
    from datadog_api_client.v1.model.free_text_widget_definition import FreeTextWidgetDefinition
    from datadog_api_client.v1.model.geomap_widget_definition import GeomapWidgetDefinition
    from datadog_api_client.v1.model.group_widget_definition import GroupWidgetDefinition
    from datadog_api_client.v1.model.heat_map_widget_definition import HeatMapWidgetDefinition
    from datadog_api_client.v1.model.host_map_widget_definition import HostMapWidgetDefinition
    from datadog_api_client.v1.model.i_frame_widget_definition import IFrameWidgetDefinition
    from datadog_api_client.v1.model.image_widget_definition import ImageWidgetDefinition
    from datadog_api_client.v1.model.log_stream_widget_definition import LogStreamWidgetDefinition
    from datadog_api_client.v1.model.monitor_summary_widget_definition import MonitorSummaryWidgetDefinition
    from datadog_api_client.v1.model.note_widget_definition import NoteWidgetDefinition
    from datadog_api_client.v1.model.query_value_widget_definition import QueryValueWidgetDefinition
    from datadog_api_client.v1.model.run_workflow_widget_definition import RunWorkflowWidgetDefinition
    from datadog_api_client.v1.model.scatter_plot_widget_definition import ScatterPlotWidgetDefinition
    from datadog_api_client.v1.model.slo_widget_definition import SLOWidgetDefinition
    from datadog_api_client.v1.model.slo_list_widget_definition import SLOListWidgetDefinition
    from datadog_api_client.v1.model.service_map_widget_definition import ServiceMapWidgetDefinition
    from datadog_api_client.v1.model.service_summary_widget_definition import ServiceSummaryWidgetDefinition
    from datadog_api_client.v1.model.sunburst_widget_definition import SunburstWidgetDefinition
    from datadog_api_client.v1.model.table_widget_definition import TableWidgetDefinition
    from datadog_api_client.v1.model.timeseries_widget_definition import TimeseriesWidgetDefinition
    from datadog_api_client.v1.model.toplist_widget_definition import ToplistWidgetDefinition
    from datadog_api_client.v1.model.tree_map_widget_definition import TreeMapWidgetDefinition
    from datadog_api_client.v1.model.list_stream_widget_definition import ListStreamWidgetDefinition
    from datadog_api_client.v1.model.funnel_widget_definition import FunnelWidgetDefinition
    from datadog_api_client.v1.model.topology_map_widget_definition import TopologyMapWidgetDefinition


class Widget(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_definition import WidgetDefinition
        from datadog_api_client.v1.model.widget_layout import WidgetLayout

        return {
            "definition": (WidgetDefinition,),
            "id": (int,),
            "layout": (WidgetLayout,),
        }

    attribute_map = {
        "definition": "definition",
        "id": "id",
        "layout": "layout",
    }

    def __init__(
        self_,
        definition: Union[
            WidgetDefinition,
            AlertGraphWidgetDefinition,
            AlertValueWidgetDefinition,
            ChangeWidgetDefinition,
            CheckStatusWidgetDefinition,
            DistributionWidgetDefinition,
            EventStreamWidgetDefinition,
            EventTimelineWidgetDefinition,
            FreeTextWidgetDefinition,
            GeomapWidgetDefinition,
            GroupWidgetDefinition,
            HeatMapWidgetDefinition,
            HostMapWidgetDefinition,
            IFrameWidgetDefinition,
            ImageWidgetDefinition,
            LogStreamWidgetDefinition,
            MonitorSummaryWidgetDefinition,
            NoteWidgetDefinition,
            QueryValueWidgetDefinition,
            RunWorkflowWidgetDefinition,
            ScatterPlotWidgetDefinition,
            SLOWidgetDefinition,
            SLOListWidgetDefinition,
            ServiceMapWidgetDefinition,
            ServiceSummaryWidgetDefinition,
            SunburstWidgetDefinition,
            TableWidgetDefinition,
            TimeseriesWidgetDefinition,
            ToplistWidgetDefinition,
            TreeMapWidgetDefinition,
            ListStreamWidgetDefinition,
            FunnelWidgetDefinition,
            TopologyMapWidgetDefinition,
        ],
        id: Union[int, UnsetType] = unset,
        layout: Union[WidgetLayout, UnsetType] = unset,
        **kwargs,
    ):
        """
        Information about widget.

        **Note** : The ``layout`` property is required for widgets in dashboards with ``free`` ``layout_type``.
              For the **new dashboard layout** , the ``layout`` property depends on the ``reflow_type`` of the dashboard.

        .. code-block::

             - If `reflow_type` is `fixed`, `layout` is required.
             - If `reflow_type` is `auto`, `layout` should not be set.

        :param definition: `Definition of the widget <https://docs.datadoghq.com/dashboards/widgets/>`_.
        :type definition: WidgetDefinition

        :param id: ID of the widget.
        :type id: int, optional

        :param layout: The layout for a widget on a ``free`` or **new dashboard layout** dashboard.
        :type layout: WidgetLayout, optional
        """
        if id is not unset:
            kwargs["id"] = id
        if layout is not unset:
            kwargs["layout"] = layout
        super().__init__(kwargs)

        self_.definition = definition
