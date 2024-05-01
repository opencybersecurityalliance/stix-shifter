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
    from datadog_api_client.v1.model.formula_and_function_event_query_definition_compute import (
        FormulaAndFunctionEventQueryDefinitionCompute,
    )
    from datadog_api_client.v1.model.formula_and_function_events_data_source import FormulaAndFunctionEventsDataSource
    from datadog_api_client.v1.model.formula_and_function_event_query_group_by import (
        FormulaAndFunctionEventQueryGroupBy,
    )
    from datadog_api_client.v1.model.formula_and_function_event_query_definition_search import (
        FormulaAndFunctionEventQueryDefinitionSearch,
    )


class FormulaAndFunctionEventQueryDefinition(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.formula_and_function_event_query_definition_compute import (
            FormulaAndFunctionEventQueryDefinitionCompute,
        )
        from datadog_api_client.v1.model.formula_and_function_events_data_source import (
            FormulaAndFunctionEventsDataSource,
        )
        from datadog_api_client.v1.model.formula_and_function_event_query_group_by import (
            FormulaAndFunctionEventQueryGroupBy,
        )
        from datadog_api_client.v1.model.formula_and_function_event_query_definition_search import (
            FormulaAndFunctionEventQueryDefinitionSearch,
        )

        return {
            "compute": (FormulaAndFunctionEventQueryDefinitionCompute,),
            "data_source": (FormulaAndFunctionEventsDataSource,),
            "group_by": ([FormulaAndFunctionEventQueryGroupBy],),
            "indexes": ([str],),
            "name": (str,),
            "search": (FormulaAndFunctionEventQueryDefinitionSearch,),
            "storage": (str,),
        }

    attribute_map = {
        "compute": "compute",
        "data_source": "data_source",
        "group_by": "group_by",
        "indexes": "indexes",
        "name": "name",
        "search": "search",
        "storage": "storage",
    }

    def __init__(
        self_,
        compute: FormulaAndFunctionEventQueryDefinitionCompute,
        data_source: FormulaAndFunctionEventsDataSource,
        name: str,
        group_by: Union[List[FormulaAndFunctionEventQueryGroupBy], UnsetType] = unset,
        indexes: Union[List[str], UnsetType] = unset,
        search: Union[FormulaAndFunctionEventQueryDefinitionSearch, UnsetType] = unset,
        storage: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        A formula and functions events query.

        :param compute: Compute options.
        :type compute: FormulaAndFunctionEventQueryDefinitionCompute

        :param data_source: Data source for event platform-based queries.
        :type data_source: FormulaAndFunctionEventsDataSource

        :param group_by: Group by options.
        :type group_by: [FormulaAndFunctionEventQueryGroupBy], optional

        :param indexes: An array of index names to query in the stream. Omit or use ``[]`` to query all indexes at once.
        :type indexes: [str], optional

        :param name: Name of the query for use in formulas.
        :type name: str

        :param search: Search options.
        :type search: FormulaAndFunctionEventQueryDefinitionSearch, optional

        :param storage: Option for storage location. Feature in Private Beta.
        :type storage: str, optional
        """
        if group_by is not unset:
            kwargs["group_by"] = group_by
        if indexes is not unset:
            kwargs["indexes"] = indexes
        if search is not unset:
            kwargs["search"] = search
        if storage is not unset:
            kwargs["storage"] = storage
        super().__init__(kwargs)

        self_.compute = compute
        self_.data_source = data_source
        self_.name = name
