# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelComposed,
    cached_property,
)


class MonitorFormulaAndFunctionQueryDefinition(ModelComposed):
    def __init__(self, **kwargs):
        """
        A formula and function query.

        :param compute: Compute options.
        :type compute: MonitorFormulaAndFunctionEventQueryDefinitionCompute

        :param data_source: Data source for event platform-based queries.
        :type data_source: MonitorFormulaAndFunctionEventsDataSource

        :param group_by: Group by options.
        :type group_by: [MonitorFormulaAndFunctionEventQueryGroupBy], optional

        :param indexes: An array of index names to query in the stream. Omit or use `[]` to query all indexes at once.
        :type indexes: [str], optional

        :param name: Name of the query for use in formulas.
        :type name: str

        :param search: Search options.
        :type search: MonitorFormulaAndFunctionEventQueryDefinitionSearch, optional
        """
        super().__init__(kwargs)

    @cached_property
    def _composed_schemas(_):
        # we need this here to make our import statements work
        # we must store _composed_schemas in here so the code is only run
        # when we invoke this method. If we kept this at the class
        # level we would get an error because the class level
        # code would be run when this module is imported, and these composed
        # classes don't exist yet because their module has not finished
        # loading
        from datadog_api_client.v1.model.monitor_formula_and_function_event_query_definition import (
            MonitorFormulaAndFunctionEventQueryDefinition,
        )

        return {
            "oneOf": [
                MonitorFormulaAndFunctionEventQueryDefinition,
            ],
        }
