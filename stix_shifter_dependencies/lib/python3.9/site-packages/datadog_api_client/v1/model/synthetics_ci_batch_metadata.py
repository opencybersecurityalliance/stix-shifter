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
    from datadog_api_client.v1.model.synthetics_ci_batch_metadata_ci import SyntheticsCIBatchMetadataCI
    from datadog_api_client.v1.model.synthetics_ci_batch_metadata_git import SyntheticsCIBatchMetadataGit


class SyntheticsCIBatchMetadata(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_ci_batch_metadata_ci import SyntheticsCIBatchMetadataCI
        from datadog_api_client.v1.model.synthetics_ci_batch_metadata_git import SyntheticsCIBatchMetadataGit

        return {
            "ci": (SyntheticsCIBatchMetadataCI,),
            "git": (SyntheticsCIBatchMetadataGit,),
        }

    attribute_map = {
        "ci": "ci",
        "git": "git",
    }

    def __init__(
        self_,
        ci: Union[SyntheticsCIBatchMetadataCI, UnsetType] = unset,
        git: Union[SyntheticsCIBatchMetadataGit, UnsetType] = unset,
        **kwargs,
    ):
        """
        Metadata for the Synthetics tests run.

        :param ci: Description of the CI provider.
        :type ci: SyntheticsCIBatchMetadataCI, optional

        :param git: Git information.
        :type git: SyntheticsCIBatchMetadataGit, optional
        """
        if ci is not unset:
            kwargs["ci"] = ci
        if git is not unset:
            kwargs["git"] = git
        super().__init__(kwargs)
