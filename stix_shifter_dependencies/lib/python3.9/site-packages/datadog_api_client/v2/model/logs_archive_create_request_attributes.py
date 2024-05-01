# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.logs_archive_create_request_destination import LogsArchiveCreateRequestDestination
    from datadog_api_client.v2.model.logs_archive_destination_azure import LogsArchiveDestinationAzure
    from datadog_api_client.v2.model.logs_archive_destination_gcs import LogsArchiveDestinationGCS
    from datadog_api_client.v2.model.logs_archive_destination_s3 import LogsArchiveDestinationS3


class LogsArchiveCreateRequestAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.logs_archive_create_request_destination import (
            LogsArchiveCreateRequestDestination,
        )

        return {
            "destination": (LogsArchiveCreateRequestDestination,),
            "include_tags": (bool,),
            "name": (str,),
            "query": (str,),
            "rehydration_max_scan_size_in_gb": (int, none_type),
            "rehydration_tags": ([str],),
        }

    attribute_map = {
        "destination": "destination",
        "include_tags": "include_tags",
        "name": "name",
        "query": "query",
        "rehydration_max_scan_size_in_gb": "rehydration_max_scan_size_in_gb",
        "rehydration_tags": "rehydration_tags",
    }

    def __init__(
        self_,
        destination: Union[
            LogsArchiveCreateRequestDestination,
            LogsArchiveDestinationAzure,
            LogsArchiveDestinationGCS,
            LogsArchiveDestinationS3,
        ],
        name: str,
        query: str,
        include_tags: Union[bool, UnsetType] = unset,
        rehydration_max_scan_size_in_gb: Union[int, none_type, UnsetType] = unset,
        rehydration_tags: Union[List[str], UnsetType] = unset,
        **kwargs,
    ):
        """
        The attributes associated with the archive.

        :param destination: An archive's destination.
        :type destination: LogsArchiveCreateRequestDestination

        :param include_tags: To store the tags in the archive, set the value "true".
            If it is set to "false", the tags will be deleted when the logs are sent to the archive.
        :type include_tags: bool, optional

        :param name: The archive name.
        :type name: str

        :param query: The archive query/filter. Logs matching this query are included in the archive.
        :type query: str

        :param rehydration_max_scan_size_in_gb: Maximum scan size for rehydration from this archive.
        :type rehydration_max_scan_size_in_gb: int, none_type, optional

        :param rehydration_tags: An array of tags to add to rehydrated logs from an archive.
        :type rehydration_tags: [str], optional
        """
        if include_tags is not unset:
            kwargs["include_tags"] = include_tags
        if rehydration_max_scan_size_in_gb is not unset:
            kwargs["rehydration_max_scan_size_in_gb"] = rehydration_max_scan_size_in_gb
        if rehydration_tags is not unset:
            kwargs["rehydration_tags"] = rehydration_tags
        super().__init__(kwargs)

        self_.destination = destination
        self_.name = name
        self_.query = query
