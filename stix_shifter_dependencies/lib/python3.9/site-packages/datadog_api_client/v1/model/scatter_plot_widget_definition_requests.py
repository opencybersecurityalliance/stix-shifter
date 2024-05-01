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
    from datadog_api_client.v1.model.scatterplot_table_request import ScatterplotTableRequest
    from datadog_api_client.v1.model.scatter_plot_request import ScatterPlotRequest


class ScatterPlotWidgetDefinitionRequests(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.scatterplot_table_request import ScatterplotTableRequest
        from datadog_api_client.v1.model.scatter_plot_request import ScatterPlotRequest

        return {
            "table": (ScatterplotTableRequest,),
            "x": (ScatterPlotRequest,),
            "y": (ScatterPlotRequest,),
        }

    attribute_map = {
        "table": "table",
        "x": "x",
        "y": "y",
    }

    def __init__(
        self_,
        table: Union[ScatterplotTableRequest, UnsetType] = unset,
        x: Union[ScatterPlotRequest, UnsetType] = unset,
        y: Union[ScatterPlotRequest, UnsetType] = unset,
        **kwargs,
    ):
        """
        Widget definition.

        :param table: Scatterplot request containing formulas and functions.
        :type table: ScatterplotTableRequest, optional

        :param x: Updated scatter plot.
        :type x: ScatterPlotRequest, optional

        :param y: Updated scatter plot.
        :type y: ScatterPlotRequest, optional
        """
        if table is not unset:
            kwargs["table"] = table
        if x is not unset:
            kwargs["x"] = x
        if y is not unset:
            kwargs["y"] = y
        super().__init__(kwargs)
