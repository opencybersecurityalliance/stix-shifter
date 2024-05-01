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
    from datadog_api_client.v2.model.unit import Unit


class ScalarMeta(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.unit import Unit

        return {
            "unit": ([Unit, none_type],),
        }

    attribute_map = {
        "unit": "unit",
    }

    def __init__(self_, unit: Union[List[Unit], UnsetType] = unset, **kwargs):
        """
        Metadata for the resulting numerical values.

        :param unit: Detailed information about the unit.
            First element describes the "primary unit" (for example, ``bytes`` in ``bytes per second`` ).
            The second element describes the "per unit" (for example, ``second`` in ``bytes per second`` ).
            If the second element is not present, the API returns null.
        :type unit: [Unit, none_type], optional
        """
        if unit is not unset:
            kwargs["unit"] = unit
        super().__init__(kwargs)
