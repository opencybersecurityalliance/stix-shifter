# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.logs_index import LogsIndex


class LogsIndexListResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.logs_index import LogsIndex

        return {
            "indexes": ([LogsIndex],),
        }

    attribute_map = {
        "indexes": "indexes",
    }

    def __init__(self_, indexes: Union[List[LogsIndex], UnsetType] = unset, **kwargs):
        """
        Object with all Index configurations for a given organization.

        :param indexes: Array of Log index configurations.
        :type indexes: [LogsIndex], optional
        """
        if indexes is not unset:
            kwargs["indexes"] = indexes
        super().__init__(kwargs)
