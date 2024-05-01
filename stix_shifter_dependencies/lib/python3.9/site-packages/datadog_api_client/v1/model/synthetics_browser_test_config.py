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
    from datadog_api_client.v1.model.synthetics_config_variable import SyntheticsConfigVariable
    from datadog_api_client.v1.model.synthetics_test_request import SyntheticsTestRequest
    from datadog_api_client.v1.model.synthetics_browser_variable import SyntheticsBrowserVariable


class SyntheticsBrowserTestConfig(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_assertion import SyntheticsAssertion
        from datadog_api_client.v1.model.synthetics_config_variable import SyntheticsConfigVariable
        from datadog_api_client.v1.model.synthetics_test_request import SyntheticsTestRequest
        from datadog_api_client.v1.model.synthetics_browser_variable import SyntheticsBrowserVariable

        return {
            "assertions": ([SyntheticsAssertion],),
            "config_variables": ([SyntheticsConfigVariable],),
            "request": (SyntheticsTestRequest,),
            "set_cookie": (str,),
            "variables": ([SyntheticsBrowserVariable],),
        }

    attribute_map = {
        "assertions": "assertions",
        "config_variables": "configVariables",
        "request": "request",
        "set_cookie": "setCookie",
        "variables": "variables",
    }

    def __init__(
        self_,
        request: SyntheticsTestRequest,
        config_variables: Union[List[SyntheticsConfigVariable], UnsetType] = unset,
        set_cookie: Union[str, UnsetType] = unset,
        variables: Union[List[SyntheticsBrowserVariable], UnsetType] = unset,
        **kwargs,
    ):
        """
        Configuration object for a Synthetic browser test.

        :param assertions: Array of assertions used for the test.
        :type assertions: [SyntheticsAssertion]

        :param config_variables: Array of variables used for the test.
        :type config_variables: [SyntheticsConfigVariable], optional

        :param request: Object describing the Synthetic test request.
        :type request: SyntheticsTestRequest

        :param set_cookie: Cookies to be used for the request, using the `Set-Cookie <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie>`_ syntax.
        :type set_cookie: str, optional

        :param variables: Array of variables used for the test steps.
        :type variables: [SyntheticsBrowserVariable], optional
        """
        if config_variables is not unset:
            kwargs["config_variables"] = config_variables
        if set_cookie is not unset:
            kwargs["set_cookie"] = set_cookie
        if variables is not unset:
            kwargs["variables"] = variables
        super().__init__(kwargs)
        assertions = kwargs.get("assertions", [])

        self_.assertions = assertions
        self_.request = request
