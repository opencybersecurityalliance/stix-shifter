# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SyntheticsPlayingTab(ModelSimple):
    """
    Navigate between different tabs for your browser test.

    :param value: Must be one of [-1, 0, 1, 2, 3].
    :type value: int
    """

    allowed_values = {
        -1,
        0,
        1,
        2,
        3,
    }
    MAIN_TAB: ClassVar["SyntheticsPlayingTab"]
    NEW_TAB: ClassVar["SyntheticsPlayingTab"]
    TAB_1: ClassVar["SyntheticsPlayingTab"]
    TAB_2: ClassVar["SyntheticsPlayingTab"]
    TAB_3: ClassVar["SyntheticsPlayingTab"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (int,),
        }


SyntheticsPlayingTab.MAIN_TAB = SyntheticsPlayingTab(-1)
SyntheticsPlayingTab.NEW_TAB = SyntheticsPlayingTab(0)
SyntheticsPlayingTab.TAB_1 = SyntheticsPlayingTab(1)
SyntheticsPlayingTab.TAB_2 = SyntheticsPlayingTab(2)
SyntheticsPlayingTab.TAB_3 = SyntheticsPlayingTab(3)
