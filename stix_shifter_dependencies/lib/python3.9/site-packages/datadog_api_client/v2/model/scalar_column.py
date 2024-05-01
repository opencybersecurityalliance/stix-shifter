# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelComposed,
    cached_property,
)


class ScalarColumn(ModelComposed):
    def __init__(self, **kwargs):
        """
        A single column in a scalar query response.

        :param name: The name of the tag key or group.
        :type name: str, optional

        :param type: The type of column present.
        :type type: str, optional

        :param values: The array of tag values for each group found for the results of the formulas or queries.
        :type values: [[str]], optional

        :param meta: Metadata for the resulting numerical values.
        :type meta: ScalarMeta, optional
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
        from datadog_api_client.v2.model.group_scalar_column import GroupScalarColumn
        from datadog_api_client.v2.model.data_scalar_column import DataScalarColumn

        return {
            "oneOf": [
                GroupScalarColumn,
                DataScalarColumn,
            ],
        }
