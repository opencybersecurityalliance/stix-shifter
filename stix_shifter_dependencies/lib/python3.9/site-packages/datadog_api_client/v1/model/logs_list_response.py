# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.log import Log


class LogsListResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.log import Log

        return {
            "logs": ([Log],),
            "next_log_id": (str, none_type),
            "status": (str,),
        }

    attribute_map = {
        "logs": "logs",
        "next_log_id": "nextLogId",
        "status": "status",
    }

    def __init__(
        self_,
        logs: Union[List[Log], UnsetType] = unset,
        next_log_id: Union[str, none_type, UnsetType] = unset,
        status: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Response object with all logs matching the request and pagination information.

        :param logs: Array of logs matching the request and the ``nextLogId`` if sent.
        :type logs: [Log], optional

        :param next_log_id: Hash identifier of the next log to return in the list.
            This parameter is used for the pagination feature.
        :type next_log_id: str, none_type, optional

        :param status: Status of the response.
        :type status: str, optional
        """
        if logs is not unset:
            kwargs["logs"] = logs
        if next_log_id is not unset:
            kwargs["next_log_id"] = next_log_id
        if status is not unset:
            kwargs["status"] = status
        super().__init__(kwargs)
