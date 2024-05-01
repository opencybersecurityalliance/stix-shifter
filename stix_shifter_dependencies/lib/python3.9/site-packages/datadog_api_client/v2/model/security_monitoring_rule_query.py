# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelComposed,
    cached_property,
)


class SecurityMonitoringRuleQuery(ModelComposed):
    def __init__(self, **kwargs):
        """
        Query for matching rule.

        :param aggregation: The aggregation type.
        :type aggregation: SecurityMonitoringRuleQueryAggregation, optional

        :param distinct_fields: Field for which the cardinality is measured. Sent as an array.
        :type distinct_fields: [str], optional

        :param group_by_fields: Fields to group by.
        :type group_by_fields: [str], optional

        :param metric: (Deprecated) The target field to aggregate over when using the sum or max
            aggregations. `metrics` field should be used instead.
        :type metric: str, optional

        :param metrics: Group of target fields to aggregate over when using the sum, max, geo data, or new value aggregations. The sum, max, and geo data aggregations only accept one value in this list, whereas the new value aggregation accepts up to five values.
        :type metrics: [str], optional

        :param name: Name of the query.
        :type name: str, optional

        :param query: Query to run on logs.
        :type query: str

        :param correlated_by_fields: Fields to group by.
        :type correlated_by_fields: [str], optional

        :param correlated_query_index: Index of the rule query used to retrieve the correlated field.
        :type correlated_query_index: int, optional

        :param rule_id: Rule ID to match on signals.
        :type rule_id: str
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
        from datadog_api_client.v2.model.security_monitoring_standard_rule_query import (
            SecurityMonitoringStandardRuleQuery,
        )
        from datadog_api_client.v2.model.security_monitoring_signal_rule_query import SecurityMonitoringSignalRuleQuery

        return {
            "oneOf": [
                SecurityMonitoringStandardRuleQuery,
                SecurityMonitoringSignalRuleQuery,
            ],
        }
