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
    from datadog_api_client.v2.model.query_formula import QueryFormula
    from datadog_api_client.v2.model.scalar_formula_request_queries import ScalarFormulaRequestQueries


class ScalarFormulaRequestAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.query_formula import QueryFormula
        from datadog_api_client.v2.model.scalar_formula_request_queries import ScalarFormulaRequestQueries

        return {
            "formulas": ([QueryFormula],),
            "_from": (int,),
            "queries": (ScalarFormulaRequestQueries,),
            "to": (int,),
        }

    attribute_map = {
        "formulas": "formulas",
        "_from": "from",
        "queries": "queries",
        "to": "to",
    }

    def __init__(
        self_,
        _from: int,
        queries: ScalarFormulaRequestQueries,
        to: int,
        formulas: Union[List[QueryFormula], UnsetType] = unset,
        **kwargs,
    ):
        """
        The object describing a scalar formula request.

        :param formulas: List of formulas to be calculated and returned as responses.
        :type formulas: [QueryFormula], optional

        :param _from: Start date (inclusive) of the query in milliseconds since the Unix epoch.
        :type _from: int

        :param queries: List of queries to be run and used as inputs to the formulas.
        :type queries: ScalarFormulaRequestQueries

        :param to: End date (exclusive) of the query in milliseconds since the Unix epoch.
        :type to: int
        """
        if formulas is not unset:
            kwargs["formulas"] = formulas
        super().__init__(kwargs)

        self_._from = _from
        self_.queries = queries
        self_.to = to
