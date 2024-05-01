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
    from datadog_api_client.v1.model.synthetics_test_request_certificate_item import (
        SyntheticsTestRequestCertificateItem,
    )


class SyntheticsTestRequestCertificate(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_test_request_certificate_item import (
            SyntheticsTestRequestCertificateItem,
        )

        return {
            "cert": (SyntheticsTestRequestCertificateItem,),
            "key": (SyntheticsTestRequestCertificateItem,),
        }

    attribute_map = {
        "cert": "cert",
        "key": "key",
    }

    def __init__(
        self_,
        cert: Union[SyntheticsTestRequestCertificateItem, UnsetType] = unset,
        key: Union[SyntheticsTestRequestCertificateItem, UnsetType] = unset,
        **kwargs,
    ):
        """
        Client certificate to use when performing the test request.

        :param cert: Define a request certificate.
        :type cert: SyntheticsTestRequestCertificateItem, optional

        :param key: Define a request certificate.
        :type key: SyntheticsTestRequestCertificateItem, optional
        """
        if cert is not unset:
            kwargs["cert"] = cert
        if key is not unset:
            kwargs["key"] = key
        super().__init__(kwargs)
