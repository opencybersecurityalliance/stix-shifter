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
    from datadog_api_client.v1.model.usage_attribution_metadata import UsageAttributionMetadata
    from datadog_api_client.v1.model.usage_attribution_body import UsageAttributionBody


class UsageAttributionResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.usage_attribution_metadata import UsageAttributionMetadata
        from datadog_api_client.v1.model.usage_attribution_body import UsageAttributionBody

        return {
            "metadata": (UsageAttributionMetadata,),
            "usage": ([UsageAttributionBody],),
        }

    attribute_map = {
        "metadata": "metadata",
        "usage": "usage",
    }

    def __init__(
        self_,
        metadata: Union[UsageAttributionMetadata, UnsetType] = unset,
        usage: Union[List[UsageAttributionBody], UnsetType] = unset,
        **kwargs,
    ):
        """
        Response containing the Usage Summary by tag(s).

        :param metadata: The object containing document metadata.
        :type metadata: UsageAttributionMetadata, optional

        :param usage: Get usage summary by tag(s).
        :type usage: [UsageAttributionBody], optional
        """
        if metadata is not unset:
            kwargs["metadata"] = metadata
        if usage is not unset:
            kwargs["usage"] = usage
        super().__init__(kwargs)
