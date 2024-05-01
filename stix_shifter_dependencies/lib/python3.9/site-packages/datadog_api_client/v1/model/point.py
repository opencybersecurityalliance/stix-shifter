# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
    none_type,
)


class Point(ModelSimple):
    """
    Array of timeseries points.


    :type value: [float, none_type]
    """

    validations = {
        "value": {
            "max_items": 2,
            "min_items": 2,
        },
    }

    @cached_property
    def openapi_types(_):
        return {
            "value": ([float, none_type],),
        }
