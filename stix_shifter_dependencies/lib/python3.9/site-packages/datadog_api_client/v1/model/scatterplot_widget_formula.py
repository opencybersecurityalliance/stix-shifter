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
    from datadog_api_client.v1.model.scatterplot_dimension import ScatterplotDimension


class ScatterplotWidgetFormula(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.scatterplot_dimension import ScatterplotDimension

        return {
            "alias": (str,),
            "dimension": (ScatterplotDimension,),
            "formula": (str,),
        }

    attribute_map = {
        "alias": "alias",
        "dimension": "dimension",
        "formula": "formula",
    }

    def __init__(self_, dimension: ScatterplotDimension, formula: str, alias: Union[str, UnsetType] = unset, **kwargs):
        """
        Formula to be used in a Scatterplot widget query.

        :param alias: Expression alias.
        :type alias: str, optional

        :param dimension: Dimension of the Scatterplot.
        :type dimension: ScatterplotDimension

        :param formula: String expression built from queries, formulas, and functions.
        :type formula: str
        """
        if alias is not unset:
            kwargs["alias"] = alias
        super().__init__(kwargs)

        self_.dimension = dimension
        self_.formula = formula
