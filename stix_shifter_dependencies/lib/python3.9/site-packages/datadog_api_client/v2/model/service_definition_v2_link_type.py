# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class ServiceDefinitionV2LinkType(ModelSimple):
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
    DOC: ClassVar["ServiceDefinitionV2LinkType"]
    WIKI: ClassVar["ServiceDefinitionV2LinkType"]
    RUNBOOK: ClassVar["ServiceDefinitionV2LinkType"]
    URL: ClassVar["ServiceDefinitionV2LinkType"]
    REPO: ClassVar["ServiceDefinitionV2LinkType"]
    DASHBOARD: ClassVar["ServiceDefinitionV2LinkType"]
    ONCALL: ClassVar["ServiceDefinitionV2LinkType"]
    CODE: ClassVar["ServiceDefinitionV2LinkType"]
    LINK: ClassVar["ServiceDefinitionV2LinkType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


ServiceDefinitionV2LinkType.DOC = ServiceDefinitionV2LinkType("doc")
ServiceDefinitionV2LinkType.WIKI = ServiceDefinitionV2LinkType("wiki")
ServiceDefinitionV2LinkType.RUNBOOK = ServiceDefinitionV2LinkType("runbook")
ServiceDefinitionV2LinkType.URL = ServiceDefinitionV2LinkType("url")
ServiceDefinitionV2LinkType.REPO = ServiceDefinitionV2LinkType("repo")
ServiceDefinitionV2LinkType.DASHBOARD = ServiceDefinitionV2LinkType("dashboard")
ServiceDefinitionV2LinkType.ONCALL = ServiceDefinitionV2LinkType("oncall")
ServiceDefinitionV2LinkType.CODE = ServiceDefinitionV2LinkType("code")
ServiceDefinitionV2LinkType.LINK = ServiceDefinitionV2LinkType("link")
