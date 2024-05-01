# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Dict, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.check_can_delete_slo_response_data import CheckCanDeleteSLOResponseData


class CheckCanDeleteSLOResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.check_can_delete_slo_response_data import CheckCanDeleteSLOResponseData

        return {
            "data": (CheckCanDeleteSLOResponseData,),
            "errors": ({str: (str,)},),
        }

    attribute_map = {
        "data": "data",
        "errors": "errors",
    }

    def __init__(
        self_,
        data: Union[CheckCanDeleteSLOResponseData, UnsetType] = unset,
        errors: Union[Dict[str, str], UnsetType] = unset,
        **kwargs,
    ):
        """
        A service level objective response containing the requested object.

        :param data: An array of service level objective objects.
        :type data: CheckCanDeleteSLOResponseData, optional

        :param errors: A mapping of SLO id to it's current usages.
        :type errors: {str: (str,)}, optional
        """
        if data is not unset:
            kwargs["data"] = data
        if errors is not unset:
            kwargs["errors"] = errors
        super().__init__(kwargs)
