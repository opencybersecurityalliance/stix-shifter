# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


class LogsPipelinesOrder(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "pipeline_ids": ([str],),
        }

    attribute_map = {
        "pipeline_ids": "pipeline_ids",
    }

    def __init__(self_, pipeline_ids: List[str], **kwargs):
        """
        Object containing the ordered list of pipeline IDs.

        :param pipeline_ids: Ordered Array of ``<PIPELINE_ID>`` strings, the order of pipeline IDs in the array
            define the overall Pipelines order for Datadog.
        :type pipeline_ids: [str]
        """
        super().__init__(kwargs)

        self_.pipeline_ids = pipeline_ids
