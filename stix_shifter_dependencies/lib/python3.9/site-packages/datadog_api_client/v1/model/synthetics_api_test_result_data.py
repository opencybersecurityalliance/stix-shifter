# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    date,
    datetime,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.synthetics_ssl_certificate import SyntheticsSSLCertificate
    from datadog_api_client.v1.model.synthetics_test_process_status import SyntheticsTestProcessStatus
    from datadog_api_client.v1.model.synthetics_api_test_result_failure import SyntheticsApiTestResultFailure
    from datadog_api_client.v1.model.synthetics_timing import SyntheticsTiming


class SyntheticsAPITestResultData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_ssl_certificate import SyntheticsSSLCertificate
        from datadog_api_client.v1.model.synthetics_test_process_status import SyntheticsTestProcessStatus
        from datadog_api_client.v1.model.synthetics_api_test_result_failure import SyntheticsApiTestResultFailure
        from datadog_api_client.v1.model.synthetics_timing import SyntheticsTiming

        return {
            "cert": (SyntheticsSSLCertificate,),
            "event_type": (SyntheticsTestProcessStatus,),
            "failure": (SyntheticsApiTestResultFailure,),
            "http_status_code": (int,),
            "request_headers": ({str: (dict,)},),
            "response_body": (str,),
            "response_headers": (
                {
                    str: (
                        bool,
                        date,
                        datetime,
                        dict,
                        float,
                        int,
                        list,
                        str,
                        none_type,
                    )
                },
            ),
            "response_size": (int,),
            "timings": (SyntheticsTiming,),
        }

    attribute_map = {
        "cert": "cert",
        "event_type": "eventType",
        "failure": "failure",
        "http_status_code": "httpStatusCode",
        "request_headers": "requestHeaders",
        "response_body": "responseBody",
        "response_headers": "responseHeaders",
        "response_size": "responseSize",
        "timings": "timings",
    }

    def __init__(
        self_,
        cert: Union[SyntheticsSSLCertificate, UnsetType] = unset,
        event_type: Union[SyntheticsTestProcessStatus, UnsetType] = unset,
        failure: Union[SyntheticsApiTestResultFailure, UnsetType] = unset,
        http_status_code: Union[int, UnsetType] = unset,
        request_headers: Union[Dict[str, dict], UnsetType] = unset,
        response_body: Union[str, UnsetType] = unset,
        response_headers: Union[Dict[str, Any], UnsetType] = unset,
        response_size: Union[int, UnsetType] = unset,
        timings: Union[SyntheticsTiming, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object containing results for your Synthetic API test.

        :param cert: Object describing the SSL certificate used for a Synthetic test.
        :type cert: SyntheticsSSLCertificate, optional

        :param event_type: Status of a Synthetic test.
        :type event_type: SyntheticsTestProcessStatus, optional

        :param failure: The API test failure details.
        :type failure: SyntheticsApiTestResultFailure, optional

        :param http_status_code: The API test HTTP status code.
        :type http_status_code: int, optional

        :param request_headers: Request header object used for the API test.
        :type request_headers: {str: (dict,)}, optional

        :param response_body: Response body returned for the API test.
        :type response_body: str, optional

        :param response_headers: Response headers returned for the API test.
        :type response_headers: {str: (bool, date, datetime, dict, float, int, list, str, none_type,)}, optional

        :param response_size: Global size in byte of the API test response.
        :type response_size: int, optional

        :param timings: Object containing all metrics and their values collected for a Synthetic API test.
            Learn more about those metrics in `Synthetics documentation <https://docs.datadoghq.com/synthetics/#metrics>`_.
        :type timings: SyntheticsTiming, optional
        """
        if cert is not unset:
            kwargs["cert"] = cert
        if event_type is not unset:
            kwargs["event_type"] = event_type
        if failure is not unset:
            kwargs["failure"] = failure
        if http_status_code is not unset:
            kwargs["http_status_code"] = http_status_code
        if request_headers is not unset:
            kwargs["request_headers"] = request_headers
        if response_body is not unset:
            kwargs["response_body"] = response_body
        if response_headers is not unset:
            kwargs["response_headers"] = response_headers
        if response_size is not unset:
            kwargs["response_size"] = response_size
        if timings is not unset:
            kwargs["timings"] = timings
        super().__init__(kwargs)
