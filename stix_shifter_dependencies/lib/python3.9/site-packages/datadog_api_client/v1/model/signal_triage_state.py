# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SignalTriageState(ModelSimple):
    """
    The new triage state of the signal.

    :param value: Must be one of ["open", "archived", "under_review"].
    :type value: str
    """

    allowed_values = {
        "open",
        "archived",
        "under_review",
    }
    OPEN: ClassVar["SignalTriageState"]
    ARCHIVED: ClassVar["SignalTriageState"]
    UNDER_REVIEW: ClassVar["SignalTriageState"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SignalTriageState.OPEN = SignalTriageState("open")
SignalTriageState.ARCHIVED = SignalTriageState("archived")
SignalTriageState.UNDER_REVIEW = SignalTriageState("under_review")
