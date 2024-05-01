# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class JiraIntegrationMetadataIssuesItem(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "account": (str,),
            "issue_key": (str,),
            "issuetype_id": (str,),
            "project_key": (str,),
            "redirect_url": (str,),
        }

    attribute_map = {
        "account": "account",
        "issue_key": "issue_key",
        "issuetype_id": "issuetype_id",
        "project_key": "project_key",
        "redirect_url": "redirect_url",
    }

    def __init__(
        self_,
        account: str,
        project_key: str,
        issue_key: Union[str, UnsetType] = unset,
        issuetype_id: Union[str, UnsetType] = unset,
        redirect_url: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Item in the Jira integration metadata issue array.

        :param account: URL of issue's Jira account.
        :type account: str

        :param issue_key: Jira issue's issue key.
        :type issue_key: str, optional

        :param issuetype_id: Jira issue's issue type.
        :type issuetype_id: str, optional

        :param project_key: Jira issue's project keys.
        :type project_key: str

        :param redirect_url: URL redirecting to the Jira issue.
        :type redirect_url: str, optional
        """
        if issue_key is not unset:
            kwargs["issue_key"] = issue_key
        if issuetype_id is not unset:
            kwargs["issuetype_id"] = issuetype_id
        if redirect_url is not unset:
            kwargs["redirect_url"] = redirect_url
        super().__init__(kwargs)

        self_.account = account
        self_.project_key = project_key
