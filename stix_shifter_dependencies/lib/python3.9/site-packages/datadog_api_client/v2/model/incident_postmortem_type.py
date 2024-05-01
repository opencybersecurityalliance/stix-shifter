# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class IncidentPostmortemType(ModelSimple):
    """
    Incident postmortem resource type.

    :param value: If omitted defaults to "incident_postmortems". Must be one of ["incident_postmortems"].
    :type value: str
    """

    allowed_values = {
        "incident_postmortems",
    }
    INCIDENT_POSTMORTEMS: ClassVar["IncidentPostmortemType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


IncidentPostmortemType.INCIDENT_POSTMORTEMS = IncidentPostmortemType("incident_postmortems")
