# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelComposed,
    cached_property,
)


class NotebookUpdateCell(ModelComposed):
    def __init__(self, **kwargs):
        """
        Updating a notebook can either insert new cell(s) or update existing cell(s) by including the cell ``id``.
        To delete existing cell(s), simply omit it from the list of cells.

        :param attributes: The attributes of a notebook cell in create cell request. Valid cell types are `markdown`, `timeseries`, `toplist`, `heatmap`, `distribution`,
            `log_stream`. [More information on each graph visualization type.](https://docs.datadoghq.com/dashboards/widgets/)
        :type attributes: NotebookCellCreateRequestAttributes

        :param type: Type of the Notebook Cell resource.
        :type type: NotebookCellResourceType

        :param id: Notebook cell ID.
        :type id: str
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
        from datadog_api_client.v1.model.notebook_cell_create_request import NotebookCellCreateRequest
        from datadog_api_client.v1.model.notebook_cell_update_request import NotebookCellUpdateRequest

        return {
            "oneOf": [
                NotebookCellCreateRequest,
                NotebookCellUpdateRequest,
            ],
        }
