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
    from datadog_api_client.v1.model.log_stream_widget_definition import LogStreamWidgetDefinition
    from datadog_api_client.v1.model.notebook_graph_size import NotebookGraphSize
    from datadog_api_client.v1.model.notebook_cell_time import NotebookCellTime
    from datadog_api_client.v1.model.notebook_relative_time import NotebookRelativeTime
    from datadog_api_client.v1.model.notebook_absolute_time import NotebookAbsoluteTime


class NotebookLogStreamCellAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.log_stream_widget_definition import LogStreamWidgetDefinition
        from datadog_api_client.v1.model.notebook_graph_size import NotebookGraphSize
        from datadog_api_client.v1.model.notebook_cell_time import NotebookCellTime

        return {
            "definition": (LogStreamWidgetDefinition,),
            "graph_size": (NotebookGraphSize,),
            "time": (NotebookCellTime,),
        }

    attribute_map = {
        "definition": "definition",
        "graph_size": "graph_size",
        "time": "time",
    }

    def __init__(
        self_,
        definition: LogStreamWidgetDefinition,
        graph_size: Union[NotebookGraphSize, UnsetType] = unset,
        time: Union[Union[NotebookCellTime, NotebookRelativeTime, NotebookAbsoluteTime], none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        The attributes of a notebook ``log_stream`` cell.

        :param definition: The Log Stream displays a log flow matching the defined query. Only available on FREE layout dashboards.
        :type definition: LogStreamWidgetDefinition

        :param graph_size: The size of the graph.
        :type graph_size: NotebookGraphSize, optional

        :param time: Timeframe for the notebook cell. When 'null', the notebook global time is used.
        :type time: NotebookCellTime, none_type, optional
        """
        if graph_size is not unset:
            kwargs["graph_size"] = graph_size
        if time is not unset:
            kwargs["time"] = time
        super().__init__(kwargs)

        self_.definition = definition
