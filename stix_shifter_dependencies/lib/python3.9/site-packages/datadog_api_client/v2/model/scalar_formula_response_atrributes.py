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
    from datadog_api_client.v2.model.scalar_column import ScalarColumn
    from datadog_api_client.v2.model.group_scalar_column import GroupScalarColumn
    from datadog_api_client.v2.model.data_scalar_column import DataScalarColumn


class ScalarFormulaResponseAtrributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.scalar_column import ScalarColumn

        return {
            "columns": ([ScalarColumn],),
        }

    attribute_map = {
        "columns": "columns",
    }

    def __init__(
        self_,
        columns: Union[List[Union[ScalarColumn, GroupScalarColumn, DataScalarColumn]], UnsetType] = unset,
        **kwargs,
    ):
        """
        The object describing a scalar response.

        :param columns: List of response columns, each corresponding to an individual formula or query in the request and with values in parallel arrays matching the series list.
        :type columns: [ScalarColumn], optional
        """
        if columns is not unset:
            kwargs["columns"] = columns
        super().__init__(kwargs)
