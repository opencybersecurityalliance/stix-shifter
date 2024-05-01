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
    from datadog_api_client.v1.model.formula_and_function_event_aggregation import FormulaAndFunctionEventAggregation


class FormulaAndFunctionEventQueryDefinitionCompute(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.formula_and_function_event_aggregation import (
            FormulaAndFunctionEventAggregation,
        )

        return {
            "aggregation": (FormulaAndFunctionEventAggregation,),
            "interval": (int,),
            "metric": (str,),
        }

    attribute_map = {
        "aggregation": "aggregation",
        "interval": "interval",
        "metric": "metric",
    }

    def __init__(
        self_,
        aggregation: FormulaAndFunctionEventAggregation,
        interval: Union[int, UnsetType] = unset,
        metric: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Compute options.

        :param aggregation: Aggregation methods for event platform queries.
        :type aggregation: FormulaAndFunctionEventAggregation

        :param interval: A time interval in milliseconds.
        :type interval: int, optional

        :param metric: Measurable attribute to compute.
        :type metric: str, optional
        """
        if interval is not unset:
            kwargs["interval"] = interval
        if metric is not unset:
            kwargs["metric"] = metric
        super().__init__(kwargs)

        self_.aggregation = aggregation
