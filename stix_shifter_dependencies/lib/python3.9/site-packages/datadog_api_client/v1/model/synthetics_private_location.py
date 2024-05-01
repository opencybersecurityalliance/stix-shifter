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
    from datadog_api_client.v1.model.synthetics_private_location_metadata import SyntheticsPrivateLocationMetadata
    from datadog_api_client.v1.model.synthetics_private_location_secrets import SyntheticsPrivateLocationSecrets


class SyntheticsPrivateLocation(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_private_location_metadata import SyntheticsPrivateLocationMetadata
        from datadog_api_client.v1.model.synthetics_private_location_secrets import SyntheticsPrivateLocationSecrets

        return {
            "description": (str,),
            "id": (str,),
            "metadata": (SyntheticsPrivateLocationMetadata,),
            "name": (str,),
            "secrets": (SyntheticsPrivateLocationSecrets,),
            "tags": ([str],),
        }

    attribute_map = {
        "description": "description",
        "id": "id",
        "metadata": "metadata",
        "name": "name",
        "secrets": "secrets",
        "tags": "tags",
    }
    read_only_vars = {
        "id",
        "secrets",
    }

    def __init__(
        self_,
        description: str,
        name: str,
        tags: List[str],
        id: Union[str, UnsetType] = unset,
        metadata: Union[SyntheticsPrivateLocationMetadata, UnsetType] = unset,
        secrets: Union[SyntheticsPrivateLocationSecrets, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object containing information about the private location to create.

        :param description: Description of the private location.
        :type description: str

        :param id: Unique identifier of the private location.
        :type id: str, optional

        :param metadata: Object containing metadata about the private location.
        :type metadata: SyntheticsPrivateLocationMetadata, optional

        :param name: Name of the private location.
        :type name: str

        :param secrets: Secrets for the private location. Only present in the response when creating the private location.
        :type secrets: SyntheticsPrivateLocationSecrets, optional

        :param tags: Array of tags attached to the private location.
        :type tags: [str]
        """
        if id is not unset:
            kwargs["id"] = id
        if metadata is not unset:
            kwargs["metadata"] = metadata
        if secrets is not unset:
            kwargs["secrets"] = secrets
        super().__init__(kwargs)

        self_.description = description
        self_.name = name
        self_.tags = tags
