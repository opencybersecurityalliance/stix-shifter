# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


class LogsArchiveOrderAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "archive_ids": ([str],),
        }

    attribute_map = {
        "archive_ids": "archive_ids",
    }

    def __init__(self_, archive_ids: List[str], **kwargs):
        """
        The attributes associated with the archive order.

        :param archive_ids: An ordered array of ``<ARCHIVE_ID>`` strings, the order of archive IDs in the array
            define the overall archives order for Datadog.
        :type archive_ids: [str]
        """
        super().__init__(kwargs)

        self_.archive_ids = archive_ids
