# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SyntheticsTestProcessStatus(ModelSimple):
    """
    Status of a Synthetic test.

    :param value: Must be one of ["not_scheduled", "scheduled", "finished", "finished_with_error"].
    :type value: str
    """

    allowed_values = {
        "not_scheduled",
        "scheduled",
        "finished",
        "finished_with_error",
    }
    NOT_SCHEDULED: ClassVar["SyntheticsTestProcessStatus"]
    SCHEDULED: ClassVar["SyntheticsTestProcessStatus"]
    FINISHED: ClassVar["SyntheticsTestProcessStatus"]
    FINISHED_WITH_ERROR: ClassVar["SyntheticsTestProcessStatus"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SyntheticsTestProcessStatus.NOT_SCHEDULED = SyntheticsTestProcessStatus("not_scheduled")
SyntheticsTestProcessStatus.SCHEDULED = SyntheticsTestProcessStatus("scheduled")
SyntheticsTestProcessStatus.FINISHED = SyntheticsTestProcessStatus("finished")
SyntheticsTestProcessStatus.FINISHED_WITH_ERROR = SyntheticsTestProcessStatus("finished_with_error")
