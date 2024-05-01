# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class ServiceDefinitionV2Dot1LinkType(ModelSimple):
    """
    Link type.

    :param value: Must be one of ["doc", "repo", "runbook", "dashboard", "other"].
    :type value: str
    """

    allowed_values = {
        "doc",
        "repo",
        "runbook",
        "dashboard",
        "other",
    }
    DOC: ClassVar["ServiceDefinitionV2Dot1LinkType"]
    REPO: ClassVar["ServiceDefinitionV2Dot1LinkType"]
    RUNBOOK: ClassVar["ServiceDefinitionV2Dot1LinkType"]
    DASHBOARD: ClassVar["ServiceDefinitionV2Dot1LinkType"]
    OTHER: ClassVar["ServiceDefinitionV2Dot1LinkType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


ServiceDefinitionV2Dot1LinkType.DOC = ServiceDefinitionV2Dot1LinkType("doc")
ServiceDefinitionV2Dot1LinkType.REPO = ServiceDefinitionV2Dot1LinkType("repo")
ServiceDefinitionV2Dot1LinkType.RUNBOOK = ServiceDefinitionV2Dot1LinkType("runbook")
ServiceDefinitionV2Dot1LinkType.DASHBOARD = ServiceDefinitionV2Dot1LinkType("dashboard")
ServiceDefinitionV2Dot1LinkType.OTHER = ServiceDefinitionV2Dot1LinkType("other")
