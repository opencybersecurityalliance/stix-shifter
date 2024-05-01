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
    from datadog_api_client.v1.model.aws_tag_filter import AWSTagFilter


class AWSTagFilterListResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.aws_tag_filter import AWSTagFilter

        return {
            "filters": ([AWSTagFilter],),
        }

    attribute_map = {
        "filters": "filters",
    }

    def __init__(self_, filters: Union[List[AWSTagFilter], UnsetType] = unset, **kwargs):
        """
        An array of tag filter rules by ``namespace`` and tag filter string.

        :param filters: An array of tag filters.
        :type filters: [AWSTagFilter], optional
        """
        if filters is not unset:
            kwargs["filters"] = filters
        super().__init__(kwargs)
