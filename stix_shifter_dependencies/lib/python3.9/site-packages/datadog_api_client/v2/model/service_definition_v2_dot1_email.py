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
    from datadog_api_client.v2.model.service_definition_v2_dot1_email_type import ServiceDefinitionV2Dot1EmailType


class ServiceDefinitionV2Dot1Email(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.service_definition_v2_dot1_email_type import ServiceDefinitionV2Dot1EmailType

        return {
            "contact": (str,),
            "name": (str,),
            "type": (ServiceDefinitionV2Dot1EmailType,),
        }

    attribute_map = {
        "contact": "contact",
        "name": "name",
        "type": "type",
    }

    def __init__(
        self_, contact: str, type: ServiceDefinitionV2Dot1EmailType, name: Union[str, UnsetType] = unset, **kwargs
    ):
        """
        Service owner's email.

        :param contact: Contact value.
        :type contact: str

        :param name: Contact email.
        :type name: str, optional

        :param type: Contact type.
        :type type: ServiceDefinitionV2Dot1EmailType
        """
        if name is not unset:
            kwargs["name"] = name
        super().__init__(kwargs)

        self_.contact = contact
        self_.type = type
