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
    from datadog_api_client.v2.model.security_monitoring_signal import SecurityMonitoringSignal
    from datadog_api_client.v2.model.security_monitoring_signals_list_response_links import (
        SecurityMonitoringSignalsListResponseLinks,
    )
    from datadog_api_client.v2.model.security_monitoring_signals_list_response_meta import (
        SecurityMonitoringSignalsListResponseMeta,
    )


class SecurityMonitoringSignalsListResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.security_monitoring_signal import SecurityMonitoringSignal
        from datadog_api_client.v2.model.security_monitoring_signals_list_response_links import (
            SecurityMonitoringSignalsListResponseLinks,
        )
        from datadog_api_client.v2.model.security_monitoring_signals_list_response_meta import (
            SecurityMonitoringSignalsListResponseMeta,
        )

        return {
            "data": ([SecurityMonitoringSignal],),
            "links": (SecurityMonitoringSignalsListResponseLinks,),
            "meta": (SecurityMonitoringSignalsListResponseMeta,),
        }

    attribute_map = {
        "data": "data",
        "links": "links",
        "meta": "meta",
    }

    def __init__(
        self_,
        data: Union[List[SecurityMonitoringSignal], UnsetType] = unset,
        links: Union[SecurityMonitoringSignalsListResponseLinks, UnsetType] = unset,
        meta: Union[SecurityMonitoringSignalsListResponseMeta, UnsetType] = unset,
        **kwargs,
    ):
        """
        The response object with all security signals matching the request
        and pagination information.

        :param data: An array of security signals matching the request.
        :type data: [SecurityMonitoringSignal], optional

        :param links: Links attributes.
        :type links: SecurityMonitoringSignalsListResponseLinks, optional

        :param meta: Meta attributes.
        :type meta: SecurityMonitoringSignalsListResponseMeta, optional
        """
        if data is not unset:
            kwargs["data"] = data
        if links is not unset:
            kwargs["links"] = links
        if meta is not unset:
            kwargs["meta"] = meta
        super().__init__(kwargs)
