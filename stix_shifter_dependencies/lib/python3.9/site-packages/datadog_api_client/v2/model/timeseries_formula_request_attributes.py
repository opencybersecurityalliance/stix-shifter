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
    from datadog_api_client.v2.model.timeseries_formula_request_queries import TimeseriesFormulaRequestQueries


class TimeseriesFormulaRequestAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.query_formula import QueryFormula
        from datadog_api_client.v2.model.timeseries_formula_request_queries import TimeseriesFormulaRequestQueries

        return {
            "formulas": ([QueryFormula],),
            "_from": (int,),
            "interval": (int,),
            "queries": (TimeseriesFormulaRequestQueries,),
            "to": (int,),
        }

    attribute_map = {
        "formulas": "formulas",
        "_from": "from",
        "interval": "interval",
        "queries": "queries",
        "to": "to",
    }

    def __init__(
        self_,
        _from: int,
        queries: TimeseriesFormulaRequestQueries,
        to: int,
        formulas: Union[List[QueryFormula], UnsetType] = unset,
        interval: Union[int, UnsetType] = unset,
        **kwargs,
    ):
        """
        The object describing a timeseries formula request.

        :param formulas: List of formulas to be calculated and returned as responses.
        :type formulas: [QueryFormula], optional

        :param _from: Start date (inclusive) of the query in milliseconds since the Unix epoch.
        :type _from: int

        :param interval: A time interval in milliseconds.
            May be overridden by a larger interval if the query would result in
            too many points for the specified timeframe.
            Defaults to a reasonable interval for the given timeframe.
        :type interval: int, optional

        :param queries: List of queries to be run and used as inputs to the formulas.
        :type queries: TimeseriesFormulaRequestQueries

        :param to: End date (exclusive) of the query in milliseconds since the Unix epoch.
        :type to: int
        """
        if formulas is not unset:
            kwargs["formulas"] = formulas
        if interval is not unset:
            kwargs["interval"] = interval
        super().__init__(kwargs)

        self_._from = _from
        self_.queries = queries
        self_.to = to
