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
    from datadog_api_client.v1.model.synthetics_basic_auth_ntlm_type import SyntheticsBasicAuthNTLMType


class SyntheticsBasicAuthNTLM(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_basic_auth_ntlm_type import SyntheticsBasicAuthNTLMType

        return {
            "domain": (str,),
            "password": (str,),
            "type": (SyntheticsBasicAuthNTLMType,),
            "username": (str,),
            "workstation": (str,),
        }

    attribute_map = {
        "domain": "domain",
        "password": "password",
        "type": "type",
        "username": "username",
        "workstation": "workstation",
    }

    def __init__(
        self_,
        type: SyntheticsBasicAuthNTLMType,
        domain: Union[str, UnsetType] = unset,
        password: Union[str, UnsetType] = unset,
        username: Union[str, UnsetType] = unset,
        workstation: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object to handle ``NTLM`` authentication when performing the test.

        :param domain: Domain for the authentication to use when performing the test.
        :type domain: str, optional

        :param password: Password for the authentication to use when performing the test.
        :type password: str, optional

        :param type: The type of authentication to use when performing the test.
        :type type: SyntheticsBasicAuthNTLMType

        :param username: Username for the authentication to use when performing the test.
        :type username: str, optional

        :param workstation: Workstation for the authentication to use when performing the test.
        :type workstation: str, optional
        """
        if domain is not unset:
            kwargs["domain"] = domain
        if password is not unset:
            kwargs["password"] = password
        if username is not unset:
            kwargs["username"] = username
        if workstation is not unset:
            kwargs["workstation"] = workstation
        super().__init__(kwargs)

        self_.type = type
