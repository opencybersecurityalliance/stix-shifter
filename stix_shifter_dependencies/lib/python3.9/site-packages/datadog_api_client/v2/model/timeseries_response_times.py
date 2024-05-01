# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)


class TimeseriesResponseTimes(ModelSimple):
    """
    Array of times, 1-1 match with individual values arrays.


    :type value: [int]
    """

    @cached_property
    def openapi_types(_):
        return {
            "value": ([int],),
        }
