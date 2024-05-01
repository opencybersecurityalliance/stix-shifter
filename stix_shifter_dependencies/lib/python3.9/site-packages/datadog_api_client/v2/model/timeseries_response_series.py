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
    from datadog_api_client.v2.model.group_tags import GroupTags
    from datadog_api_client.v2.model.unit import Unit


class TimeseriesResponseSeries(ModelNormal):
    validations = {
        "query_index": {
            "inclusive_maximum": 2147483647,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.group_tags import GroupTags
        from datadog_api_client.v2.model.unit import Unit

        return {
            "group_tags": (GroupTags,),
            "query_index": (int,),
            "unit": ([Unit, none_type],),
        }

    attribute_map = {
        "group_tags": "group_tags",
        "query_index": "query_index",
        "unit": "unit",
    }

    def __init__(
        self_,
        group_tags: Union[GroupTags, UnsetType] = unset,
        query_index: Union[int, UnsetType] = unset,
        unit: Union[List[Unit], UnsetType] = unset,
        **kwargs,
    ):
        """


        :param group_tags: List of tags that apply to a single response value.
        :type group_tags: GroupTags, optional

        :param query_index: The index of the query in the "formulas" array (or "queries" array if no "formulas" was specified).
        :type query_index: int, optional

        :param unit: Detailed information about the unit.
            The first element describes the "primary unit" (for example, ``bytes`` in ``bytes per second`` ).
            The second element describes the "per unit" (for example, ``second`` in ``bytes per second`` ).
            If the second element is not present, the API returns null.
        :type unit: [Unit, none_type], optional
        """
        if group_tags is not unset:
            kwargs["group_tags"] = group_tags
        if query_index is not unset:
            kwargs["query_index"] = query_index
        if unit is not unset:
            kwargs["unit"] = unit
        super().__init__(kwargs)
