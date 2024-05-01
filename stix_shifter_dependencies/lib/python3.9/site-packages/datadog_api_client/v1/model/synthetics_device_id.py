# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SyntheticsDeviceID(ModelSimple):
    """
    The device ID.

    :param value: Must be one of ["laptop_large", "tablet", "mobile_small", "chrome.laptop_large", "chrome.tablet", "chrome.mobile_small", "firefox.laptop_large", "firefox.tablet", "firefox.mobile_small", "edge.laptop_large", "edge.tablet", "edge.mobile_small"].
    :type value: str
    """

    allowed_values = {
        "laptop_large",
        "tablet",
        "mobile_small",
        "chrome.laptop_large",
        "chrome.tablet",
        "chrome.mobile_small",
        "firefox.laptop_large",
        "firefox.tablet",
        "firefox.mobile_small",
        "edge.laptop_large",
        "edge.tablet",
        "edge.mobile_small",
    }
    LAPTOP_LARGE: ClassVar["SyntheticsDeviceID"]
    TABLET: ClassVar["SyntheticsDeviceID"]
    MOBILE_SMALL: ClassVar["SyntheticsDeviceID"]
    CHROME_LAPTOP_LARGE: ClassVar["SyntheticsDeviceID"]
    CHROME_TABLET: ClassVar["SyntheticsDeviceID"]
    CHROME_MOBILE_SMALL: ClassVar["SyntheticsDeviceID"]
    FIREFOX_LAPTOP_LARGE: ClassVar["SyntheticsDeviceID"]
    FIREFOX_TABLET: ClassVar["SyntheticsDeviceID"]
    FIREFOX_MOBILE_SMALL: ClassVar["SyntheticsDeviceID"]
    EDGE_LAPTOP_LARGE: ClassVar["SyntheticsDeviceID"]
    EDGE_TABLET: ClassVar["SyntheticsDeviceID"]
    EDGE_MOBILE_SMALL: ClassVar["SyntheticsDeviceID"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SyntheticsDeviceID.LAPTOP_LARGE = SyntheticsDeviceID("laptop_large")
SyntheticsDeviceID.TABLET = SyntheticsDeviceID("tablet")
SyntheticsDeviceID.MOBILE_SMALL = SyntheticsDeviceID("mobile_small")
SyntheticsDeviceID.CHROME_LAPTOP_LARGE = SyntheticsDeviceID("chrome.laptop_large")
SyntheticsDeviceID.CHROME_TABLET = SyntheticsDeviceID("chrome.tablet")
SyntheticsDeviceID.CHROME_MOBILE_SMALL = SyntheticsDeviceID("chrome.mobile_small")
SyntheticsDeviceID.FIREFOX_LAPTOP_LARGE = SyntheticsDeviceID("firefox.laptop_large")
SyntheticsDeviceID.FIREFOX_TABLET = SyntheticsDeviceID("firefox.tablet")
SyntheticsDeviceID.FIREFOX_MOBILE_SMALL = SyntheticsDeviceID("firefox.mobile_small")
SyntheticsDeviceID.EDGE_LAPTOP_LARGE = SyntheticsDeviceID("edge.laptop_large")
SyntheticsDeviceID.EDGE_TABLET = SyntheticsDeviceID("edge.tablet")
SyntheticsDeviceID.EDGE_MOBILE_SMALL = SyntheticsDeviceID("edge.mobile_small")
