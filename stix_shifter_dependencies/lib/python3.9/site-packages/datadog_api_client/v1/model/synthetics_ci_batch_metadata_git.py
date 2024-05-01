# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class SyntheticsCIBatchMetadataGit(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "branch": (str,),
            "commit_sha": (str,),
        }

    attribute_map = {
        "branch": "branch",
        "commit_sha": "commitSha",
    }

    def __init__(self_, branch: Union[str, UnsetType] = unset, commit_sha: Union[str, UnsetType] = unset, **kwargs):
        """
        Git information.

        :param branch: Branch name.
        :type branch: str, optional

        :param commit_sha: The commit SHA.
        :type commit_sha: str, optional
        """
        if branch is not unset:
            kwargs["branch"] = branch
        if commit_sha is not unset:
            kwargs["commit_sha"] = commit_sha
        super().__init__(kwargs)
