# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.logs_by_retention_org_usage import LogsByRetentionOrgUsage


class LogsByRetentionOrgs(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.logs_by_retention_org_usage import LogsByRetentionOrgUsage

        return {
            "usage": ([LogsByRetentionOrgUsage],),
        }

    attribute_map = {
        "usage": "usage",
    }

    def __init__(self_, usage: Union[List[LogsByRetentionOrgUsage], UnsetType] = unset, **kwargs):
        """
        Indexed logs usage summary for each organization for each retention period with usage.

        :param usage: Indexed logs usage summary for each organization.
        :type usage: [LogsByRetentionOrgUsage], optional
        """
        if usage is not unset:
            kwargs["usage"] = usage
        super().__init__(kwargs)
