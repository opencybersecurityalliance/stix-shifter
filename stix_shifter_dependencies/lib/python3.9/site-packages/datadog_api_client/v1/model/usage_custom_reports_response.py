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
    from datadog_api_client.v1.model.usage_custom_reports_data import UsageCustomReportsData
    from datadog_api_client.v1.model.usage_custom_reports_meta import UsageCustomReportsMeta


class UsageCustomReportsResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.usage_custom_reports_data import UsageCustomReportsData
        from datadog_api_client.v1.model.usage_custom_reports_meta import UsageCustomReportsMeta

        return {
            "data": ([UsageCustomReportsData],),
            "meta": (UsageCustomReportsMeta,),
        }

    attribute_map = {
        "data": "data",
        "meta": "meta",
    }

    def __init__(
        self_,
        data: Union[List[UsageCustomReportsData], UnsetType] = unset,
        meta: Union[UsageCustomReportsMeta, UnsetType] = unset,
        **kwargs,
    ):
        """
        Response containing available custom reports.

        :param data: An array of available custom reports.
        :type data: [UsageCustomReportsData], optional

        :param meta: The object containing document metadata.
        :type meta: UsageCustomReportsMeta, optional
        """
        if data is not unset:
            kwargs["data"] = data
        if meta is not unset:
            kwargs["meta"] = meta
        super().__init__(kwargs)
