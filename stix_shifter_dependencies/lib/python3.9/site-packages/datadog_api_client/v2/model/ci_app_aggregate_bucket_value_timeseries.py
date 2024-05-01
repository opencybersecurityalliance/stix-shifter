# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)


class CIAppAggregateBucketValueTimeseries(ModelSimple):
    """
    A timeseries array.


    :type value: [CIAppAggregateBucketValueTimeseriesPoint]
    """

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.ci_app_aggregate_bucket_value_timeseries_point import (
            CIAppAggregateBucketValueTimeseriesPoint,
        )

        return {
            "value": ([CIAppAggregateBucketValueTimeseriesPoint],),
        }
