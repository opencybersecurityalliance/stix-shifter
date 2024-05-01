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
    from datadog_api_client.v2.model.ci_app_tests_query_filter import CIAppTestsQueryFilter
    from datadog_api_client.v2.model.ci_app_query_options import CIAppQueryOptions
    from datadog_api_client.v2.model.ci_app_query_page_options import CIAppQueryPageOptions
    from datadog_api_client.v2.model.ci_app_sort import CIAppSort


class CIAppTestEventsRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.ci_app_tests_query_filter import CIAppTestsQueryFilter
        from datadog_api_client.v2.model.ci_app_query_options import CIAppQueryOptions
        from datadog_api_client.v2.model.ci_app_query_page_options import CIAppQueryPageOptions
        from datadog_api_client.v2.model.ci_app_sort import CIAppSort

        return {
            "filter": (CIAppTestsQueryFilter,),
            "options": (CIAppQueryOptions,),
            "page": (CIAppQueryPageOptions,),
            "sort": (CIAppSort,),
        }

    attribute_map = {
        "filter": "filter",
        "options": "options",
        "page": "page",
        "sort": "sort",
    }

    def __init__(
        self_,
        filter: Union[CIAppTestsQueryFilter, UnsetType] = unset,
        options: Union[CIAppQueryOptions, UnsetType] = unset,
        page: Union[CIAppQueryPageOptions, UnsetType] = unset,
        sort: Union[CIAppSort, UnsetType] = unset,
        **kwargs,
    ):
        """
        The request for a tests search.

        :param filter: The search and filter query settings.
        :type filter: CIAppTestsQueryFilter, optional

        :param options: Global query options that are used during the query.
            Only supply timezone or time offset, not both. Otherwise, the query fails.
        :type options: CIAppQueryOptions, optional

        :param page: Paging attributes for listing events.
        :type page: CIAppQueryPageOptions, optional

        :param sort: Sort parameters when querying events.
        :type sort: CIAppSort, optional
        """
        if filter is not unset:
            kwargs["filter"] = filter
        if options is not unset:
            kwargs["options"] = options
        if page is not unset:
            kwargs["page"] = page
        if sort is not unset:
            kwargs["sort"] = sort
        super().__init__(kwargs)
