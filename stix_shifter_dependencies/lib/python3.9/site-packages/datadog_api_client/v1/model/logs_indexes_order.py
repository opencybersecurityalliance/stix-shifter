# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


class LogsIndexesOrder(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "index_names": ([str],),
        }

    attribute_map = {
        "index_names": "index_names",
    }

    def __init__(self_, index_names: List[str], **kwargs):
        """
        Object containing the ordered list of log index names.

        :param index_names: Array of strings identifying by their name(s) the index(es) of your organization.
            Logs are tested against the query filter of each index one by one, following the order of the array.
            Logs are eventually stored in the first matching index.
        :type index_names: [str]
        """
        super().__init__(kwargs)

        self_.index_names = index_names
