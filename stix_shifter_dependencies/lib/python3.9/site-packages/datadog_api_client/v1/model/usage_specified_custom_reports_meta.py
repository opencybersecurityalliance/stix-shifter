# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.usage_specified_custom_reports_page import UsageSpecifiedCustomReportsPage


class UsageSpecifiedCustomReportsMeta(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.usage_specified_custom_reports_page import UsageSpecifiedCustomReportsPage

        return {
            "page": (UsageSpecifiedCustomReportsPage,),
        }

    attribute_map = {
        "page": "page",
    }

    def __init__(self_, page: Union[UsageSpecifiedCustomReportsPage, UnsetType] = unset, **kwargs):
        """
        The object containing document metadata.

        :param page: The object containing page total count for specified ID.
        :type page: UsageSpecifiedCustomReportsPage, optional
        """
        if page is not unset:
            kwargs["page"] = page
        super().__init__(kwargs)
