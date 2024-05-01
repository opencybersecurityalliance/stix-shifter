# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict, Union

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.model_utils import (
    UnsetType,
    unset,
)
from datadog_api_client.v1.model.notebooks_response import NotebooksResponse
from datadog_api_client.v1.model.notebook_response import NotebookResponse
from datadog_api_client.v1.model.notebook_create_request import NotebookCreateRequest
from datadog_api_client.v1.model.notebook_update_request import NotebookUpdateRequest


class NotebooksApi:
    """
    Interact with your notebooks through the API to make it easier to organize, find, and
    share all of your notebooks with your team and organization. For more information, see the
    `Notebooks documentation <https://docs.datadoghq.com/notebooks/>`_.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_notebook_endpoint = _Endpoint(
            settings={
                "response_type": (NotebookResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/notebooks",
                "operation_id": "create_notebook",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (NotebookCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_notebook_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/notebooks/{notebook_id}",
                "operation_id": "delete_notebook",
                "http_method": "DELETE",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "notebook_id": {
                    "required": True,
                    "openapi_types": (int,),
                    "attribute": "notebook_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_notebook_endpoint = _Endpoint(
            settings={
                "response_type": (NotebookResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/notebooks/{notebook_id}",
                "operation_id": "get_notebook",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "notebook_id": {
                    "required": True,
                    "openapi_types": (int,),
                    "attribute": "notebook_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_notebooks_endpoint = _Endpoint(
            settings={
                "response_type": (NotebooksResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/notebooks",
                "operation_id": "list_notebooks",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "author_handle": {
                    "openapi_types": (str,),
                    "attribute": "author_handle",
                    "location": "query",
                },
                "exclude_author_handle": {
                    "openapi_types": (str,),
                    "attribute": "exclude_author_handle",
                    "location": "query",
                },
                "start": {
                    "openapi_types": (int,),
                    "attribute": "start",
                    "location": "query",
                },
                "count": {
                    "openapi_types": (int,),
                    "attribute": "count",
                    "location": "query",
                },
                "sort_field": {
                    "openapi_types": (str,),
                    "attribute": "sort_field",
                    "location": "query",
                },
                "sort_dir": {
                    "openapi_types": (str,),
                    "attribute": "sort_dir",
                    "location": "query",
                },
                "query": {
                    "openapi_types": (str,),
                    "attribute": "query",
                    "location": "query",
                },
                "include_cells": {
                    "openapi_types": (bool,),
                    "attribute": "include_cells",
                    "location": "query",
                },
                "is_template": {
                    "openapi_types": (bool,),
                    "attribute": "is_template",
                    "location": "query",
                },
                "type": {
                    "openapi_types": (str,),
                    "attribute": "type",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._update_notebook_endpoint = _Endpoint(
            settings={
                "response_type": (NotebookResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/notebooks/{notebook_id}",
                "operation_id": "update_notebook",
                "http_method": "PUT",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "notebook_id": {
                    "required": True,
                    "openapi_types": (int,),
                    "attribute": "notebook_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (NotebookUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_notebook(
        self,
        body: NotebookCreateRequest,
    ) -> NotebookResponse:
        """Create a notebook.

        Create a notebook using the specified options.

        :param body: The JSON description of the notebook you want to create.
        :type body: NotebookCreateRequest
        :rtype: NotebookResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_notebook_endpoint.call_with_http_info(**kwargs)

    def delete_notebook(
        self,
        notebook_id: int,
    ) -> None:
        """Delete a notebook.

        Delete a notebook using the specified ID.

        :param notebook_id: Unique ID, assigned when you create the notebook.
        :type notebook_id: int
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["notebook_id"] = notebook_id

        return self._delete_notebook_endpoint.call_with_http_info(**kwargs)

    def get_notebook(
        self,
        notebook_id: int,
    ) -> NotebookResponse:
        """Get a notebook.

        Get a notebook using the specified notebook ID.

        :param notebook_id: Unique ID, assigned when you create the notebook.
        :type notebook_id: int
        :rtype: NotebookResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["notebook_id"] = notebook_id

        return self._get_notebook_endpoint.call_with_http_info(**kwargs)

    def list_notebooks(
        self,
        *,
        author_handle: Union[str, UnsetType] = unset,
        exclude_author_handle: Union[str, UnsetType] = unset,
        start: Union[int, UnsetType] = unset,
        count: Union[int, UnsetType] = unset,
        sort_field: Union[str, UnsetType] = unset,
        sort_dir: Union[str, UnsetType] = unset,
        query: Union[str, UnsetType] = unset,
        include_cells: Union[bool, UnsetType] = unset,
        is_template: Union[bool, UnsetType] = unset,
        type: Union[str, UnsetType] = unset,
    ) -> NotebooksResponse:
        """Get all notebooks.

        Get all notebooks. This can also be used to search for notebooks with a particular ``query`` in the notebook
        ``name`` or author ``handle``.

        :param author_handle: Return notebooks created by the given ``author_handle``.
        :type author_handle: str, optional
        :param exclude_author_handle: Return notebooks not created by the given ``author_handle``.
        :type exclude_author_handle: str, optional
        :param start: The index of the first notebook you want returned.
        :type start: int, optional
        :param count: The number of notebooks to be returned.
        :type count: int, optional
        :param sort_field: Sort by field ``modified`` , ``name`` , or ``created``.
        :type sort_field: str, optional
        :param sort_dir: Sort by direction ``asc`` or ``desc``.
        :type sort_dir: str, optional
        :param query: Return only notebooks with ``query`` string in notebook name or author handle.
        :type query: str, optional
        :param include_cells: Value of ``false`` excludes the ``cells`` and global ``time`` for each notebook.
        :type include_cells: bool, optional
        :param is_template: True value returns only template notebooks. Default is false (returns only non-template notebooks).
        :type is_template: bool, optional
        :param type: If type is provided, returns only notebooks with that metadata type. Default does not have type filtering.
        :type type: str, optional
        :rtype: NotebooksResponse
        """
        kwargs: Dict[str, Any] = {}
        if author_handle is not unset:
            kwargs["author_handle"] = author_handle

        if exclude_author_handle is not unset:
            kwargs["exclude_author_handle"] = exclude_author_handle

        if start is not unset:
            kwargs["start"] = start

        if count is not unset:
            kwargs["count"] = count

        if sort_field is not unset:
            kwargs["sort_field"] = sort_field

        if sort_dir is not unset:
            kwargs["sort_dir"] = sort_dir

        if query is not unset:
            kwargs["query"] = query

        if include_cells is not unset:
            kwargs["include_cells"] = include_cells

        if is_template is not unset:
            kwargs["is_template"] = is_template

        if type is not unset:
            kwargs["type"] = type

        return self._list_notebooks_endpoint.call_with_http_info(**kwargs)

    def update_notebook(
        self,
        notebook_id: int,
        body: NotebookUpdateRequest,
    ) -> NotebookResponse:
        """Update a notebook.

        Update a notebook using the specified ID.

        :param notebook_id: Unique ID, assigned when you create the notebook.
        :type notebook_id: int
        :param body: Update notebook request body.
        :type body: NotebookUpdateRequest
        :rtype: NotebookResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["notebook_id"] = notebook_id

        kwargs["body"] = body

        return self._update_notebook_endpoint.call_with_http_info(**kwargs)
