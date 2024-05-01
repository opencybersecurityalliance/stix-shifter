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
    from datadog_api_client.v2.model.logs_archive_destination import LogsArchiveDestination
    from datadog_api_client.v2.model.logs_archive_state import LogsArchiveState
    from datadog_api_client.v2.model.logs_archive_destination_azure import LogsArchiveDestinationAzure
    from datadog_api_client.v2.model.logs_archive_destination_gcs import LogsArchiveDestinationGCS
    from datadog_api_client.v2.model.logs_archive_destination_s3 import LogsArchiveDestinationS3


class LogsArchiveAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.logs_archive_destination import LogsArchiveDestination
        from datadog_api_client.v2.model.logs_archive_state import LogsArchiveState

        return {
            "destination": (LogsArchiveDestination,),
            "include_tags": (bool,),
            "name": (str,),
            "query": (str,),
            "rehydration_max_scan_size_in_gb": (int, none_type),
            "rehydration_tags": ([str],),
            "state": (LogsArchiveState,),
        }

    attribute_map = {
        "destination": "destination",
        "include_tags": "include_tags",
        "name": "name",
        "query": "query",
        "rehydration_max_scan_size_in_gb": "rehydration_max_scan_size_in_gb",
        "rehydration_tags": "rehydration_tags",
        "state": "state",
    }

    def __init__(
        self_,
        destination: Union[
            Union[
                LogsArchiveDestination, LogsArchiveDestinationAzure, LogsArchiveDestinationGCS, LogsArchiveDestinationS3
            ],
            none_type,
        ],
        name: str,
        query: str,
        include_tags: Union[bool, UnsetType] = unset,
        rehydration_max_scan_size_in_gb: Union[int, none_type, UnsetType] = unset,
        rehydration_tags: Union[List[str], UnsetType] = unset,
        state: Union[LogsArchiveState, UnsetType] = unset,
        **kwargs,
    ):
        """
        The attributes associated with the archive.

        :param destination: An archive's destination.
        :type destination: LogsArchiveDestination, none_type

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

        :param state: The state of the archive.
        :type state: LogsArchiveState, optional
        """
        if include_tags is not unset:
            kwargs["include_tags"] = include_tags
        if rehydration_max_scan_size_in_gb is not unset:
            kwargs["rehydration_max_scan_size_in_gb"] = rehydration_max_scan_size_in_gb
        if rehydration_tags is not unset:
            kwargs["rehydration_tags"] = rehydration_tags
        if state is not unset:
            kwargs["state"] = state
        super().__init__(kwargs)

        self_.destination = destination
        self_.name = name
        self_.query = query
