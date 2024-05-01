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
    from datadog_api_client.v2.model.scalar_response import ScalarResponse


class ScalarFormulaQueryResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.scalar_response import ScalarResponse

        return {
            "data": (ScalarResponse,),
            "errors": (str,),
        }

    attribute_map = {
        "data": "data",
        "errors": "errors",
    }

    def __init__(
        self_, data: Union[ScalarResponse, UnsetType] = unset, errors: Union[str, UnsetType] = unset, **kwargs
    ):
        """
        A message containing one or more responses to scalar queries.

        :param data: A message containing the response to a scalar query.
        :type data: ScalarResponse, optional

        :param errors: An error generated when processing a request.
        :type errors: str, optional
        """
        if data is not unset:
            kwargs["data"] = data
        if errors is not unset:
            kwargs["errors"] = errors
        super().__init__(kwargs)
