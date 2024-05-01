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
    from datadog_api_client.v1.model.synthetics_test_ci_options import SyntheticsTestCiOptions
    from datadog_api_client.v1.model.synthetics_device_id import SyntheticsDeviceID
    from datadog_api_client.v1.model.synthetics_test_options_http_version import SyntheticsTestOptionsHTTPVersion
    from datadog_api_client.v1.model.synthetics_test_options_monitor_options import SyntheticsTestOptionsMonitorOptions
    from datadog_api_client.v1.model.synthetics_restricted_roles import SyntheticsRestrictedRoles
    from datadog_api_client.v1.model.synthetics_test_options_retry import SyntheticsTestOptionsRetry
    from datadog_api_client.v1.model.synthetics_browser_test_rum_settings import SyntheticsBrowserTestRumSettings
    from datadog_api_client.v1.model.synthetics_test_options_scheduling import SyntheticsTestOptionsScheduling


class SyntheticsTestOptions(ModelNormal):
    validations = {
        "monitor_priority": {
            "inclusive_maximum": 5,
            "inclusive_minimum": 1,
        },
        "tick_every": {
            "inclusive_maximum": 604800,
            "inclusive_minimum": 30,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_test_ci_options import SyntheticsTestCiOptions
        from datadog_api_client.v1.model.synthetics_device_id import SyntheticsDeviceID
        from datadog_api_client.v1.model.synthetics_test_options_http_version import SyntheticsTestOptionsHTTPVersion
        from datadog_api_client.v1.model.synthetics_test_options_monitor_options import (
            SyntheticsTestOptionsMonitorOptions,
        )
        from datadog_api_client.v1.model.synthetics_restricted_roles import SyntheticsRestrictedRoles
        from datadog_api_client.v1.model.synthetics_test_options_retry import SyntheticsTestOptionsRetry
        from datadog_api_client.v1.model.synthetics_browser_test_rum_settings import SyntheticsBrowserTestRumSettings
        from datadog_api_client.v1.model.synthetics_test_options_scheduling import SyntheticsTestOptionsScheduling

        return {
            "accept_self_signed": (bool,),
            "allow_insecure": (bool,),
            "check_certificate_revocation": (bool,),
            "ci": (SyntheticsTestCiOptions,),
            "device_ids": ([SyntheticsDeviceID],),
            "disable_cors": (bool,),
            "disable_csp": (bool,),
            "follow_redirects": (bool,),
            "http_version": (SyntheticsTestOptionsHTTPVersion,),
            "ignore_server_certificate_error": (bool,),
            "initial_navigation_timeout": (int,),
            "min_failure_duration": (int,),
            "min_location_failed": (int,),
            "monitor_name": (str,),
            "monitor_options": (SyntheticsTestOptionsMonitorOptions,),
            "monitor_priority": (int,),
            "no_screenshot": (bool,),
            "restricted_roles": (SyntheticsRestrictedRoles,),
            "retry": (SyntheticsTestOptionsRetry,),
            "rum_settings": (SyntheticsBrowserTestRumSettings,),
            "scheduling": (SyntheticsTestOptionsScheduling,),
            "tick_every": (int,),
        }

    attribute_map = {
        "accept_self_signed": "accept_self_signed",
        "allow_insecure": "allow_insecure",
        "check_certificate_revocation": "checkCertificateRevocation",
        "ci": "ci",
        "device_ids": "device_ids",
        "disable_cors": "disableCors",
        "disable_csp": "disableCsp",
        "follow_redirects": "follow_redirects",
        "http_version": "httpVersion",
        "ignore_server_certificate_error": "ignoreServerCertificateError",
        "initial_navigation_timeout": "initialNavigationTimeout",
        "min_failure_duration": "min_failure_duration",
        "min_location_failed": "min_location_failed",
        "monitor_name": "monitor_name",
        "monitor_options": "monitor_options",
        "monitor_priority": "monitor_priority",
        "no_screenshot": "noScreenshot",
        "restricted_roles": "restricted_roles",
        "retry": "retry",
        "rum_settings": "rumSettings",
        "scheduling": "scheduling",
        "tick_every": "tick_every",
    }

    def __init__(
        self_,
        accept_self_signed: Union[bool, UnsetType] = unset,
        allow_insecure: Union[bool, UnsetType] = unset,
        check_certificate_revocation: Union[bool, UnsetType] = unset,
        ci: Union[SyntheticsTestCiOptions, UnsetType] = unset,
        device_ids: Union[List[SyntheticsDeviceID], UnsetType] = unset,
        disable_cors: Union[bool, UnsetType] = unset,
        disable_csp: Union[bool, UnsetType] = unset,
        follow_redirects: Union[bool, UnsetType] = unset,
        http_version: Union[SyntheticsTestOptionsHTTPVersion, UnsetType] = unset,
        ignore_server_certificate_error: Union[bool, UnsetType] = unset,
        initial_navigation_timeout: Union[int, UnsetType] = unset,
        min_failure_duration: Union[int, UnsetType] = unset,
        min_location_failed: Union[int, UnsetType] = unset,
        monitor_name: Union[str, UnsetType] = unset,
        monitor_options: Union[SyntheticsTestOptionsMonitorOptions, UnsetType] = unset,
        monitor_priority: Union[int, UnsetType] = unset,
        no_screenshot: Union[bool, UnsetType] = unset,
        restricted_roles: Union[SyntheticsRestrictedRoles, UnsetType] = unset,
        retry: Union[SyntheticsTestOptionsRetry, UnsetType] = unset,
        rum_settings: Union[SyntheticsBrowserTestRumSettings, UnsetType] = unset,
        scheduling: Union[SyntheticsTestOptionsScheduling, UnsetType] = unset,
        tick_every: Union[int, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object describing the extra options for a Synthetic test.

        :param accept_self_signed: For SSL test, whether or not the test should allow self signed
            certificates.
        :type accept_self_signed: bool, optional

        :param allow_insecure: Allows loading insecure content for an HTTP request in an API test.
        :type allow_insecure: bool, optional

        :param check_certificate_revocation: For SSL test, whether or not the test should fail on revoked certificate in stapled OCSP.
        :type check_certificate_revocation: bool, optional

        :param ci: CI/CD options for a Synthetic test.
        :type ci: SyntheticsTestCiOptions, optional

        :param device_ids: For browser test, array with the different device IDs used to run the test.
        :type device_ids: [SyntheticsDeviceID], optional

        :param disable_cors: Whether or not to disable CORS mechanism.
        :type disable_cors: bool, optional

        :param disable_csp: Disable Content Security Policy for browser tests.
        :type disable_csp: bool, optional

        :param follow_redirects: For API HTTP test, whether or not the test should follow redirects.
        :type follow_redirects: bool, optional

        :param http_version: HTTP version to use for a Synthetic test.
        :type http_version: SyntheticsTestOptionsHTTPVersion, optional

        :param ignore_server_certificate_error: Ignore server certificate error for browser tests.
        :type ignore_server_certificate_error: bool, optional

        :param initial_navigation_timeout: Timeout before declaring the initial step as failed (in seconds) for browser tests.
        :type initial_navigation_timeout: int, optional

        :param min_failure_duration: Minimum amount of time in failure required to trigger an alert.
        :type min_failure_duration: int, optional

        :param min_location_failed: Minimum number of locations in failure required to trigger
            an alert.
        :type min_location_failed: int, optional

        :param monitor_name: The monitor name is used for the alert title as well as for all monitor dashboard widgets and SLOs.
        :type monitor_name: str, optional

        :param monitor_options: Object containing the options for a Synthetic test as a monitor
            (for example, renotification).
        :type monitor_options: SyntheticsTestOptionsMonitorOptions, optional

        :param monitor_priority: Integer from 1 (high) to 5 (low) indicating alert severity.
        :type monitor_priority: int, optional

        :param no_screenshot: Prevents saving screenshots of the steps.
        :type no_screenshot: bool, optional

        :param restricted_roles: A list of role identifiers that can be pulled from the Roles API, for restricting read and write access.
        :type restricted_roles: SyntheticsRestrictedRoles, optional

        :param retry: Object describing the retry strategy to apply to a Synthetic test.
        :type retry: SyntheticsTestOptionsRetry, optional

        :param rum_settings: The RUM data collection settings for the Synthetic browser test.
            **Note:** There are 3 ways to format RUM settings:

            ``{ isEnabled: false }``
            RUM data is not collected.

            ``{ isEnabled: true }``
            RUM data is collected from the Synthetic test's default application.

            ``{ isEnabled: true, applicationId: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", clientTokenId: 12345 }``
            RUM data is collected using the specified application.
        :type rum_settings: SyntheticsBrowserTestRumSettings, optional

        :param scheduling: Object containing timeframes and timezone used for advanced scheduling.
        :type scheduling: SyntheticsTestOptionsScheduling, optional

        :param tick_every: The frequency at which to run the Synthetic test (in seconds).
        :type tick_every: int, optional
        """
        if accept_self_signed is not unset:
            kwargs["accept_self_signed"] = accept_self_signed
        if allow_insecure is not unset:
            kwargs["allow_insecure"] = allow_insecure
        if check_certificate_revocation is not unset:
            kwargs["check_certificate_revocation"] = check_certificate_revocation
        if ci is not unset:
            kwargs["ci"] = ci
        if device_ids is not unset:
            kwargs["device_ids"] = device_ids
        if disable_cors is not unset:
            kwargs["disable_cors"] = disable_cors
        if disable_csp is not unset:
            kwargs["disable_csp"] = disable_csp
        if follow_redirects is not unset:
            kwargs["follow_redirects"] = follow_redirects
        if http_version is not unset:
            kwargs["http_version"] = http_version
        if ignore_server_certificate_error is not unset:
            kwargs["ignore_server_certificate_error"] = ignore_server_certificate_error
        if initial_navigation_timeout is not unset:
            kwargs["initial_navigation_timeout"] = initial_navigation_timeout
        if min_failure_duration is not unset:
            kwargs["min_failure_duration"] = min_failure_duration
        if min_location_failed is not unset:
            kwargs["min_location_failed"] = min_location_failed
        if monitor_name is not unset:
            kwargs["monitor_name"] = monitor_name
        if monitor_options is not unset:
            kwargs["monitor_options"] = monitor_options
        if monitor_priority is not unset:
            kwargs["monitor_priority"] = monitor_priority
        if no_screenshot is not unset:
            kwargs["no_screenshot"] = no_screenshot
        if restricted_roles is not unset:
            kwargs["restricted_roles"] = restricted_roles
        if retry is not unset:
            kwargs["retry"] = retry
        if rum_settings is not unset:
            kwargs["rum_settings"] = rum_settings
        if scheduling is not unset:
            kwargs["scheduling"] = scheduling
        if tick_every is not unset:
            kwargs["tick_every"] = tick_every
        super().__init__(kwargs)
