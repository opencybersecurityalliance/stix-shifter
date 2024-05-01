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
    from datadog_api_client.v1.model.synthetics_private_location_secrets_authentication import (
        SyntheticsPrivateLocationSecretsAuthentication,
    )
    from datadog_api_client.v1.model.synthetics_private_location_secrets_config_decryption import (
        SyntheticsPrivateLocationSecretsConfigDecryption,
    )


class SyntheticsPrivateLocationSecrets(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_private_location_secrets_authentication import (
            SyntheticsPrivateLocationSecretsAuthentication,
        )
        from datadog_api_client.v1.model.synthetics_private_location_secrets_config_decryption import (
            SyntheticsPrivateLocationSecretsConfigDecryption,
        )

        return {
            "authentication": (SyntheticsPrivateLocationSecretsAuthentication,),
            "config_decryption": (SyntheticsPrivateLocationSecretsConfigDecryption,),
        }

    attribute_map = {
        "authentication": "authentication",
        "config_decryption": "config_decryption",
    }

    def __init__(
        self_,
        authentication: Union[SyntheticsPrivateLocationSecretsAuthentication, UnsetType] = unset,
        config_decryption: Union[SyntheticsPrivateLocationSecretsConfigDecryption, UnsetType] = unset,
        **kwargs,
    ):
        """
        Secrets for the private location. Only present in the response when creating the private location.

        :param authentication: Authentication part of the secrets.
        :type authentication: SyntheticsPrivateLocationSecretsAuthentication, optional

        :param config_decryption: Private key for the private location.
        :type config_decryption: SyntheticsPrivateLocationSecretsConfigDecryption, optional
        """
        if authentication is not unset:
            kwargs["authentication"] = authentication
        if config_decryption is not unset:
            kwargs["config_decryption"] = config_decryption
        super().__init__(kwargs)
