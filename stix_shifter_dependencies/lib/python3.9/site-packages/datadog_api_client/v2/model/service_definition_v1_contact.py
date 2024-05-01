# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class ServiceDefinitionV1Contact(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "email": (str,),
            "slack": (str,),
        }

    attribute_map = {
        "email": "email",
        "slack": "slack",
    }

    def __init__(self_, email: Union[str, UnsetType] = unset, slack: Union[str, UnsetType] = unset, **kwargs):
        """
        Contact information about the service.

        :param email: Service owner’s email.
        :type email: str, optional

        :param slack: Service owner’s Slack channel.
        :type slack: str, optional
        """
        if email is not unset:
            kwargs["email"] = email
        if slack is not unset:
            kwargs["slack"] = slack
        super().__init__(kwargs)
