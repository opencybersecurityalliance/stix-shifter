# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)


class TimeseriesResponseValuesList(ModelSimple):
    """
    Array of value-arrays. The index here corresponds to the index in the ``formulas`` or ``queries`` array from the request.


    :type value: [TimeseriesResponseValues]
    """

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.timeseries_response_values import TimeseriesResponseValues

        return {
            "value": ([TimeseriesResponseValues],),
        }
