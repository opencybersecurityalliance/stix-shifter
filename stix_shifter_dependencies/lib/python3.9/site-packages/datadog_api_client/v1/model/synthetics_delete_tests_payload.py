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


class SyntheticsDeleteTestsPayload(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "public_ids": ([str],),
        }

    attribute_map = {
        "public_ids": "public_ids",
    }

    def __init__(self_, public_ids: Union[List[str], UnsetType] = unset, **kwargs):
        """
        A JSON list of the ID or IDs of the Synthetic tests that you want
        to delete.

        :param public_ids: An array of Synthetic test IDs you want to delete.
        :type public_ids: [str], optional
        """
        if public_ids is not unset:
            kwargs["public_ids"] = public_ids
        super().__init__(kwargs)
