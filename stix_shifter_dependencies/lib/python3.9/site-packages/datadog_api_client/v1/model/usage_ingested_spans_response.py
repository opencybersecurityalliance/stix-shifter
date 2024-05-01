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
    from datadog_api_client.v1.model.usage_ingested_spans_hour import UsageIngestedSpansHour


class UsageIngestedSpansResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.usage_ingested_spans_hour import UsageIngestedSpansHour

        return {
            "usage": ([UsageIngestedSpansHour],),
        }

    attribute_map = {
        "usage": "usage",
    }

    def __init__(self_, usage: Union[List[UsageIngestedSpansHour], UnsetType] = unset, **kwargs):
        """
        Response containing the ingested spans usage for each hour for a given organization.

        :param usage: Get hourly usage for ingested spans.
        :type usage: [UsageIngestedSpansHour], optional
        """
        if usage is not unset:
            kwargs["usage"] = usage
        super().__init__(kwargs)
