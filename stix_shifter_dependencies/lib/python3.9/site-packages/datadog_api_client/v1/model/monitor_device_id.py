# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class MonitorDeviceID(ModelSimple):
    """
    ID of the device the Synthetics monitor is running on. Same as `SyntheticsDeviceID`.

    :param value: Must be one of ["laptop_large", "tablet", "mobile_small", "chrome.laptop_large", "chrome.tablet", "chrome.mobile_small", "firefox.laptop_large", "firefox.tablet", "firefox.mobile_small"].
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
    }
    LAPTOP_LARGE: ClassVar["MonitorDeviceID"]
    TABLET: ClassVar["MonitorDeviceID"]
    MOBILE_SMALL: ClassVar["MonitorDeviceID"]
    CHROME_LAPTOP_LARGE: ClassVar["MonitorDeviceID"]
    CHROME_TABLET: ClassVar["MonitorDeviceID"]
    CHROME_MOBILE_SMALL: ClassVar["MonitorDeviceID"]
    FIREFOX_LAPTOP_LARGE: ClassVar["MonitorDeviceID"]
    FIREFOX_TABLET: ClassVar["MonitorDeviceID"]
    FIREFOX_MOBILE_SMALL: ClassVar["MonitorDeviceID"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


MonitorDeviceID.LAPTOP_LARGE = MonitorDeviceID("laptop_large")
MonitorDeviceID.TABLET = MonitorDeviceID("tablet")
MonitorDeviceID.MOBILE_SMALL = MonitorDeviceID("mobile_small")
MonitorDeviceID.CHROME_LAPTOP_LARGE = MonitorDeviceID("chrome.laptop_large")
MonitorDeviceID.CHROME_TABLET = MonitorDeviceID("chrome.tablet")
MonitorDeviceID.CHROME_MOBILE_SMALL = MonitorDeviceID("chrome.mobile_small")
MonitorDeviceID.FIREFOX_LAPTOP_LARGE = MonitorDeviceID("firefox.laptop_large")
MonitorDeviceID.FIREFOX_TABLET = MonitorDeviceID("firefox.tablet")
MonitorDeviceID.FIREFOX_MOBILE_SMALL = MonitorDeviceID("firefox.mobile_small")
