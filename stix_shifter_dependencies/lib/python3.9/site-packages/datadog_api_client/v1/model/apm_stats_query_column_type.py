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
    from datadog_api_client.v1.model.table_widget_cell_display_mode import TableWidgetCellDisplayMode
    from datadog_api_client.v1.model.widget_sort import WidgetSort


class ApmStatsQueryColumnType(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.table_widget_cell_display_mode import TableWidgetCellDisplayMode
        from datadog_api_client.v1.model.widget_sort import WidgetSort

        return {
            "alias": (str,),
            "cell_display_mode": (TableWidgetCellDisplayMode,),
            "name": (str,),
            "order": (WidgetSort,),
        }

    attribute_map = {
        "alias": "alias",
        "cell_display_mode": "cell_display_mode",
        "name": "name",
        "order": "order",
    }

    def __init__(
        self_,
        name: str,
        alias: Union[str, UnsetType] = unset,
        cell_display_mode: Union[TableWidgetCellDisplayMode, UnsetType] = unset,
        order: Union[WidgetSort, UnsetType] = unset,
        **kwargs,
    ):
        """
        Column properties.

        :param alias: A user-assigned alias for the column.
        :type alias: str, optional

        :param cell_display_mode: Define a display mode for the table cell.
        :type cell_display_mode: TableWidgetCellDisplayMode, optional

        :param name: Column name.
        :type name: str

        :param order: Widget sorting methods.
        :type order: WidgetSort, optional
        """
        if alias is not unset:
            kwargs["alias"] = alias
        if cell_display_mode is not unset:
            kwargs["cell_display_mode"] = cell_display_mode
        if order is not unset:
            kwargs["order"] = order
        super().__init__(kwargs)

        self_.name = name
