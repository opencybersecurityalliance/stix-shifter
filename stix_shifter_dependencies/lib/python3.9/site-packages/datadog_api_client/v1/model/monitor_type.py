# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class MonitorType(ModelSimple):
    """
    The type of the monitor. For more information about `type`, see the [monitor options](https://docs.datadoghq.com/monitors/guide/monitor_api_options/) docs.

    :param value: Must be one of ["composite", "event alert", "log alert", "metric alert", "process alert", "query alert", "rum alert", "service check", "synthetics alert", "trace-analytics alert", "slo alert", "event-v2 alert", "audit alert", "ci-pipelines alert", "ci-tests alert", "error-tracking alert"].
    :type value: str
    """

    allowed_values = {
        "composite",
        "event alert",
        "log alert",
        "metric alert",
        "process alert",
        "query alert",
        "rum alert",
        "service check",
        "synthetics alert",
        "trace-analytics alert",
        "slo alert",
        "event-v2 alert",
        "audit alert",
        "ci-pipelines alert",
        "ci-tests alert",
        "error-tracking alert",
    }
    COMPOSITE: ClassVar["MonitorType"]
    EVENT_ALERT: ClassVar["MonitorType"]
    LOG_ALERT: ClassVar["MonitorType"]
    METRIC_ALERT: ClassVar["MonitorType"]
    PROCESS_ALERT: ClassVar["MonitorType"]
    QUERY_ALERT: ClassVar["MonitorType"]
    RUM_ALERT: ClassVar["MonitorType"]
    SERVICE_CHECK: ClassVar["MonitorType"]
    SYNTHETICS_ALERT: ClassVar["MonitorType"]
    TRACE_ANALYTICS_ALERT: ClassVar["MonitorType"]
    SLO_ALERT: ClassVar["MonitorType"]
    EVENT_V2_ALERT: ClassVar["MonitorType"]
    AUDIT_ALERT: ClassVar["MonitorType"]
    CI_PIPELINES_ALERT: ClassVar["MonitorType"]
    CI_TESTS_ALERT: ClassVar["MonitorType"]
    ERROR_TRACKING_ALERT: ClassVar["MonitorType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


MonitorType.COMPOSITE = MonitorType("composite")
MonitorType.EVENT_ALERT = MonitorType("event alert")
MonitorType.LOG_ALERT = MonitorType("log alert")
MonitorType.METRIC_ALERT = MonitorType("metric alert")
MonitorType.PROCESS_ALERT = MonitorType("process alert")
MonitorType.QUERY_ALERT = MonitorType("query alert")
MonitorType.RUM_ALERT = MonitorType("rum alert")
MonitorType.SERVICE_CHECK = MonitorType("service check")
MonitorType.SYNTHETICS_ALERT = MonitorType("synthetics alert")
MonitorType.TRACE_ANALYTICS_ALERT = MonitorType("trace-analytics alert")
MonitorType.SLO_ALERT = MonitorType("slo alert")
MonitorType.EVENT_V2_ALERT = MonitorType("event-v2 alert")
MonitorType.AUDIT_ALERT = MonitorType("audit alert")
MonitorType.CI_PIPELINES_ALERT = MonitorType("ci-pipelines alert")
MonitorType.CI_TESTS_ALERT = MonitorType("ci-tests alert")
MonitorType.ERROR_TRACKING_ALERT = MonitorType("error-tracking alert")
