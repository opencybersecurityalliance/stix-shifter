# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    datetime,
    unset,
    UnsetType,
)


class SyntheticsDeletedTest(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "deleted_at": (datetime,),
            "public_id": (str,),
        }

    attribute_map = {
        "deleted_at": "deleted_at",
        "public_id": "public_id",
    }

    def __init__(
        self_, deleted_at: Union[datetime, UnsetType] = unset, public_id: Union[str, UnsetType] = unset, **kwargs
    ):
        """
        Object containing a deleted Synthetic test ID with the associated
        deletion timestamp.

        :param deleted_at: Deletion timestamp of the Synthetic test ID.
        :type deleted_at: datetime, optional

        :param public_id: The Synthetic test ID deleted.
        :type public_id: str, optional
        """
        if deleted_at is not unset:
            kwargs["deleted_at"] = deleted_at
        if public_id is not unset:
            kwargs["public_id"] = public_id
        super().__init__(kwargs)
