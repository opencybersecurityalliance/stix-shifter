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
    from datadog_api_client.v1.model.log_query_definition import LogQueryDefinition
    from datadog_api_client.v1.model.widget_display_type import WidgetDisplayType
    from datadog_api_client.v1.model.widget_formula import WidgetFormula
    from datadog_api_client.v1.model.timeseries_widget_expression_alias import TimeseriesWidgetExpressionAlias
    from datadog_api_client.v1.model.process_query_definition import ProcessQueryDefinition
    from datadog_api_client.v1.model.formula_and_function_query_definition import FormulaAndFunctionQueryDefinition
    from datadog_api_client.v1.model.formula_and_function_response_format import FormulaAndFunctionResponseFormat
    from datadog_api_client.v1.model.widget_request_style import WidgetRequestStyle
    from datadog_api_client.v1.model.formula_and_function_metric_query_definition import (
        FormulaAndFunctionMetricQueryDefinition,
    )
    from datadog_api_client.v1.model.formula_and_function_event_query_definition import (
        FormulaAndFunctionEventQueryDefinition,
    )
    from datadog_api_client.v1.model.formula_and_function_process_query_definition import (
        FormulaAndFunctionProcessQueryDefinition,
    )
    from datadog_api_client.v1.model.formula_and_function_apm_dependency_stats_query_definition import (
        FormulaAndFunctionApmDependencyStatsQueryDefinition,
    )
    from datadog_api_client.v1.model.formula_and_function_apm_resource_stats_query_definition import (
        FormulaAndFunctionApmResourceStatsQueryDefinition,
    )


class TimeseriesWidgetRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.log_query_definition import LogQueryDefinition
        from datadog_api_client.v1.model.widget_display_type import WidgetDisplayType
        from datadog_api_client.v1.model.widget_formula import WidgetFormula
        from datadog_api_client.v1.model.timeseries_widget_expression_alias import TimeseriesWidgetExpressionAlias
        from datadog_api_client.v1.model.process_query_definition import ProcessQueryDefinition
        from datadog_api_client.v1.model.formula_and_function_query_definition import FormulaAndFunctionQueryDefinition
        from datadog_api_client.v1.model.formula_and_function_response_format import FormulaAndFunctionResponseFormat
        from datadog_api_client.v1.model.widget_request_style import WidgetRequestStyle

        return {
            "apm_query": (LogQueryDefinition,),
            "audit_query": (LogQueryDefinition,),
            "display_type": (WidgetDisplayType,),
            "event_query": (LogQueryDefinition,),
            "formulas": ([WidgetFormula],),
            "log_query": (LogQueryDefinition,),
            "metadata": ([TimeseriesWidgetExpressionAlias],),
            "network_query": (LogQueryDefinition,),
            "on_right_yaxis": (bool,),
            "process_query": (ProcessQueryDefinition,),
            "profile_metrics_query": (LogQueryDefinition,),
            "q": (str,),
            "queries": ([FormulaAndFunctionQueryDefinition],),
            "response_format": (FormulaAndFunctionResponseFormat,),
            "rum_query": (LogQueryDefinition,),
            "security_query": (LogQueryDefinition,),
            "style": (WidgetRequestStyle,),
        }

    attribute_map = {
        "apm_query": "apm_query",
        "audit_query": "audit_query",
        "display_type": "display_type",
        "event_query": "event_query",
        "formulas": "formulas",
        "log_query": "log_query",
        "metadata": "metadata",
        "network_query": "network_query",
        "on_right_yaxis": "on_right_yaxis",
        "process_query": "process_query",
        "profile_metrics_query": "profile_metrics_query",
        "q": "q",
        "queries": "queries",
        "response_format": "response_format",
        "rum_query": "rum_query",
        "security_query": "security_query",
        "style": "style",
    }

    def __init__(
        self_,
        apm_query: Union[LogQueryDefinition, UnsetType] = unset,
        audit_query: Union[LogQueryDefinition, UnsetType] = unset,
        display_type: Union[WidgetDisplayType, UnsetType] = unset,
        event_query: Union[LogQueryDefinition, UnsetType] = unset,
        formulas: Union[List[WidgetFormula], UnsetType] = unset,
        log_query: Union[LogQueryDefinition, UnsetType] = unset,
        metadata: Union[List[TimeseriesWidgetExpressionAlias], UnsetType] = unset,
        network_query: Union[LogQueryDefinition, UnsetType] = unset,
        on_right_yaxis: Union[bool, UnsetType] = unset,
        process_query: Union[ProcessQueryDefinition, UnsetType] = unset,
        profile_metrics_query: Union[LogQueryDefinition, UnsetType] = unset,
        q: Union[str, UnsetType] = unset,
        queries: Union[
            List[
                Union[
                    FormulaAndFunctionQueryDefinition,
                    FormulaAndFunctionMetricQueryDefinition,
                    FormulaAndFunctionEventQueryDefinition,
                    FormulaAndFunctionProcessQueryDefinition,
                    FormulaAndFunctionApmDependencyStatsQueryDefinition,
                    FormulaAndFunctionApmResourceStatsQueryDefinition,
                ]
            ],
            UnsetType,
        ] = unset,
        response_format: Union[FormulaAndFunctionResponseFormat, UnsetType] = unset,
        rum_query: Union[LogQueryDefinition, UnsetType] = unset,
        security_query: Union[LogQueryDefinition, UnsetType] = unset,
        style: Union[WidgetRequestStyle, UnsetType] = unset,
        **kwargs,
    ):
        """
        Updated timeseries widget.

        :param apm_query: The log query.
        :type apm_query: LogQueryDefinition, optional

        :param audit_query: The log query.
        :type audit_query: LogQueryDefinition, optional

        :param display_type: Type of display to use for the request.
        :type display_type: WidgetDisplayType, optional

        :param event_query: The log query.
        :type event_query: LogQueryDefinition, optional

        :param formulas: List of formulas that operate on queries.
        :type formulas: [WidgetFormula], optional

        :param log_query: The log query.
        :type log_query: LogQueryDefinition, optional

        :param metadata: Used to define expression aliases.
        :type metadata: [TimeseriesWidgetExpressionAlias], optional

        :param network_query: The log query.
        :type network_query: LogQueryDefinition, optional

        :param on_right_yaxis: Whether or not to display a second y-axis on the right.
        :type on_right_yaxis: bool, optional

        :param process_query: The process query to use in the widget.
        :type process_query: ProcessQueryDefinition, optional

        :param profile_metrics_query: The log query.
        :type profile_metrics_query: LogQueryDefinition, optional

        :param q: Widget query.
        :type q: str, optional

        :param queries: List of queries that can be returned directly or used in formulas.
        :type queries: [FormulaAndFunctionQueryDefinition], optional

        :param response_format: Timeseries or Scalar response.
        :type response_format: FormulaAndFunctionResponseFormat, optional

        :param rum_query: The log query.
        :type rum_query: LogQueryDefinition, optional

        :param security_query: The log query.
        :type security_query: LogQueryDefinition, optional

        :param style: Define request widget style.
        :type style: WidgetRequestStyle, optional
        """
        if apm_query is not unset:
            kwargs["apm_query"] = apm_query
        if audit_query is not unset:
            kwargs["audit_query"] = audit_query
        if display_type is not unset:
            kwargs["display_type"] = display_type
        if event_query is not unset:
            kwargs["event_query"] = event_query
        if formulas is not unset:
            kwargs["formulas"] = formulas
        if log_query is not unset:
            kwargs["log_query"] = log_query
        if metadata is not unset:
            kwargs["metadata"] = metadata
        if network_query is not unset:
            kwargs["network_query"] = network_query
        if on_right_yaxis is not unset:
            kwargs["on_right_yaxis"] = on_right_yaxis
        if process_query is not unset:
            kwargs["process_query"] = process_query
        if profile_metrics_query is not unset:
            kwargs["profile_metrics_query"] = profile_metrics_query
        if q is not unset:
            kwargs["q"] = q
        if queries is not unset:
            kwargs["queries"] = queries
        if response_format is not unset:
            kwargs["response_format"] = response_format
        if rum_query is not unset:
            kwargs["rum_query"] = rum_query
        if security_query is not unset:
            kwargs["security_query"] = security_query
        if style is not unset:
            kwargs["style"] = style
        super().__init__(kwargs)
