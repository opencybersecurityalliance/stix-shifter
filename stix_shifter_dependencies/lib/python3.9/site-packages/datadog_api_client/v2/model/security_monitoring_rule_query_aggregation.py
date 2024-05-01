# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SecurityMonitoringRuleQueryAggregation(ModelSimple):
    """
    The aggregation type.

    :param value: Must be one of ["count", "cardinality", "sum", "max", "new_value", "geo_data", "event_count", "none"].
    :type value: str
    """

    allowed_values = {
        "count",
        "cardinality",
        "sum",
        "max",
        "new_value",
        "geo_data",
        "event_count",
        "none",
    }
    COUNT: ClassVar["SecurityMonitoringRuleQueryAggregation"]
    CARDINALITY: ClassVar["SecurityMonitoringRuleQueryAggregation"]
    SUM: ClassVar["SecurityMonitoringRuleQueryAggregation"]
    MAX: ClassVar["SecurityMonitoringRuleQueryAggregation"]
    NEW_VALUE: ClassVar["SecurityMonitoringRuleQueryAggregation"]
    GEO_DATA: ClassVar["SecurityMonitoringRuleQueryAggregation"]
    EVENT_COUNT: ClassVar["SecurityMonitoringRuleQueryAggregation"]
    NONE: ClassVar["SecurityMonitoringRuleQueryAggregation"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SecurityMonitoringRuleQueryAggregation.COUNT = SecurityMonitoringRuleQueryAggregation("count")
SecurityMonitoringRuleQueryAggregation.CARDINALITY = SecurityMonitoringRuleQueryAggregation("cardinality")
SecurityMonitoringRuleQueryAggregation.SUM = SecurityMonitoringRuleQueryAggregation("sum")
SecurityMonitoringRuleQueryAggregation.MAX = SecurityMonitoringRuleQueryAggregation("max")
SecurityMonitoringRuleQueryAggregation.NEW_VALUE = SecurityMonitoringRuleQueryAggregation("new_value")
SecurityMonitoringRuleQueryAggregation.GEO_DATA = SecurityMonitoringRuleQueryAggregation("geo_data")
SecurityMonitoringRuleQueryAggregation.EVENT_COUNT = SecurityMonitoringRuleQueryAggregation("event_count")
SecurityMonitoringRuleQueryAggregation.NONE = SecurityMonitoringRuleQueryAggregation("none")
