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
    from datadog_api_client.v1.model.widget_aggregator import WidgetAggregator
    from datadog_api_client.v1.model.log_query_definition import LogQueryDefinition
    from datadog_api_client.v1.model.widget_conditional_format import WidgetConditionalFormat
    from datadog_api_client.v1.model.widget_formula import WidgetFormula
    from datadog_api_client.v1.model.process_query_definition import ProcessQueryDefinition
    from datadog_api_client.v1.model.formula_and_function_query_definition import FormulaAndFunctionQueryDefinition
    from datadog_api_client.v1.model.formula_and_function_response_format import FormulaAndFunctionResponseFormat
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


class QueryValueWidgetRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.widget_aggregator import WidgetAggregator
        from datadog_api_client.v1.model.log_query_definition import LogQueryDefinition
        from datadog_api_client.v1.model.widget_conditional_format import WidgetConditionalFormat
        from datadog_api_client.v1.model.widget_formula import WidgetFormula
        from datadog_api_client.v1.model.process_query_definition import ProcessQueryDefinition
        from datadog_api_client.v1.model.formula_and_function_query_definition import FormulaAndFunctionQueryDefinition
        from datadog_api_client.v1.model.formula_and_function_response_format import FormulaAndFunctionResponseFormat

        return {
            "aggregator": (WidgetAggregator,),
            "apm_query": (LogQueryDefinition,),
            "audit_query": (LogQueryDefinition,),
            "conditional_formats": ([WidgetConditionalFormat],),
            "event_query": (LogQueryDefinition,),
            "formulas": ([WidgetFormula],),
            "log_query": (LogQueryDefinition,),
            "network_query": (LogQueryDefinition,),
            "process_query": (ProcessQueryDefinition,),
            "profile_metrics_query": (LogQueryDefinition,),
            "q": (str,),
            "queries": ([FormulaAndFunctionQueryDefinition],),
            "response_format": (FormulaAndFunctionResponseFormat,),
            "rum_query": (LogQueryDefinition,),
            "security_query": (LogQueryDefinition,),
        }

    attribute_map = {
        "aggregator": "aggregator",
        "apm_query": "apm_query",
        "audit_query": "audit_query",
        "conditional_formats": "conditional_formats",
        "event_query": "event_query",
        "formulas": "formulas",
        "log_query": "log_query",
        "network_query": "network_query",
        "process_query": "process_query",
        "profile_metrics_query": "profile_metrics_query",
        "q": "q",
        "queries": "queries",
        "response_format": "response_format",
        "rum_query": "rum_query",
        "security_query": "security_query",
    }

    def __init__(
        self_,
        aggregator: Union[WidgetAggregator, UnsetType] = unset,
        apm_query: Union[LogQueryDefinition, UnsetType] = unset,
        audit_query: Union[LogQueryDefinition, UnsetType] = unset,
        conditional_formats: Union[List[WidgetConditionalFormat], UnsetType] = unset,
        event_query: Union[LogQueryDefinition, UnsetType] = unset,
        formulas: Union[List[WidgetFormula], UnsetType] = unset,
        log_query: Union[LogQueryDefinition, UnsetType] = unset,
        network_query: Union[LogQueryDefinition, UnsetType] = unset,
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
        **kwargs,
    ):
        """
        Updated query value widget.

        :param aggregator: Aggregator used for the request.
        :type aggregator: WidgetAggregator, optional

        :param apm_query: The log query.
        :type apm_query: LogQueryDefinition, optional

        :param audit_query: The log query.
        :type audit_query: LogQueryDefinition, optional

        :param conditional_formats: List of conditional formats.
        :type conditional_formats: [WidgetConditionalFormat], optional

        :param event_query: The log query.
        :type event_query: LogQueryDefinition, optional

        :param formulas: List of formulas that operate on queries.
        :type formulas: [WidgetFormula], optional

        :param log_query: The log query.
        :type log_query: LogQueryDefinition, optional

        :param network_query: The log query.
        :type network_query: LogQueryDefinition, optional

        :param process_query: The process query to use in the widget.
        :type process_query: ProcessQueryDefinition, optional

        :param profile_metrics_query: The log query.
        :type profile_metrics_query: LogQueryDefinition, optional

        :param q: TODO.
        :type q: str, optional

        :param queries: List of queries that can be returned directly or used in formulas.
        :type queries: [FormulaAndFunctionQueryDefinition], optional

        :param response_format: Timeseries or Scalar response.
        :type response_format: FormulaAndFunctionResponseFormat, optional

        :param rum_query: The log query.
        :type rum_query: LogQueryDefinition, optional

        :param security_query: The log query.
        :type security_query: LogQueryDefinition, optional
        """
        if aggregator is not unset:
            kwargs["aggregator"] = aggregator
        if apm_query is not unset:
            kwargs["apm_query"] = apm_query
        if audit_query is not unset:
            kwargs["audit_query"] = audit_query
        if conditional_formats is not unset:
            kwargs["conditional_formats"] = conditional_formats
        if event_query is not unset:
            kwargs["event_query"] = event_query
        if formulas is not unset:
            kwargs["formulas"] = formulas
        if log_query is not unset:
            kwargs["log_query"] = log_query
        if network_query is not unset:
            kwargs["network_query"] = network_query
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
        super().__init__(kwargs)
