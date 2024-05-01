# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelComposed,
    cached_property,
)


class WidgetDefinition(ModelComposed):
    def __init__(self, **kwargs):
        """
        `Definition of the widget <https://docs.datadoghq.com/dashboards/widgets/>`_.

        :param alert_id: ID of the alert to use in the widget.
        :type alert_id: str

        :param time: Time setting for the widget.
        :type time: WidgetTime, optional

        :param title: The title of the widget.
        :type title: str, optional

        :param title_align: How to align the text on the widget.
        :type title_align: WidgetTextAlign, optional

        :param title_size: Size of the title.
        :type title_size: str, optional

        :param type: Type of the alert graph widget.
        :type type: AlertGraphWidgetDefinitionType

        :param viz_type: Whether to display the Alert Graph as a timeseries or a top list.
        :type viz_type: WidgetVizType

        :param precision: Number of decimal to show. If not defined, will use the raw value.
        :type precision: int, optional

        :param text_align: How to align the text on the widget.
        :type text_align: WidgetTextAlign, optional

        :param unit: Unit to display with the value.
        :type unit: str, optional

        :param custom_links: List of custom links.
        :type custom_links: [WidgetCustomLink], optional

        :param requests: Array of one request object to display in the widget.

            See the dedicated [Request JSON schema documentation](https://docs.datadoghq.com/dashboards/graphing_json/request_json)
             to learn how to build the `REQUEST_SCHEMA`.
        :type requests: [ChangeWidgetRequest]

        :param check: Name of the check to use in the widget.
        :type check: str

        :param group: Group reporting a single check.
        :type group: str, optional

        :param group_by: List of tag prefixes to group by in the case of a cluster check.
        :type group_by: [str], optional

        :param grouping: The kind of grouping to use.
        :type grouping: WidgetGrouping

        :param tags: List of tags used to filter the groups reporting a cluster check.
        :type tags: [str], optional

        :param legend_size: (Deprecated) The widget legend was replaced by a tooltip and sidebar.
        :type legend_size: str, optional

        :param markers: List of markers.
        :type markers: [WidgetMarker], optional

        :param show_legend: (Deprecated) The widget legend was replaced by a tooltip and sidebar.
        :type show_legend: bool, optional

        :param xaxis: X Axis controls for the distribution widget.
        :type xaxis: DistributionWidgetXAxis, optional

        :param yaxis: Y Axis controls for the distribution widget.
        :type yaxis: DistributionWidgetYAxis, optional

        :param event_size: Size to use to display an event.
        :type event_size: WidgetEventSize, optional

        :param query: Query to filter the event stream with.
        :type query: str

        :param tags_execution: The execution method for multi-value filters. Can be either and or or.
        :type tags_execution: str, optional

        :param color: Color of the text.
        :type color: str, optional

        :param font_size: Size of the text.
        :type font_size: str, optional

        :param text: Text to display.
        :type text: str

        :param style: The style to apply to the widget.
        :type style: GeomapWidgetDefinitionStyle

        :param view: The view of the world that the map should render.
        :type view: GeomapWidgetDefinitionView

        :param background_color: Background color of the group title.
        :type background_color: str, optional

        :param banner_img: URL of image to display as a banner for the group.
        :type banner_img: str, optional

        :param layout_type: Layout type of the group.
        :type layout_type: WidgetLayoutType

        :param show_title: Whether to show the title or not.
        :type show_title: bool, optional

        :param widgets: List of widget groups.
        :type widgets: [Widget]

        :param events: List of widget events.
        :type events: [WidgetEvent], optional

        :param no_group_hosts: Whether to show the hosts that don’t fit in a group.
        :type no_group_hosts: bool, optional

        :param no_metric_hosts: Whether to show the hosts with no metrics.
        :type no_metric_hosts: bool, optional

        :param node_type: Which type of node to use in the map.
        :type node_type: WidgetNodeType, optional

        :param notes: Notes on the title.
        :type notes: str, optional

        :param scope: List of tags used to filter the map.
        :type scope: [str], optional

        :param url: URL of the iframe.
        :type url: str

        :param has_background: Whether to display a background or not.
        :type has_background: bool, optional

        :param has_border: Whether to display a border or not.
        :type has_border: bool, optional

        :param horizontal_align: Horizontal alignment.
        :type horizontal_align: WidgetHorizontalAlign, optional

        :param margin: Size of the margins around the image.
            **Note**: `small` and `large` values are deprecated.
        :type margin: WidgetMargin, optional

        :param sizing: How to size the image on the widget. The values are based on the image `object-fit` CSS properties.
            **Note**: `zoom`, `fit` and `center` values are deprecated.
        :type sizing: WidgetImageSizing, optional

        :param url_dark_theme: URL of the image in dark mode.
        :type url_dark_theme: str, optional

        :param vertical_align: Vertical alignment.
        :type vertical_align: WidgetVerticalAlign, optional

        :param columns: Which columns to display on the widget.
        :type columns: [str], optional

        :param indexes: An array of index names to query in the stream. Use [] to query all indexes at once.
        :type indexes: [str], optional

        :param logset: ID of the log set to use.
        :type logset: str, optional

        :param message_display: Amount of log lines to display
        :type message_display: WidgetMessageDisplay, optional

        :param show_date_column: Whether to show the date column or not
        :type show_date_column: bool, optional

        :param show_message_column: Whether to show the message column or not
        :type show_message_column: bool, optional

        :param sort: Which column and order to sort by
        :type sort: WidgetFieldSort, optional

        :param color_preference: Which color to use on the widget.
        :type color_preference: WidgetColorPreference, optional

        :param count: The number of monitors to display.
        :type count: int, optional

        :param display_format: What to display on the widget.
        :type display_format: WidgetMonitorSummaryDisplayFormat, optional

        :param hide_zero_counts: Whether to show counts of 0 or not.
        :type hide_zero_counts: bool, optional

        :param show_last_triggered: Whether to show the time that has elapsed since the monitor/group triggered.
        :type show_last_triggered: bool, optional

        :param show_priority: Whether to show the priorities column.
        :type show_priority: bool, optional

        :param start: The start of the list. Typically 0.
        :type start: int, optional

        :param summary_type: Which summary type should be used.
        :type summary_type: WidgetSummaryType, optional

        :param content: Content of the note.
        :type content: str

        :param has_padding: Whether to add padding or not.
        :type has_padding: bool, optional

        :param show_tick: Whether to show a tick or not.
        :type show_tick: bool, optional

        :param tick_edge: Define how you want to align the text on the widget.
        :type tick_edge: WidgetTickEdge, optional

        :param tick_pos: Where to position the tick on an edge.
        :type tick_pos: str, optional

        :param autoscale: Whether to use auto-scaling or not.
        :type autoscale: bool, optional

        :param custom_unit: Display a unit of your choice on the widget.
        :type custom_unit: str, optional

        :param timeseries_background: Set a timeseries on the widget background.
        :type timeseries_background: TimeseriesBackground, optional

        :param inputs: Array of workflow inputs to map to dashboard template variables.
        :type inputs: [RunWorkflowWidgetInput], optional

        :param workflow_id: Workflow id.
        :type workflow_id: str

        :param color_by_groups: List of groups used for colors.
        :type color_by_groups: [str], optional

        :param global_time_target: Defined global time target.
        :type global_time_target: str, optional

        :param show_error_budget: Defined error budget.
        :type show_error_budget: bool, optional

        :param slo_id: ID of the SLO displayed.
        :type slo_id: str, optional

        :param time_windows: Times being monitored.
        :type time_windows: [WidgetTimeWindows], optional

        :param view_mode: Define how you want the SLO to be displayed.
        :type view_mode: WidgetViewMode, optional

        :param view_type: Type of view displayed by the widget.
        :type view_type: str

        :param filters: Your environment and primary tag (or * if enabled for your account).
        :type filters: [str]

        :param service: The ID of the service you want to map.
        :type service: str

        :param env: APM environment.
        :type env: str

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

        :param hide_total: Show the total value in this widget.
        :type hide_total: bool, optional

        :param legend: Configuration of the legend.
        :type legend: SunburstWidgetLegend, optional

        :param has_search_bar: Controls the display of the search bar.
        :type has_search_bar: TableWidgetHasSearchBar, optional

        :param legend_columns: Columns displayed in the legend.
        :type legend_columns: [TimeseriesWidgetLegendColumn], optional

        :param legend_layout: Layout of the legend.
        :type legend_layout: TimeseriesWidgetLegendLayout, optional

        :param right_yaxis: Axis controls for the widget.
        :type right_yaxis: WidgetAxis, optional

        :param color_by: (deprecated) The attribute formerly used to determine color in the widget.
        :type color_by: TreeMapColorBy, optional

        :param size_by: (deprecated) The attribute formerly used to determine size in the widget.
        :type size_by: TreeMapSizeBy, optional
        """
        super().__init__(kwargs)

    @cached_property
    def _composed_schemas(_):
        # we need this here to make our import statements work
        # we must store _composed_schemas in here so the code is only run
        # when we invoke this method. If we kept this at the class
        # level we would get an error because the class level
        # code would be run when this module is imported, and these composed
        # classes don't exist yet because their module has not finished
        # loading
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

        return {
            "oneOf": [
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
        }
