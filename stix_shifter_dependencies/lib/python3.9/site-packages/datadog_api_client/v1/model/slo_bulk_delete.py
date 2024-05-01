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


class SLOBulkDelete(ModelNormal):
    @cached_property
    def additional_properties_type(_):
        from datadog_api_client.v1.model.slo_timeframe import SLOTimeframe

        return ([SLOTimeframe],)

    def __init__(self_, **kwargs):
        """
        A map of service level objective object IDs to arrays of timeframes,
        which indicate the thresholds to delete for each ID.
        """
        super().__init__(kwargs)
