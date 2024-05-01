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
    from datadog_api_client.v1.model.synthetics_basic_auth_sigv4_type import SyntheticsBasicAuthSigv4Type


class SyntheticsBasicAuthSigv4(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_basic_auth_sigv4_type import SyntheticsBasicAuthSigv4Type

        return {
            "access_key": (str,),
            "region": (str,),
            "secret_key": (str,),
            "service_name": (str,),
            "session_token": (str,),
            "type": (SyntheticsBasicAuthSigv4Type,),
        }

    attribute_map = {
        "access_key": "accessKey",
        "region": "region",
        "secret_key": "secretKey",
        "service_name": "serviceName",
        "session_token": "sessionToken",
        "type": "type",
    }

    def __init__(
        self_,
        access_key: str,
        secret_key: str,
        type: SyntheticsBasicAuthSigv4Type,
        region: Union[str, UnsetType] = unset,
        service_name: Union[str, UnsetType] = unset,
        session_token: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object to handle ``SIGV4`` authentication when performing the test.

        :param access_key: Access key for the ``SIGV4`` authentication.
        :type access_key: str

        :param region: Region for the ``SIGV4`` authentication.
        :type region: str, optional

        :param secret_key: Secret key for the ``SIGV4`` authentication.
        :type secret_key: str

        :param service_name: Service name for the ``SIGV4`` authentication.
        :type service_name: str, optional

        :param session_token: Session token for the ``SIGV4`` authentication.
        :type session_token: str, optional

        :param type: The type of authentication to use when performing the test.
        :type type: SyntheticsBasicAuthSigv4Type
        """
        if region is not unset:
            kwargs["region"] = region
        if service_name is not unset:
            kwargs["service_name"] = service_name
        if session_token is not unset:
            kwargs["session_token"] = session_token
        super().__init__(kwargs)

        self_.access_key = access_key
        self_.secret_key = secret_key
        self_.type = type
