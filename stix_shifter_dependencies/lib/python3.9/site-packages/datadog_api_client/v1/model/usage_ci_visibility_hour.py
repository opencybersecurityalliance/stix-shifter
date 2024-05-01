# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


class UsageCIVisibilityHour(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "ci_pipeline_indexed_spans": (int, none_type),
            "ci_test_indexed_spans": (int, none_type),
            "ci_visibility_pipeline_committers": (int, none_type),
            "ci_visibility_test_committers": (int, none_type),
            "org_name": (str,),
            "public_id": (str,),
        }

    attribute_map = {
        "ci_pipeline_indexed_spans": "ci_pipeline_indexed_spans",
        "ci_test_indexed_spans": "ci_test_indexed_spans",
        "ci_visibility_pipeline_committers": "ci_visibility_pipeline_committers",
        "ci_visibility_test_committers": "ci_visibility_test_committers",
        "org_name": "org_name",
        "public_id": "public_id",
    }

    def __init__(
        self_,
        ci_pipeline_indexed_spans: Union[int, none_type, UnsetType] = unset,
        ci_test_indexed_spans: Union[int, none_type, UnsetType] = unset,
        ci_visibility_pipeline_committers: Union[int, none_type, UnsetType] = unset,
        ci_visibility_test_committers: Union[int, none_type, UnsetType] = unset,
        org_name: Union[str, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        CI visibility usage in a given hour.

        :param ci_pipeline_indexed_spans: The number of spans for pipelines in the queried hour.
        :type ci_pipeline_indexed_spans: int, none_type, optional

        :param ci_test_indexed_spans: The number of spans for tests in the queried hour.
        :type ci_test_indexed_spans: int, none_type, optional

        :param ci_visibility_pipeline_committers: Shows the total count of all active Git committers for Pipelines in the current month. A committer is active if they commit at least 3 times in a given month.
        :type ci_visibility_pipeline_committers: int, none_type, optional

        :param ci_visibility_test_committers: The total count of all active Git committers for tests in the current month. A committer is active if they commit at least 3 times in a given month.
        :type ci_visibility_test_committers: int, none_type, optional

        :param org_name: The organization name.
        :type org_name: str, optional

        :param public_id: The organization public ID.
        :type public_id: str, optional
        """
        if ci_pipeline_indexed_spans is not unset:
            kwargs["ci_pipeline_indexed_spans"] = ci_pipeline_indexed_spans
        if ci_test_indexed_spans is not unset:
            kwargs["ci_test_indexed_spans"] = ci_test_indexed_spans
        if ci_visibility_pipeline_committers is not unset:
            kwargs["ci_visibility_pipeline_committers"] = ci_visibility_pipeline_committers
        if ci_visibility_test_committers is not unset:
            kwargs["ci_visibility_test_committers"] = ci_visibility_test_committers
        if org_name is not unset:
            kwargs["org_name"] = org_name
        if public_id is not unset:
            kwargs["public_id"] = public_id
        super().__init__(kwargs)
