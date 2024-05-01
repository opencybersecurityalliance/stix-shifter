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
    from datadog_api_client.v1.model.service_check_status import ServiceCheckStatus


class ServiceCheck(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.service_check_status import ServiceCheckStatus

        return {
            "check": (str,),
            "host_name": (str,),
            "message": (str,),
            "status": (ServiceCheckStatus,),
            "tags": ([str],),
            "timestamp": (int,),
        }

    attribute_map = {
        "check": "check",
        "host_name": "host_name",
        "message": "message",
        "status": "status",
        "tags": "tags",
        "timestamp": "timestamp",
    }

    def __init__(
        self_,
        check: str,
        host_name: str,
        status: ServiceCheckStatus,
        tags: List[str],
        message: Union[str, UnsetType] = unset,
        timestamp: Union[int, UnsetType] = unset,
        **kwargs,
    ):
        """
        An object containing service check and status.

        :param check: The check.
        :type check: str

        :param host_name: The host name correlated with the check.
        :type host_name: str

        :param message: Message containing check status.
        :type message: str, optional

        :param status: The status of a service check. Set to ``0`` for OK, ``1`` for warning, ``2`` for critical, and ``3`` for unknown.
        :type status: ServiceCheckStatus

        :param tags: Tags related to a check.
        :type tags: [str]

        :param timestamp: Time of check.
        :type timestamp: int, optional
        """
        if message is not unset:
            kwargs["message"] = message
        if timestamp is not unset:
            kwargs["timestamp"] = timestamp
        super().__init__(kwargs)

        self_.check = check
        self_.host_name = host_name
        self_.status = status
        self_.tags = tags
