# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class FormulaAndFunctionEventsDataSource(ModelSimple):
    """
    Data source for event platform-based queries.

    :param value: Must be one of ["logs", "spans", "network", "rum", "security_signals", "profiles", "audit", "events", "ci_tests", "ci_pipelines"].
    :type value: str
    """

    allowed_values = {
        "logs",
        "spans",
        "network",
        "rum",
        "security_signals",
        "profiles",
        "audit",
        "events",
        "ci_tests",
        "ci_pipelines",
    }
    LOGS: ClassVar["FormulaAndFunctionEventsDataSource"]
    SPANS: ClassVar["FormulaAndFunctionEventsDataSource"]
    NETWORK: ClassVar["FormulaAndFunctionEventsDataSource"]
    RUM: ClassVar["FormulaAndFunctionEventsDataSource"]
    SECURITY_SIGNALS: ClassVar["FormulaAndFunctionEventsDataSource"]
    PROFILES: ClassVar["FormulaAndFunctionEventsDataSource"]
    AUDIT: ClassVar["FormulaAndFunctionEventsDataSource"]
    EVENTS: ClassVar["FormulaAndFunctionEventsDataSource"]
    CI_TESTS: ClassVar["FormulaAndFunctionEventsDataSource"]
    CI_PIPELINES: ClassVar["FormulaAndFunctionEventsDataSource"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


FormulaAndFunctionEventsDataSource.LOGS = FormulaAndFunctionEventsDataSource("logs")
FormulaAndFunctionEventsDataSource.SPANS = FormulaAndFunctionEventsDataSource("spans")
FormulaAndFunctionEventsDataSource.NETWORK = FormulaAndFunctionEventsDataSource("network")
FormulaAndFunctionEventsDataSource.RUM = FormulaAndFunctionEventsDataSource("rum")
FormulaAndFunctionEventsDataSource.SECURITY_SIGNALS = FormulaAndFunctionEventsDataSource("security_signals")
FormulaAndFunctionEventsDataSource.PROFILES = FormulaAndFunctionEventsDataSource("profiles")
FormulaAndFunctionEventsDataSource.AUDIT = FormulaAndFunctionEventsDataSource("audit")
FormulaAndFunctionEventsDataSource.EVENTS = FormulaAndFunctionEventsDataSource("events")
FormulaAndFunctionEventsDataSource.CI_TESTS = FormulaAndFunctionEventsDataSource("ci_tests")
FormulaAndFunctionEventsDataSource.CI_PIPELINES = FormulaAndFunctionEventsDataSource("ci_pipelines")
