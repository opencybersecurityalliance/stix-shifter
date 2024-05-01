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
    from datadog_api_client.v1.model.list_stream_compute_aggregation import ListStreamComputeAggregation


class ListStreamComputeItems(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.list_stream_compute_aggregation import ListStreamComputeAggregation

        return {
            "aggregation": (ListStreamComputeAggregation,),
            "facet": (str,),
        }

    attribute_map = {
        "aggregation": "aggregation",
        "facet": "facet",
    }

    def __init__(self_, aggregation: ListStreamComputeAggregation, facet: Union[str, UnsetType] = unset, **kwargs):
        """
        List of facets and aggregations which to compute.

        :param aggregation: Aggregation value.
        :type aggregation: ListStreamComputeAggregation

        :param facet: Facet name.
        :type facet: str, optional
        """
        if facet is not unset:
            kwargs["facet"] = facet
        super().__init__(kwargs)

        self_.aggregation = aggregation
