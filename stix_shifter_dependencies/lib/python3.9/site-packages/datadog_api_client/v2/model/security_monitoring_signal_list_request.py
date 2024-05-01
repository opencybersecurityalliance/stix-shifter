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
    from datadog_api_client.v2.model.security_monitoring_signal_list_request_filter import (
        SecurityMonitoringSignalListRequestFilter,
    )
    from datadog_api_client.v2.model.security_monitoring_signal_list_request_page import (
        SecurityMonitoringSignalListRequestPage,
    )
    from datadog_api_client.v2.model.security_monitoring_signals_sort import SecurityMonitoringSignalsSort


class SecurityMonitoringSignalListRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.security_monitoring_signal_list_request_filter import (
            SecurityMonitoringSignalListRequestFilter,
        )
        from datadog_api_client.v2.model.security_monitoring_signal_list_request_page import (
            SecurityMonitoringSignalListRequestPage,
        )
        from datadog_api_client.v2.model.security_monitoring_signals_sort import SecurityMonitoringSignalsSort

        return {
            "filter": (SecurityMonitoringSignalListRequestFilter,),
            "page": (SecurityMonitoringSignalListRequestPage,),
            "sort": (SecurityMonitoringSignalsSort,),
        }

    attribute_map = {
        "filter": "filter",
        "page": "page",
        "sort": "sort",
    }

    def __init__(
        self_,
        filter: Union[SecurityMonitoringSignalListRequestFilter, UnsetType] = unset,
        page: Union[SecurityMonitoringSignalListRequestPage, UnsetType] = unset,
        sort: Union[SecurityMonitoringSignalsSort, UnsetType] = unset,
        **kwargs,
    ):
        """
        The request for a security signal list.

        :param filter: Search filters for listing security signals.
        :type filter: SecurityMonitoringSignalListRequestFilter, optional

        :param page: The paging attributes for listing security signals.
        :type page: SecurityMonitoringSignalListRequestPage, optional

        :param sort: The sort parameters used for querying security signals.
        :type sort: SecurityMonitoringSignalsSort, optional
        """
        if filter is not unset:
            kwargs["filter"] = filter
        if page is not unset:
            kwargs["page"] = page
        if sort is not unset:
            kwargs["sort"] = sort
        super().__init__(kwargs)
