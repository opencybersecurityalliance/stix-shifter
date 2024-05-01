# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class MetricIngestedIndexedVolumeAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "indexed_volume": (int,),
            "ingested_volume": (int,),
        }

    attribute_map = {
        "indexed_volume": "indexed_volume",
        "ingested_volume": "ingested_volume",
    }

    def __init__(
        self_, indexed_volume: Union[int, UnsetType] = unset, ingested_volume: Union[int, UnsetType] = unset, **kwargs
    ):
        """
        Object containing the definition of a metric's ingested and indexed volume.

        :param indexed_volume: Indexed volume for the given metric.
        :type indexed_volume: int, optional

        :param ingested_volume: Ingested volume for the given metric.
        :type ingested_volume: int, optional
        """
        if indexed_volume is not unset:
            kwargs["indexed_volume"] = indexed_volume
        if ingested_volume is not unset:
            kwargs["ingested_volume"] = ingested_volume
        super().__init__(kwargs)
