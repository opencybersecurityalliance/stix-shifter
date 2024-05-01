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
    from datadog_api_client.v1.model.synthetics_global_variable import SyntheticsGlobalVariable


class SyntheticsListGlobalVariablesResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_global_variable import SyntheticsGlobalVariable

        return {
            "variables": ([SyntheticsGlobalVariable],),
        }

    attribute_map = {
        "variables": "variables",
    }

    def __init__(self_, variables: Union[List[SyntheticsGlobalVariable], UnsetType] = unset, **kwargs):
        """
        Object containing an array of Synthetic global variables.

        :param variables: Array of Synthetic global variables.
        :type variables: [SyntheticsGlobalVariable], optional
        """
        if variables is not unset:
            kwargs["variables"] = variables
        super().__init__(kwargs)
