# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SLOCorrectionCategory(ModelSimple):
    """
    Category the SLO correction belongs to.

    :param value: Must be one of ["Scheduled Maintenance", "Outside Business Hours", "Deployment", "Other"].
    :type value: str
    """

    allowed_values = {
        "Scheduled Maintenance",
        "Outside Business Hours",
        "Deployment",
        "Other",
    }
    SCHEDULED_MAINTENANCE: ClassVar["SLOCorrectionCategory"]
    OUTSIDE_BUSINESS_HOURS: ClassVar["SLOCorrectionCategory"]
    DEPLOYMENT: ClassVar["SLOCorrectionCategory"]
    OTHER: ClassVar["SLOCorrectionCategory"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SLOCorrectionCategory.SCHEDULED_MAINTENANCE = SLOCorrectionCategory("Scheduled Maintenance")
SLOCorrectionCategory.OUTSIDE_BUSINESS_HOURS = SLOCorrectionCategory("Outside Business Hours")
SLOCorrectionCategory.DEPLOYMENT = SLOCorrectionCategory("Deployment")
SLOCorrectionCategory.OTHER = SLOCorrectionCategory("Other")
