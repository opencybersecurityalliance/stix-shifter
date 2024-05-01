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
    from datadog_api_client.v2.model.rum_bucket_response import RUMBucketResponse


class RUMAggregationBucketsResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.rum_bucket_response import RUMBucketResponse

        return {
            "buckets": ([RUMBucketResponse],),
        }

    attribute_map = {
        "buckets": "buckets",
    }

    def __init__(self_, buckets: Union[List[RUMBucketResponse], UnsetType] = unset, **kwargs):
        """
        The query results.

        :param buckets: The list of matching buckets, one item per bucket.
        :type buckets: [RUMBucketResponse], optional
        """
        if buckets is not unset:
            kwargs["buckets"] = buckets
        super().__init__(kwargs)
