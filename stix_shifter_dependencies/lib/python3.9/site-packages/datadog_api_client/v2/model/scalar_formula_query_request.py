# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.scalar_formula_request import ScalarFormulaRequest


class ScalarFormulaQueryRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.scalar_formula_request import ScalarFormulaRequest

        return {
            "data": (ScalarFormulaRequest,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: ScalarFormulaRequest, **kwargs):
        """
        A wrapper request around one scalar query to be executed.

        :param data: A single scalar query to be executed.
        :type data: ScalarFormulaRequest
        """
        super().__init__(kwargs)

        self_.data = data
