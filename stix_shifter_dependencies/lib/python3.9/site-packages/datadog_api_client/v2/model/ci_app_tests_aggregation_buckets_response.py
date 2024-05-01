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
    from datadog_api_client.v2.model.ci_app_tests_bucket_response import CIAppTestsBucketResponse


class CIAppTestsAggregationBucketsResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.ci_app_tests_bucket_response import CIAppTestsBucketResponse

        return {
            "buckets": ([CIAppTestsBucketResponse],),
        }

    attribute_map = {
        "buckets": "buckets",
    }

    def __init__(self_, buckets: Union[List[CIAppTestsBucketResponse], UnsetType] = unset, **kwargs):
        """
        The query results.

        :param buckets: The list of matching buckets, one item per bucket.
        :type buckets: [CIAppTestsBucketResponse], optional
        """
        if buckets is not unset:
            kwargs["buckets"] = buckets
        super().__init__(kwargs)
