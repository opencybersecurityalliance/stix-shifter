# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelComposed,
    cached_property,
)


class FormulaAndFunctionQueryDefinition(ModelComposed):
    def __init__(self, **kwargs):
        """
        A formula and function query.

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

        :param is_normalized_cpu: Whether to normalize the CPU percentages.
        :type is_normalized_cpu: bool, optional

        :param limit: Number of hits to return.
        :type limit: int, optional

        :param metric: Process metric name.
        :type metric: str

        :param sort: Direction of sort.
        :type sort: QuerySortOrder, optional

        :param tag_filters: An array of tags to filter by.
        :type tag_filters: [str], optional

        :param text_filter: Text to use as filter.
        :type text_filter: str, optional

        :param env: APM environment.
        :type env: str

        :param is_upstream: Determines whether stats for upstream or downstream dependencies should be queried.
        :type is_upstream: bool, optional

        :param operation_name: Name of operation on service.
        :type operation_name: str

        :param primary_tag_name: The name of the second primary tag used within APM; required when `primary_tag_value` is specified. See https://docs.datadoghq.com/tracing/guide/setting_primary_tags_to_scope/#add-a-second-primary-tag-in-datadog.
        :type primary_tag_name: str, optional

        :param primary_tag_value: Filter APM data by the second primary tag. `primary_tag_name` must also be specified.
        :type primary_tag_value: str, optional

        :param resource_name: APM resource.
        :type resource_name: str

        :param service: APM service.
        :type service: str

        :param stat: APM statistic.
        :type stat: FormulaAndFunctionApmDependencyStatName
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
        from datadog_api_client.v1.model.formula_and_function_process_query_definition import (
            FormulaAndFunctionProcessQueryDefinition,
        )
        from datadog_api_client.v1.model.formula_and_function_apm_dependency_stats_query_definition import (
            FormulaAndFunctionApmDependencyStatsQueryDefinition,
        )
        from datadog_api_client.v1.model.formula_and_function_apm_resource_stats_query_definition import (
            FormulaAndFunctionApmResourceStatsQueryDefinition,
        )

        return {
            "oneOf": [
                FormulaAndFunctionMetricQueryDefinition,
                FormulaAndFunctionEventQueryDefinition,
                FormulaAndFunctionProcessQueryDefinition,
                FormulaAndFunctionApmDependencyStatsQueryDefinition,
                FormulaAndFunctionApmResourceStatsQueryDefinition,
            ],
        }
