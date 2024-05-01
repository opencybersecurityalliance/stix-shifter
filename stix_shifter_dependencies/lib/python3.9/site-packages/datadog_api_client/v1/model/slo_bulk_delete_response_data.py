# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class SLOBulkDeleteResponseData(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "deleted": ([str],),
            "updated": ([str],),
        }

    attribute_map = {
        "deleted": "deleted",
        "updated": "updated",
    }

    def __init__(
        self_, deleted: Union[List[str], UnsetType] = unset, updated: Union[List[str], UnsetType] = unset, **kwargs
    ):
        """
        An array of service level objective objects.

        :param deleted: An array of service level objective object IDs that indicates
            which objects that were completely deleted.
        :type deleted: [str], optional

        :param updated: An array of service level objective object IDs that indicates
            which objects that were modified (objects for which at least one
            threshold was deleted, but that were not completely deleted).
        :type updated: [str], optional
        """
        if deleted is not unset:
            kwargs["deleted"] = deleted
        if updated is not unset:
            kwargs["updated"] = updated
        super().__init__(kwargs)
