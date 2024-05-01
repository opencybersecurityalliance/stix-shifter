# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)


class RUMAggregateBucketValueTimeseries(ModelSimple):
    """
    A timeseries array.


    :type value: [RUMAggregateBucketValueTimeseriesPoint]
    """

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.rum_aggregate_bucket_value_timeseries_point import (
            RUMAggregateBucketValueTimeseriesPoint,
        )

        return {
            "value": ([RUMAggregateBucketValueTimeseriesPoint],),
        }
