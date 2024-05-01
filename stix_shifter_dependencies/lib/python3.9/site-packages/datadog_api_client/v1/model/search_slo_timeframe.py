# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SearchSLOTimeframe(ModelSimple):
    """
    The SLO time window options.

    :param value: Must be one of ["7d", "30d", "90d"].
    :type value: str
    """

    allowed_values = {
        "7d",
        "30d",
        "90d",
    }
    SEVEN_DAYS: ClassVar["SearchSLOTimeframe"]
    THIRTY_DAYS: ClassVar["SearchSLOTimeframe"]
    NINETY_DAYS: ClassVar["SearchSLOTimeframe"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SearchSLOTimeframe.SEVEN_DAYS = SearchSLOTimeframe("7d")
SearchSLOTimeframe.THIRTY_DAYS = SearchSLOTimeframe("30d")
SearchSLOTimeframe.NINETY_DAYS = SearchSLOTimeframe("90d")
