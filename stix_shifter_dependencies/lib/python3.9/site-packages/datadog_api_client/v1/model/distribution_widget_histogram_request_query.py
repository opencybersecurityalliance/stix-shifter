# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelComposed,
    cached_property,
)


class DistributionWidgetHistogramRequestQuery(ModelComposed):
    def __init__(self, **kwargs):
        """
        Query definition for Distribution Widget Histogram Request

        :param aggregator: The aggregation methods available for metrics queries.
        :type aggregator: FormulaAndFunctionMetricAggregation, optional

        :param data_source: Data source for metrics queries.
        :type data_source: FormulaAndFunctionMetricDataSource

        :param name: Name of the query for use in formulas.
        :type name: str

        :param query: Metrics query definition.
        :type query: str

        :param compute: Compute options.
        :type compute: FormulaAndFunctionEventQueryDefinitionCompute

        :param group_by: Group by options.
        :type group_by: [FormulaAndFunctionEventQueryGroupBy], optional

        :param indexes: An array of index names to query in the stream. Omit or use `[]` to query all indexes at once.
        :type indexes: [str], optional

        :param search: Search options.
        :type search: FormulaAndFunctionEventQueryDefinitionSearch, optional

        :param storage: Option for storage location. Feature in Private Beta.
        :type storage: str, optional

        :param env: APM environment.
        :type env: str

        :param operation_name: Name of operation on service.
        :type operation_name: str, optional

        :param primary_tag_name: Name of the second primary tag used within APM. Required when `primary_tag_value` is specified. See https://docs.datadoghq.com/tracing/guide/setting_primary_tags_to_scope/#add-a-second-primary-tag-in-datadog
        :type primary_tag_name: str, optional

        :param primary_tag_value: Value of the second primary tag by which to filter APM data. `primary_tag_name` must also be specified.
        :type primary_tag_value: str, optional

        :param resource_name: APM resource name.
        :type resource_name: str, optional

        :param service: APM service name.
        :type service: str

        :param stat: APM resource stat name.
        :type stat: FormulaAndFunctionApmResourceStatName
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
        from datadog_api_client.v1.model.formula_and_function_metric_query_definition import (
            FormulaAndFunctionMetricQueryDefinition,
        )
        from datadog_api_client.v1.model.formula_and_function_event_query_definition import (
            FormulaAndFunctionEventQueryDefinition,
        )
        from datadog_api_client.v1.model.formula_and_function_apm_resource_stats_query_definition import (
            FormulaAndFunctionApmResourceStatsQueryDefinition,
        )

        return {
            "oneOf": [
                FormulaAndFunctionMetricQueryDefinition,
                FormulaAndFunctionEventQueryDefinition,
                FormulaAndFunctionApmResourceStatsQueryDefinition,
            ],
        }
