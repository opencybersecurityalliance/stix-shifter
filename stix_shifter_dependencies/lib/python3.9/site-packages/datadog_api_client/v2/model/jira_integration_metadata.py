# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.jira_integration_metadata_issues_item import JiraIntegrationMetadataIssuesItem


class JiraIntegrationMetadata(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.jira_integration_metadata_issues_item import JiraIntegrationMetadataIssuesItem

        return {
            "issues": ([JiraIntegrationMetadataIssuesItem],),
        }

    attribute_map = {
        "issues": "issues",
    }

    def __init__(self_, issues: List[JiraIntegrationMetadataIssuesItem], **kwargs):
        """
        Incident integration metadata for the Jira integration.

        :param issues: Array of Jira issues in this integration metadata.
        :type issues: [JiraIntegrationMetadataIssuesItem]
        """
        super().__init__(kwargs)

        self_.issues = issues
