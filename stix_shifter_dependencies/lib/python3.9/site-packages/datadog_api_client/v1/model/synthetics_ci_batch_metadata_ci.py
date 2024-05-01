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
    from datadog_api_client.v1.model.synthetics_ci_batch_metadata_pipeline import SyntheticsCIBatchMetadataPipeline
    from datadog_api_client.v1.model.synthetics_ci_batch_metadata_provider import SyntheticsCIBatchMetadataProvider


class SyntheticsCIBatchMetadataCI(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_ci_batch_metadata_pipeline import SyntheticsCIBatchMetadataPipeline
        from datadog_api_client.v1.model.synthetics_ci_batch_metadata_provider import SyntheticsCIBatchMetadataProvider

        return {
            "pipeline": (SyntheticsCIBatchMetadataPipeline,),
            "provider": (SyntheticsCIBatchMetadataProvider,),
        }

    attribute_map = {
        "pipeline": "pipeline",
        "provider": "provider",
    }

    def __init__(
        self_,
        pipeline: Union[SyntheticsCIBatchMetadataPipeline, UnsetType] = unset,
        provider: Union[SyntheticsCIBatchMetadataProvider, UnsetType] = unset,
        **kwargs,
    ):
        """
        Description of the CI provider.

        :param pipeline: Description of the CI pipeline.
        :type pipeline: SyntheticsCIBatchMetadataPipeline, optional

        :param provider: Description of the CI provider.
        :type provider: SyntheticsCIBatchMetadataProvider, optional
        """
        if pipeline is not unset:
            kwargs["pipeline"] = pipeline
        if provider is not unset:
            kwargs["provider"] = provider
        super().__init__(kwargs)
