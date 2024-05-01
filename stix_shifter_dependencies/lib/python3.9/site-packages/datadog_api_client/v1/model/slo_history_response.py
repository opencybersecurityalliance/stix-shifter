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
    from datadog_api_client.v1.model.slo_history_response_data import SLOHistoryResponseData
    from datadog_api_client.v1.model.slo_history_response_error import SLOHistoryResponseError


class SLOHistoryResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.slo_history_response_data import SLOHistoryResponseData
        from datadog_api_client.v1.model.slo_history_response_error import SLOHistoryResponseError

        return {
            "data": (SLOHistoryResponseData,),
            "errors": ([SLOHistoryResponseError], none_type),
        }

    attribute_map = {
        "data": "data",
        "errors": "errors",
    }

    def __init__(
        self_,
        data: Union[SLOHistoryResponseData, UnsetType] = unset,
        errors: Union[List[SLOHistoryResponseError], none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        A service level objective history response.

        :param data: An array of service level objective objects.
        :type data: SLOHistoryResponseData, optional

        :param errors: A list of errors while querying the history data for the service level objective.
        :type errors: [SLOHistoryResponseError], none_type, optional
        """
        if data is not unset:
            kwargs["data"] = data
        if errors is not unset:
            kwargs["errors"] = errors
        super().__init__(kwargs)
