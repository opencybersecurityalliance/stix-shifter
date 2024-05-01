# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SignalArchiveReason(ModelSimple):
    """
    Reason why a signal has been archived.

    :param value: Must be one of ["none", "false_positive", "testing_or_maintenance", "other"].
    :type value: str
    """

    allowed_values = {
        "none",
        "false_positive",
        "testing_or_maintenance",
        "other",
    }
    NONE: ClassVar["SignalArchiveReason"]
    FALSE_POSITIVE: ClassVar["SignalArchiveReason"]
    TESTING_OR_MAINTENANCE: ClassVar["SignalArchiveReason"]
    OTHER: ClassVar["SignalArchiveReason"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SignalArchiveReason.NONE = SignalArchiveReason("none")
SignalArchiveReason.FALSE_POSITIVE = SignalArchiveReason("false_positive")
SignalArchiveReason.TESTING_OR_MAINTENANCE = SignalArchiveReason("testing_or_maintenance")
SignalArchiveReason.OTHER = SignalArchiveReason("other")
