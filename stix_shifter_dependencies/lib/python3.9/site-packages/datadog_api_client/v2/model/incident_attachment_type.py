# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class IncidentAttachmentType(ModelSimple):
    """
    The incident attachment resource type.

    :param value: If omitted defaults to "incident_attachments". Must be one of ["incident_attachments"].
    :type value: str
    """

    allowed_values = {
        "incident_attachments",
    }
    INCIDENT_ATTACHMENTS: ClassVar["IncidentAttachmentType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


IncidentAttachmentType.INCIDENT_ATTACHMENTS = IncidentAttachmentType("incident_attachments")
