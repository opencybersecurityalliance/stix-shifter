# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.ci_app_pipelines_aggregation_buckets_response import (
        CIAppPipelinesAggregationBucketsResponse,
    )
    from datadog_api_client.v2.model.ci_app_response_links import CIAppResponseLinks
    from datadog_api_client.v2.model.ci_app_response_metadata import CIAppResponseMetadata


class CIAppPipelinesAnalyticsAggregateResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.ci_app_pipelines_aggregation_buckets_response import (
            CIAppPipelinesAggregationBucketsResponse,
        )
        from datadog_api_client.v2.model.ci_app_response_links import CIAppResponseLinks
        from datadog_api_client.v2.model.ci_app_response_metadata import CIAppResponseMetadata

        return {
            "data": (CIAppPipelinesAggregationBucketsResponse,),
            "links": (CIAppResponseLinks,),
            "meta": (CIAppResponseMetadata,),
        }

    attribute_map = {
        "data": "data",
        "links": "links",
        "meta": "meta",
    }

    def __init__(
        self_,
        data: Union[CIAppPipelinesAggregationBucketsResponse, UnsetType] = unset,
        links: Union[CIAppResponseLinks, UnsetType] = unset,
        meta: Union[CIAppResponseMetadata, UnsetType] = unset,
        **kwargs,
    ):
        """
        The response object for the pipeline events aggregate API endpoint.

        :param data: The query results.
        :type data: CIAppPipelinesAggregationBucketsResponse, optional

        :param links: Links attributes.
        :type links: CIAppResponseLinks, optional

        :param meta: The metadata associated with a request.
        :type meta: CIAppResponseMetadata, optional
        """
        if data is not unset:
            kwargs["data"] = data
        if links is not unset:
            kwargs["links"] = links
        if meta is not unset:
            kwargs["meta"] = meta
        super().__init__(kwargs)
