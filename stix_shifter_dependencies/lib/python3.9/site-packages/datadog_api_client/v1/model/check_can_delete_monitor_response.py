# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Dict, List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.check_can_delete_monitor_response_data import CheckCanDeleteMonitorResponseData


class CheckCanDeleteMonitorResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.check_can_delete_monitor_response_data import CheckCanDeleteMonitorResponseData

        return {
            "data": (CheckCanDeleteMonitorResponseData,),
            "errors": ({str: ([str],)}, none_type),
        }

    attribute_map = {
        "data": "data",
        "errors": "errors",
    }

    def __init__(
        self_,
        data: CheckCanDeleteMonitorResponseData,
        errors: Union[Dict[str, List[str]], none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        Response of monitor IDs that can or can't be safely deleted.

        :param data: Wrapper object with the list of monitor IDs.
        :type data: CheckCanDeleteMonitorResponseData

        :param errors: A mapping of Monitor ID to strings denoting where it's used.
        :type errors: {str: ([str],)}, none_type, optional
        """
        if errors is not unset:
            kwargs["errors"] = errors
        super().__init__(kwargs)

        self_.data = data
