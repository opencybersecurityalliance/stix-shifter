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
    from datadog_api_client.v2.model.audit_logs_event import AuditLogsEvent
    from datadog_api_client.v2.model.audit_logs_response_links import AuditLogsResponseLinks
    from datadog_api_client.v2.model.audit_logs_response_metadata import AuditLogsResponseMetadata


class AuditLogsEventsResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.audit_logs_event import AuditLogsEvent
        from datadog_api_client.v2.model.audit_logs_response_links import AuditLogsResponseLinks
        from datadog_api_client.v2.model.audit_logs_response_metadata import AuditLogsResponseMetadata

        return {
            "data": ([AuditLogsEvent],),
            "links": (AuditLogsResponseLinks,),
            "meta": (AuditLogsResponseMetadata,),
        }

    attribute_map = {
        "data": "data",
        "links": "links",
        "meta": "meta",
    }

    def __init__(
        self_,
        data: Union[List[AuditLogsEvent], UnsetType] = unset,
        links: Union[AuditLogsResponseLinks, UnsetType] = unset,
        meta: Union[AuditLogsResponseMetadata, UnsetType] = unset,
        **kwargs,
    ):
        """
        Response object with all events matching the request and pagination information.

        :param data: Array of events matching the request.
        :type data: [AuditLogsEvent], optional

        :param links: Links attributes.
        :type links: AuditLogsResponseLinks, optional

        :param meta: The metadata associated with a request.
        :type meta: AuditLogsResponseMetadata, optional
        """
        if data is not unset:
            kwargs["data"] = data
        if links is not unset:
            kwargs["links"] = links
        if meta is not unset:
            kwargs["meta"] = meta
        super().__init__(kwargs)
