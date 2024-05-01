# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class MonitorFormulaAndFunctionEventsDataSource(ModelSimple):
    """
    Data source for event platform-based queries.

    :param value: Must be one of ["rum", "ci_pipelines", "ci_tests", "audit", "events", "logs", "spans"].
    :type value: str
    """

    allowed_values = {
        "rum",
        "ci_pipelines",
        "ci_tests",
        "audit",
        "events",
        "logs",
        "spans",
    }
    RUM: ClassVar["MonitorFormulaAndFunctionEventsDataSource"]
    CI_PIPELINES: ClassVar["MonitorFormulaAndFunctionEventsDataSource"]
    CI_TESTS: ClassVar["MonitorFormulaAndFunctionEventsDataSource"]
    AUDIT: ClassVar["MonitorFormulaAndFunctionEventsDataSource"]
    EVENTS: ClassVar["MonitorFormulaAndFunctionEventsDataSource"]
    LOGS: ClassVar["MonitorFormulaAndFunctionEventsDataSource"]
    SPANS: ClassVar["MonitorFormulaAndFunctionEventsDataSource"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


MonitorFormulaAndFunctionEventsDataSource.RUM = MonitorFormulaAndFunctionEventsDataSource("rum")
MonitorFormulaAndFunctionEventsDataSource.CI_PIPELINES = MonitorFormulaAndFunctionEventsDataSource("ci_pipelines")
MonitorFormulaAndFunctionEventsDataSource.CI_TESTS = MonitorFormulaAndFunctionEventsDataSource("ci_tests")
MonitorFormulaAndFunctionEventsDataSource.AUDIT = MonitorFormulaAndFunctionEventsDataSource("audit")
MonitorFormulaAndFunctionEventsDataSource.EVENTS = MonitorFormulaAndFunctionEventsDataSource("events")
MonitorFormulaAndFunctionEventsDataSource.LOGS = MonitorFormulaAndFunctionEventsDataSource("logs")
MonitorFormulaAndFunctionEventsDataSource.SPANS = MonitorFormulaAndFunctionEventsDataSource("spans")
