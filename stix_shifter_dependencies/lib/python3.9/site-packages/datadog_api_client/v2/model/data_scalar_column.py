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
    from datadog_api_client.v2.model.scalar_meta import ScalarMeta


class DataScalarColumn(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.scalar_meta import ScalarMeta

        return {
            "meta": (ScalarMeta,),
            "name": (str,),
            "type": (str,),
            "values": ([float],),
        }

    attribute_map = {
        "meta": "meta",
        "name": "name",
        "type": "type",
        "values": "values",
    }

    def __init__(
        self_,
        meta: Union[ScalarMeta, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        type: Union[str, UnsetType] = unset,
        values: Union[List[float], UnsetType] = unset,
        **kwargs,
    ):
        """
        A column containing the numerical results for a formula or query.

        :param meta: Metadata for the resulting numerical values.
        :type meta: ScalarMeta, optional

        :param name: The name referencing the formula or query for this column.
        :type name: str, optional

        :param type: The type of column present.
        :type type: str, optional

        :param values: The array of numerical values for one formula or query.
        :type values: [float], optional
        """
        if meta is not unset:
            kwargs["meta"] = meta
        if name is not unset:
            kwargs["name"] = name
        if type is not unset:
            kwargs["type"] = type
        if values is not unset:
            kwargs["values"] = values
        super().__init__(kwargs)
