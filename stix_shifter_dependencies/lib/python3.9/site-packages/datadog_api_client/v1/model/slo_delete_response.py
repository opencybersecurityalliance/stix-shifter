# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Dict, List, Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class SLODeleteResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "data": ([str],),
            "errors": ({str: (str,)},),
        }

    attribute_map = {
        "data": "data",
        "errors": "errors",
    }

    def __init__(
        self_, data: Union[List[str], UnsetType] = unset, errors: Union[Dict[str, str], UnsetType] = unset, **kwargs
    ):
        """
        A response list of all service level objective deleted.

        :param data: An array containing the ID of the deleted service level objective object.
        :type data: [str], optional

        :param errors: An dictionary containing the ID of the SLO as key and a deletion error as value.
        :type errors: {str: (str,)}, optional
        """
        if data is not unset:
            kwargs["data"] = data
        if errors is not unset:
            kwargs["errors"] = errors
        super().__init__(kwargs)
