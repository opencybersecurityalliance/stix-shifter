# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class TableWidgetHasSearchBar(ModelSimple):
    """
    Controls the display of the search bar.

    :param value: Must be one of ["always", "never", "auto"].
    :type value: str
    """

    allowed_values = {
        "always",
        "never",
        "auto",
    }
    ALWAYS: ClassVar["TableWidgetHasSearchBar"]
    NEVER: ClassVar["TableWidgetHasSearchBar"]
    AUTO: ClassVar["TableWidgetHasSearchBar"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


TableWidgetHasSearchBar.ALWAYS = TableWidgetHasSearchBar("always")
TableWidgetHasSearchBar.NEVER = TableWidgetHasSearchBar("never")
TableWidgetHasSearchBar.AUTO = TableWidgetHasSearchBar("auto")
