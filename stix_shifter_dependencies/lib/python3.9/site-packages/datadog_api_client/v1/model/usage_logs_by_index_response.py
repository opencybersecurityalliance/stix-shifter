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
    from datadog_api_client.v1.model.usage_logs_by_index_hour import UsageLogsByIndexHour


class UsageLogsByIndexResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.usage_logs_by_index_hour import UsageLogsByIndexHour

        return {
            "usage": ([UsageLogsByIndexHour],),
        }

    attribute_map = {
        "usage": "usage",
    }

    def __init__(self_, usage: Union[List[UsageLogsByIndexHour], UnsetType] = unset, **kwargs):
        """
        Response containing the number of indexed logs for each hour and index for a given organization.

        :param usage: An array of objects regarding hourly usage of logs by index response.
        :type usage: [UsageLogsByIndexHour], optional
        """
        if usage is not unset:
            kwargs["usage"] = usage
        super().__init__(kwargs)
