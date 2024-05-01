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
    from datadog_api_client.v2.model.logs_archive_attributes import LogsArchiveAttributes


class LogsArchiveDefinition(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.logs_archive_attributes import LogsArchiveAttributes

        return {
            "attributes": (LogsArchiveAttributes,),
            "id": (str,),
            "type": (str,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }
    read_only_vars = {
        "id",
        "type",
    }

    def __init__(
        self_, attributes: Union[LogsArchiveAttributes, UnsetType] = unset, id: Union[str, UnsetType] = unset, **kwargs
    ):
        """
        The definition of an archive.

        :param attributes: The attributes associated with the archive.
        :type attributes: LogsArchiveAttributes, optional

        :param id: The archive ID.
        :type id: str, optional

        :param type: The type of the resource. The value should always be archives.
        :type type: str
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if id is not unset:
            kwargs["id"] = id
        super().__init__(kwargs)
        type = kwargs.get("type", "archives")

        self_.type = type
