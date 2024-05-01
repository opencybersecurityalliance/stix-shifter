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
    from datadog_api_client.v1.model.synthetics_test_headers import SyntheticsTestHeaders


class SyntheticsTestRequestProxy(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_test_headers import SyntheticsTestHeaders

        return {
            "headers": (SyntheticsTestHeaders,),
            "url": (str,),
        }

    attribute_map = {
        "headers": "headers",
        "url": "url",
    }

    def __init__(self_, url: str, headers: Union[SyntheticsTestHeaders, UnsetType] = unset, **kwargs):
        """
        The proxy to perform the test.

        :param headers: Headers to include when performing the test.
        :type headers: SyntheticsTestHeaders, optional

        :param url: URL of the proxy to perform the test.
        :type url: str
        """
        if headers is not unset:
            kwargs["headers"] = headers
        super().__init__(kwargs)

        self_.url = url
