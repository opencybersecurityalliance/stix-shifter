# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.distribution_points_series import DistributionPointsSeries


class DistributionPointsPayload(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.distribution_points_series import DistributionPointsSeries

        return {
            "series": ([DistributionPointsSeries],),
        }

    attribute_map = {
        "series": "series",
    }

    def __init__(self_, series: List[DistributionPointsSeries], **kwargs):
        """
        The distribution points payload.

        :param series: A list of distribution points series to submit to Datadog.
        :type series: [DistributionPointsSeries]
        """
        super().__init__(kwargs)

        self_.series = series
