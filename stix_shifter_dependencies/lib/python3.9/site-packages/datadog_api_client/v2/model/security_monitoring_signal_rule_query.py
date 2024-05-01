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
    from datadog_api_client.v2.model.security_monitoring_rule_query_aggregation import (
        SecurityMonitoringRuleQueryAggregation,
    )


class SecurityMonitoringSignalRuleQuery(ModelNormal):
    validations = {
        "correlated_query_index": {
            "inclusive_maximum": 9,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.security_monitoring_rule_query_aggregation import (
            SecurityMonitoringRuleQueryAggregation,
        )

        return {
            "aggregation": (SecurityMonitoringRuleQueryAggregation,),
            "correlated_by_fields": ([str],),
            "correlated_query_index": (int,),
            "metrics": ([str],),
            "name": (str,),
            "rule_id": (str,),
        }

    attribute_map = {
        "aggregation": "aggregation",
        "correlated_by_fields": "correlatedByFields",
        "correlated_query_index": "correlatedQueryIndex",
        "metrics": "metrics",
        "name": "name",
        "rule_id": "ruleId",
    }

    def __init__(
        self_,
        rule_id: str,
        aggregation: Union[SecurityMonitoringRuleQueryAggregation, UnsetType] = unset,
        correlated_by_fields: Union[List[str], UnsetType] = unset,
        correlated_query_index: Union[int, UnsetType] = unset,
        metrics: Union[List[str], UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Query for matching rule on signals.

        :param aggregation: The aggregation type.
        :type aggregation: SecurityMonitoringRuleQueryAggregation, optional

        :param correlated_by_fields: Fields to group by.
        :type correlated_by_fields: [str], optional

        :param correlated_query_index: Index of the rule query used to retrieve the correlated field.
        :type correlated_query_index: int, optional

        :param metrics: Group of target fields to aggregate over.
        :type metrics: [str], optional

        :param name: Name of the query.
        :type name: str, optional

        :param rule_id: Rule ID to match on signals.
        :type rule_id: str
        """
        if aggregation is not unset:
            kwargs["aggregation"] = aggregation
        if correlated_by_fields is not unset:
            kwargs["correlated_by_fields"] = correlated_by_fields
        if correlated_query_index is not unset:
            kwargs["correlated_query_index"] = correlated_query_index
        if metrics is not unset:
            kwargs["metrics"] = metrics
        if name is not unset:
            kwargs["name"] = name
        super().__init__(kwargs)

        self_.rule_id = rule_id
