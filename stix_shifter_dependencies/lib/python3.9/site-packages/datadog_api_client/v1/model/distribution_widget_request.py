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
    from datadog_api_client.v1.model.log_query_definition import LogQueryDefinition
    from datadog_api_client.v1.model.apm_stats_query_definition import ApmStatsQueryDefinition
    from datadog_api_client.v1.model.process_query_definition import ProcessQueryDefinition
    from datadog_api_client.v1.model.distribution_widget_histogram_request_query import (
        DistributionWidgetHistogramRequestQuery,
    )
    from datadog_api_client.v1.model.distribution_widget_histogram_request_type import (
        DistributionWidgetHistogramRequestType,
    )
    from datadog_api_client.v1.model.widget_style import WidgetStyle
    from datadog_api_client.v1.model.formula_and_function_metric_query_definition import (
        FormulaAndFunctionMetricQueryDefinition,
    )
    from datadog_api_client.v1.model.formula_and_function_event_query_definition import (
        FormulaAndFunctionEventQueryDefinition,
    )
    from datadog_api_client.v1.model.formula_and_function_apm_resource_stats_query_definition import (
        FormulaAndFunctionApmResourceStatsQueryDefinition,
    )


class DistributionWidgetRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.log_query_definition import LogQueryDefinition
        from datadog_api_client.v1.model.apm_stats_query_definition import ApmStatsQueryDefinition
        from datadog_api_client.v1.model.process_query_definition import ProcessQueryDefinition
        from datadog_api_client.v1.model.distribution_widget_histogram_request_query import (
            DistributionWidgetHistogramRequestQuery,
        )
        from datadog_api_client.v1.model.distribution_widget_histogram_request_type import (
            DistributionWidgetHistogramRequestType,
        )
        from datadog_api_client.v1.model.widget_style import WidgetStyle

        return {
            "apm_query": (LogQueryDefinition,),
            "apm_stats_query": (ApmStatsQueryDefinition,),
            "event_query": (LogQueryDefinition,),
            "log_query": (LogQueryDefinition,),
            "network_query": (LogQueryDefinition,),
            "process_query": (ProcessQueryDefinition,),
            "profile_metrics_query": (LogQueryDefinition,),
            "q": (str,),
            "query": (DistributionWidgetHistogramRequestQuery,),
            "request_type": (DistributionWidgetHistogramRequestType,),
            "rum_query": (LogQueryDefinition,),
            "security_query": (LogQueryDefinition,),
            "style": (WidgetStyle,),
        }

    attribute_map = {
        "apm_query": "apm_query",
        "apm_stats_query": "apm_stats_query",
        "event_query": "event_query",
        "log_query": "log_query",
        "network_query": "network_query",
        "process_query": "process_query",
        "profile_metrics_query": "profile_metrics_query",
        "q": "q",
        "query": "query",
        "request_type": "request_type",
        "rum_query": "rum_query",
        "security_query": "security_query",
        "style": "style",
    }

    def __init__(
        self_,
        apm_query: Union[LogQueryDefinition, UnsetType] = unset,
        apm_stats_query: Union[ApmStatsQueryDefinition, UnsetType] = unset,
        event_query: Union[LogQueryDefinition, UnsetType] = unset,
        log_query: Union[LogQueryDefinition, UnsetType] = unset,
        network_query: Union[LogQueryDefinition, UnsetType] = unset,
        process_query: Union[ProcessQueryDefinition, UnsetType] = unset,
        profile_metrics_query: Union[LogQueryDefinition, UnsetType] = unset,
        q: Union[str, UnsetType] = unset,
        query: Union[
            DistributionWidgetHistogramRequestQuery,
            FormulaAndFunctionMetricQueryDefinition,
            FormulaAndFunctionEventQueryDefinition,
            FormulaAndFunctionApmResourceStatsQueryDefinition,
            UnsetType,
        ] = unset,
        request_type: Union[DistributionWidgetHistogramRequestType, UnsetType] = unset,
        rum_query: Union[LogQueryDefinition, UnsetType] = unset,
        security_query: Union[LogQueryDefinition, UnsetType] = unset,
        style: Union[WidgetStyle, UnsetType] = unset,
        **kwargs,
    ):
        """
        Updated distribution widget.

        :param apm_query: The log query.
        :type apm_query: LogQueryDefinition, optional

        :param apm_stats_query: The APM stats query for table and distributions widgets.
        :type apm_stats_query: ApmStatsQueryDefinition, optional

        :param event_query: The log query.
        :type event_query: LogQueryDefinition, optional

        :param log_query: The log query.
        :type log_query: LogQueryDefinition, optional

        :param network_query: The log query.
        :type network_query: LogQueryDefinition, optional

        :param process_query: The process query to use in the widget.
        :type process_query: ProcessQueryDefinition, optional

        :param profile_metrics_query: The log query.
        :type profile_metrics_query: LogQueryDefinition, optional

        :param q: Widget query.
        :type q: str, optional

        :param query: Query definition for Distribution Widget Histogram Request
        :type query: DistributionWidgetHistogramRequestQuery, optional

        :param request_type: Request type for the histogram request.
        :type request_type: DistributionWidgetHistogramRequestType, optional

        :param rum_query: The log query.
        :type rum_query: LogQueryDefinition, optional

        :param security_query: The log query.
        :type security_query: LogQueryDefinition, optional

        :param style: Widget style definition.
        :type style: WidgetStyle, optional
        """
        if apm_query is not unset:
            kwargs["apm_query"] = apm_query
        if apm_stats_query is not unset:
            kwargs["apm_stats_query"] = apm_stats_query
        if event_query is not unset:
            kwargs["event_query"] = event_query
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
        if query is not unset:
            kwargs["query"] = query
        if request_type is not unset:
            kwargs["request_type"] = request_type
        if rum_query is not unset:
            kwargs["rum_query"] = rum_query
        if security_query is not unset:
            kwargs["security_query"] = security_query
        if style is not unset:
            kwargs["style"] = style
        super().__init__(kwargs)
