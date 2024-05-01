# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class ServiceDefinitionV1ResourceType(ModelSimple):
    """
    Link type.

    :param value: Must be one of ["doc", "wiki", "runbook", "url", "repo", "dashboard", "oncall", "code", "link"].
    :type value: str
    """

    allowed_values = {
        "doc",
        "wiki",
        "runbook",
        "url",
        "repo",
        "dashboard",
        "oncall",
        "code",
        "link",
    }
    DOC: ClassVar["ServiceDefinitionV1ResourceType"]
    WIKI: ClassVar["ServiceDefinitionV1ResourceType"]
    RUNBOOK: ClassVar["ServiceDefinitionV1ResourceType"]
    URL: ClassVar["ServiceDefinitionV1ResourceType"]
    REPO: ClassVar["ServiceDefinitionV1ResourceType"]
    DASHBOARD: ClassVar["ServiceDefinitionV1ResourceType"]
    ONCALL: ClassVar["ServiceDefinitionV1ResourceType"]
    CODE: ClassVar["ServiceDefinitionV1ResourceType"]
    LINK: ClassVar["ServiceDefinitionV1ResourceType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


ServiceDefinitionV1ResourceType.DOC = ServiceDefinitionV1ResourceType("doc")
ServiceDefinitionV1ResourceType.WIKI = ServiceDefinitionV1ResourceType("wiki")
ServiceDefinitionV1ResourceType.RUNBOOK = ServiceDefinitionV1ResourceType("runbook")
ServiceDefinitionV1ResourceType.URL = ServiceDefinitionV1ResourceType("url")
ServiceDefinitionV1ResourceType.REPO = ServiceDefinitionV1ResourceType("repo")
ServiceDefinitionV1ResourceType.DASHBOARD = ServiceDefinitionV1ResourceType("dashboard")
ServiceDefinitionV1ResourceType.ONCALL = ServiceDefinitionV1ResourceType("oncall")
ServiceDefinitionV1ResourceType.CODE = ServiceDefinitionV1ResourceType("code")
ServiceDefinitionV1ResourceType.LINK = ServiceDefinitionV1ResourceType("link")
