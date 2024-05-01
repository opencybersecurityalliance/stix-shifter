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
    from datadog_api_client.v2.model.timeseries_response_attributes import TimeseriesResponseAttributes
    from datadog_api_client.v2.model.timeseries_formula_response_type import TimeseriesFormulaResponseType


class TimeseriesResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.timeseries_response_attributes import TimeseriesResponseAttributes
        from datadog_api_client.v2.model.timeseries_formula_response_type import TimeseriesFormulaResponseType

        return {
            "attributes": (TimeseriesResponseAttributes,),
            "type": (TimeseriesFormulaResponseType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: Union[TimeseriesResponseAttributes, UnsetType] = unset,
        type: Union[TimeseriesFormulaResponseType, UnsetType] = unset,
        **kwargs,
    ):
        """
        A message containing the response to a timeseries query.

        :param attributes: The object describing a timeseries response.
        :type attributes: TimeseriesResponseAttributes, optional

        :param type: The type of the resource. The value should always be timeseries_response.
        :type type: TimeseriesFormulaResponseType, optional
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
