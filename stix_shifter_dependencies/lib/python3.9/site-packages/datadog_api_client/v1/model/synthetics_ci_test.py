# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Dict, List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.synthetics_basic_auth import SyntheticsBasicAuth
    from datadog_api_client.v1.model.synthetics_device_id import SyntheticsDeviceID
    from datadog_api_client.v1.model.synthetics_test_headers import SyntheticsTestHeaders
    from datadog_api_client.v1.model.synthetics_ci_batch_metadata import SyntheticsCIBatchMetadata
    from datadog_api_client.v1.model.synthetics_test_options_retry import SyntheticsTestOptionsRetry
    from datadog_api_client.v1.model.synthetics_basic_auth_web import SyntheticsBasicAuthWeb
    from datadog_api_client.v1.model.synthetics_basic_auth_sigv4 import SyntheticsBasicAuthSigv4
    from datadog_api_client.v1.model.synthetics_basic_auth_ntlm import SyntheticsBasicAuthNTLM
    from datadog_api_client.v1.model.synthetics_basic_auth_digest import SyntheticsBasicAuthDigest
    from datadog_api_client.v1.model.synthetics_basic_auth_oauth_client import SyntheticsBasicAuthOauthClient
    from datadog_api_client.v1.model.synthetics_basic_auth_oauth_rop import SyntheticsBasicAuthOauthROP


class SyntheticsCITest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_basic_auth import SyntheticsBasicAuth
        from datadog_api_client.v1.model.synthetics_device_id import SyntheticsDeviceID
        from datadog_api_client.v1.model.synthetics_test_headers import SyntheticsTestHeaders
        from datadog_api_client.v1.model.synthetics_ci_batch_metadata import SyntheticsCIBatchMetadata
        from datadog_api_client.v1.model.synthetics_test_options_retry import SyntheticsTestOptionsRetry

        return {
            "allow_insecure_certificates": (bool,),
            "basic_auth": (SyntheticsBasicAuth,),
            "body": (str,),
            "body_type": (str,),
            "cookies": (str,),
            "device_ids": ([SyntheticsDeviceID],),
            "follow_redirects": (bool,),
            "headers": (SyntheticsTestHeaders,),
            "locations": ([str],),
            "metadata": (SyntheticsCIBatchMetadata,),
            "public_id": (str,),
            "retry": (SyntheticsTestOptionsRetry,),
            "start_url": (str,),
            "variables": ({str: (str,)},),
        }

    attribute_map = {
        "allow_insecure_certificates": "allowInsecureCertificates",
        "basic_auth": "basicAuth",
        "body": "body",
        "body_type": "bodyType",
        "cookies": "cookies",
        "device_ids": "deviceIds",
        "follow_redirects": "followRedirects",
        "headers": "headers",
        "locations": "locations",
        "metadata": "metadata",
        "public_id": "public_id",
        "retry": "retry",
        "start_url": "startUrl",
        "variables": "variables",
    }

    def __init__(
        self_,
        public_id: str,
        allow_insecure_certificates: Union[bool, UnsetType] = unset,
        basic_auth: Union[
            SyntheticsBasicAuth,
            SyntheticsBasicAuthWeb,
            SyntheticsBasicAuthSigv4,
            SyntheticsBasicAuthNTLM,
            SyntheticsBasicAuthDigest,
            SyntheticsBasicAuthOauthClient,
            SyntheticsBasicAuthOauthROP,
            UnsetType,
        ] = unset,
        body: Union[str, UnsetType] = unset,
        body_type: Union[str, UnsetType] = unset,
        cookies: Union[str, UnsetType] = unset,
        device_ids: Union[List[SyntheticsDeviceID], UnsetType] = unset,
        follow_redirects: Union[bool, UnsetType] = unset,
        headers: Union[SyntheticsTestHeaders, UnsetType] = unset,
        locations: Union[List[str], UnsetType] = unset,
        metadata: Union[SyntheticsCIBatchMetadata, UnsetType] = unset,
        retry: Union[SyntheticsTestOptionsRetry, UnsetType] = unset,
        start_url: Union[str, UnsetType] = unset,
        variables: Union[Dict[str, str], UnsetType] = unset,
        **kwargs,
    ):
        """
        Test configuration for Synthetics CI

        :param allow_insecure_certificates: Disable certificate checks in API tests.
        :type allow_insecure_certificates: bool, optional

        :param basic_auth: Object to handle basic authentication when performing the test.
        :type basic_auth: SyntheticsBasicAuth, optional

        :param body: Body to include in the test.
        :type body: str, optional

        :param body_type: Type of the data sent in a synthetics API test.
        :type body_type: str, optional

        :param cookies: Cookies for the request.
        :type cookies: str, optional

        :param device_ids: For browser test, array with the different device IDs used to run the test.
        :type device_ids: [SyntheticsDeviceID], optional

        :param follow_redirects: For API HTTP test, whether or not the test should follow redirects.
        :type follow_redirects: bool, optional

        :param headers: Headers to include when performing the test.
        :type headers: SyntheticsTestHeaders, optional

        :param locations: Array of locations used to run the test.
        :type locations: [str], optional

        :param metadata: Metadata for the Synthetics tests run.
        :type metadata: SyntheticsCIBatchMetadata, optional

        :param public_id: The public ID of the Synthetics test to trigger.
        :type public_id: str

        :param retry: Object describing the retry strategy to apply to a Synthetic test.
        :type retry: SyntheticsTestOptionsRetry, optional

        :param start_url: Starting URL for the browser test.
        :type start_url: str, optional

        :param variables: Variables to replace in the test.
        :type variables: {str: (str,)}, optional
        """
        if allow_insecure_certificates is not unset:
            kwargs["allow_insecure_certificates"] = allow_insecure_certificates
        if basic_auth is not unset:
            kwargs["basic_auth"] = basic_auth
        if body is not unset:
            kwargs["body"] = body
        if body_type is not unset:
            kwargs["body_type"] = body_type
        if cookies is not unset:
            kwargs["cookies"] = cookies
        if device_ids is not unset:
            kwargs["device_ids"] = device_ids
        if follow_redirects is not unset:
            kwargs["follow_redirects"] = follow_redirects
        if headers is not unset:
            kwargs["headers"] = headers
        if locations is not unset:
            kwargs["locations"] = locations
        if metadata is not unset:
            kwargs["metadata"] = metadata
        if retry is not unset:
            kwargs["retry"] = retry
        if start_url is not unset:
            kwargs["start_url"] = start_url
        if variables is not unset:
            kwargs["variables"] = variables
        super().__init__(kwargs)

        self_.public_id = public_id
