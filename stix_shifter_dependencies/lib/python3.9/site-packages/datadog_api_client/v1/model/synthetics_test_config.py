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
    from datadog_api_client.v1.model.synthetics_assertion import SyntheticsAssertion
    from datadog_api_client.v1.model.synthetics_config_variable import SyntheticsConfigVariable
    from datadog_api_client.v1.model.synthetics_test_request import SyntheticsTestRequest
    from datadog_api_client.v1.model.synthetics_browser_variable import SyntheticsBrowserVariable
    from datadog_api_client.v1.model.synthetics_assertion_target import SyntheticsAssertionTarget
    from datadog_api_client.v1.model.synthetics_assertion_json_path_target import SyntheticsAssertionJSONPathTarget
    from datadog_api_client.v1.model.synthetics_assertion_x_path_target import SyntheticsAssertionXPathTarget


class SyntheticsTestConfig(ModelNormal):
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
            "variables": ([SyntheticsBrowserVariable],),
        }

    attribute_map = {
        "assertions": "assertions",
        "config_variables": "configVariables",
        "request": "request",
        "variables": "variables",
    }

    def __init__(
        self_,
        assertions: Union[
            List[
                Union[
                    SyntheticsAssertion,
                    SyntheticsAssertionTarget,
                    SyntheticsAssertionJSONPathTarget,
                    SyntheticsAssertionXPathTarget,
                ]
            ],
            UnsetType,
        ] = unset,
        config_variables: Union[List[SyntheticsConfigVariable], UnsetType] = unset,
        request: Union[SyntheticsTestRequest, UnsetType] = unset,
        variables: Union[List[SyntheticsBrowserVariable], UnsetType] = unset,
        **kwargs,
    ):
        """
        Configuration object for a Synthetic test.

        :param assertions: Array of assertions used for the test. Required for single API tests.
        :type assertions: [SyntheticsAssertion], optional

        :param config_variables: Array of variables used for the test.
        :type config_variables: [SyntheticsConfigVariable], optional

        :param request: Object describing the Synthetic test request.
        :type request: SyntheticsTestRequest, optional

        :param variables: Browser tests only - array of variables used for the test steps.
        :type variables: [SyntheticsBrowserVariable], optional
        """
        if assertions is not unset:
            kwargs["assertions"] = assertions
        if config_variables is not unset:
            kwargs["config_variables"] = config_variables
        if request is not unset:
            kwargs["request"] = request
        if variables is not unset:
            kwargs["variables"] = variables
        super().__init__(kwargs)
