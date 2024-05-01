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
    from datadog_api_client.v2.model.timeseries_formula_request_attributes import TimeseriesFormulaRequestAttributes
    from datadog_api_client.v2.model.timeseries_formula_request_type import TimeseriesFormulaRequestType


class TimeseriesFormulaRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.timeseries_formula_request_attributes import TimeseriesFormulaRequestAttributes
        from datadog_api_client.v2.model.timeseries_formula_request_type import TimeseriesFormulaRequestType

        return {
            "attributes": (TimeseriesFormulaRequestAttributes,),
            "type": (TimeseriesFormulaRequestType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "type": "type",
    }

    def __init__(self_, attributes: TimeseriesFormulaRequestAttributes, type: TimeseriesFormulaRequestType, **kwargs):
        """
        A single timeseries query to be executed.

        :param attributes: The object describing a timeseries formula request.
        :type attributes: TimeseriesFormulaRequestAttributes

        :param type: The type of the resource. The value should always be timeseries_request.
        :type type: TimeseriesFormulaRequestType
        """
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.type = type
