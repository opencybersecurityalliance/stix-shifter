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
    from datadog_api_client.v2.model.scalar_formula_request_attributes import ScalarFormulaRequestAttributes
    from datadog_api_client.v2.model.scalar_formula_request_type import ScalarFormulaRequestType


class ScalarFormulaRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.scalar_formula_request_attributes import ScalarFormulaRequestAttributes
        from datadog_api_client.v2.model.scalar_formula_request_type import ScalarFormulaRequestType

        return {
            "attributes": (ScalarFormulaRequestAttributes,),
            "type": (ScalarFormulaRequestType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "type": "type",
    }

    def __init__(self_, attributes: ScalarFormulaRequestAttributes, type: ScalarFormulaRequestType, **kwargs):
        """
        A single scalar query to be executed.

        :param attributes: The object describing a scalar formula request.
        :type attributes: ScalarFormulaRequestAttributes

        :param type: The type of the resource. The value should always be scalar_request.
        :type type: ScalarFormulaRequestType
        """
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.type = type
