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
    from datadog_api_client.v2.model.rum_aggregate_bucket_value import RUMAggregateBucketValue
    from datadog_api_client.v2.model.rum_aggregate_bucket_value_timeseries import RUMAggregateBucketValueTimeseries


class RUMBucketResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.rum_aggregate_bucket_value import RUMAggregateBucketValue

        return {
            "by": ({str: (str,)},),
            "computes": ({str: (RUMAggregateBucketValue,)},),
        }

    attribute_map = {
        "by": "by",
        "computes": "computes",
    }

    def __init__(
        self_,
        by: Union[Dict[str, str], UnsetType] = unset,
        computes: Union[
            Dict[str, Union[RUMAggregateBucketValue, str, float, RUMAggregateBucketValueTimeseries]], UnsetType
        ] = unset,
        **kwargs,
    ):
        """
        Bucket values.

        :param by: The key-value pairs for each group-by.
        :type by: {str: (str,)}, optional

        :param computes: A map of the metric name to value for regular compute, or a list of values for a timeseries.
        :type computes: {str: (RUMAggregateBucketValue,)}, optional
        """
        if by is not unset:
            kwargs["by"] = by
        if computes is not unset:
            kwargs["computes"] = computes
        super().__init__(kwargs)
