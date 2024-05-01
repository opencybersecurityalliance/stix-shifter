# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.formula_limit import FormulaLimit


class QueryFormula(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.formula_limit import FormulaLimit

        return {
            "formula": (str,),
            "limit": (FormulaLimit,),
        }

    attribute_map = {
        "formula": "formula",
        "limit": "limit",
    }

    def __init__(self_, formula: str, limit: Union[FormulaLimit, UnsetType] = unset, **kwargs):
        """
        A formula for calculation based on one or more queries.

        :param formula: Formula string, referencing one or more queries with their name property.
        :type formula: str

        :param limit: Message for specifying limits to the number of values returned by a query.
        :type limit: FormulaLimit, optional
        """
        if limit is not unset:
            kwargs["limit"] = limit
        super().__init__(kwargs)

        self_.formula = formula
