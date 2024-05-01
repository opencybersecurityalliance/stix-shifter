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
    pass


class CIAppComputes(ModelNormal):
    @cached_property
    def additional_properties_type(_):
        from datadog_api_client.v2.model.ci_app_aggregate_bucket_value import CIAppAggregateBucketValue

        return (CIAppAggregateBucketValue,)

    def __init__(self_, **kwargs):
        """
        A map of the metric name to value for regular compute, or a list of values for a timeseries.
        """
        super().__init__(kwargs)
