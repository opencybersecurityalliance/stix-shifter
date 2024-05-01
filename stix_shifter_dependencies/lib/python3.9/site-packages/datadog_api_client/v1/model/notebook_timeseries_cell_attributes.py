# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.timeseries_widget_definition import TimeseriesWidgetDefinition
    from datadog_api_client.v1.model.notebook_graph_size import NotebookGraphSize
    from datadog_api_client.v1.model.notebook_split_by import NotebookSplitBy
    from datadog_api_client.v1.model.notebook_cell_time import NotebookCellTime
    from datadog_api_client.v1.model.notebook_relative_time import NotebookRelativeTime
    from datadog_api_client.v1.model.notebook_absolute_time import NotebookAbsoluteTime


class NotebookTimeseriesCellAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.timeseries_widget_definition import TimeseriesWidgetDefinition
        from datadog_api_client.v1.model.notebook_graph_size import NotebookGraphSize
        from datadog_api_client.v1.model.notebook_split_by import NotebookSplitBy
        from datadog_api_client.v1.model.notebook_cell_time import NotebookCellTime

        return {
            "definition": (TimeseriesWidgetDefinition,),
            "graph_size": (NotebookGraphSize,),
            "split_by": (NotebookSplitBy,),
            "time": (NotebookCellTime,),
        }

    attribute_map = {
        "definition": "definition",
        "graph_size": "graph_size",
        "split_by": "split_by",
        "time": "time",
    }

    def __init__(
        self_,
        definition: TimeseriesWidgetDefinition,
        graph_size: Union[NotebookGraphSize, UnsetType] = unset,
        split_by: Union[NotebookSplitBy, UnsetType] = unset,
        time: Union[Union[NotebookCellTime, NotebookRelativeTime, NotebookAbsoluteTime], none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        The attributes of a notebook ``timeseries`` cell.

        :param definition: The timeseries visualization allows you to display the evolution of one or more metrics, log events, or Indexed Spans over time.
        :type definition: TimeseriesWidgetDefinition

        :param graph_size: The size of the graph.
        :type graph_size: NotebookGraphSize, optional

        :param split_by: Object describing how to split the graph to display multiple visualizations per request.
        :type split_by: NotebookSplitBy, optional

        :param time: Timeframe for the notebook cell. When 'null', the notebook global time is used.
        :type time: NotebookCellTime, none_type, optional
        """
        if graph_size is not unset:
            kwargs["graph_size"] = graph_size
        if split_by is not unset:
            kwargs["split_by"] = split_by
        if time is not unset:
            kwargs["time"] = time
        super().__init__(kwargs)

        self_.definition = definition
