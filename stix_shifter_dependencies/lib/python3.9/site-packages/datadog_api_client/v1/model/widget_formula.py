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
    from datadog_api_client.v1.model.table_widget_cell_display_mode import TableWidgetCellDisplayMode
    from datadog_api_client.v1.model.widget_conditional_format import WidgetConditionalFormat
    from datadog_api_client.v1.model.widget_formula_limit import WidgetFormulaLimit
    from datadog_api_client.v1.model.widget_formula_style import WidgetFormulaStyle


class WidgetFormula(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.table_widget_cell_display_mode import TableWidgetCellDisplayMode
        from datadog_api_client.v1.model.widget_conditional_format import WidgetConditionalFormat
        from datadog_api_client.v1.model.widget_formula_limit import WidgetFormulaLimit
        from datadog_api_client.v1.model.widget_formula_style import WidgetFormulaStyle

        return {
            "alias": (str,),
            "cell_display_mode": (TableWidgetCellDisplayMode,),
            "conditional_formats": ([WidgetConditionalFormat],),
            "formula": (str,),
            "limit": (WidgetFormulaLimit,),
            "style": (WidgetFormulaStyle,),
        }

    attribute_map = {
        "alias": "alias",
        "cell_display_mode": "cell_display_mode",
        "conditional_formats": "conditional_formats",
        "formula": "formula",
        "limit": "limit",
        "style": "style",
    }

    def __init__(
        self_,
        formula: str,
        alias: Union[str, UnsetType] = unset,
        cell_display_mode: Union[TableWidgetCellDisplayMode, UnsetType] = unset,
        conditional_formats: Union[List[WidgetConditionalFormat], UnsetType] = unset,
        limit: Union[WidgetFormulaLimit, UnsetType] = unset,
        style: Union[WidgetFormulaStyle, UnsetType] = unset,
        **kwargs,
    ):
        """
        Formula to be used in a widget query.

        :param alias: Expression alias.
        :type alias: str, optional

        :param cell_display_mode: Define a display mode for the table cell.
        :type cell_display_mode: TableWidgetCellDisplayMode, optional

        :param conditional_formats: List of conditional formats.
        :type conditional_formats: [WidgetConditionalFormat], optional

        :param formula: String expression built from queries, formulas, and functions.
        :type formula: str

        :param limit: Options for limiting results returned.
        :type limit: WidgetFormulaLimit, optional

        :param style: Styling options for widget formulas.
        :type style: WidgetFormulaStyle, optional
        """
        if alias is not unset:
            kwargs["alias"] = alias
        if cell_display_mode is not unset:
            kwargs["cell_display_mode"] = cell_display_mode
        if conditional_formats is not unset:
            kwargs["conditional_formats"] = conditional_formats
        if limit is not unset:
            kwargs["limit"] = limit
        if style is not unset:
            kwargs["style"] = style
        super().__init__(kwargs)

        self_.formula = formula
