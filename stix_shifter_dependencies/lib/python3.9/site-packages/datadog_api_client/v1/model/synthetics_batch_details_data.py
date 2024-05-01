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
    from datadog_api_client.v1.model.synthetics_ci_batch_metadata import SyntheticsCIBatchMetadata
    from datadog_api_client.v1.model.synthetics_batch_result import SyntheticsBatchResult
    from datadog_api_client.v1.model.synthetics_status import SyntheticsStatus


class SyntheticsBatchDetailsData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_ci_batch_metadata import SyntheticsCIBatchMetadata
        from datadog_api_client.v1.model.synthetics_batch_result import SyntheticsBatchResult
        from datadog_api_client.v1.model.synthetics_status import SyntheticsStatus

        return {
            "metadata": (SyntheticsCIBatchMetadata,),
            "results": ([SyntheticsBatchResult],),
            "status": (SyntheticsStatus,),
        }

    attribute_map = {
        "metadata": "metadata",
        "results": "results",
        "status": "status",
    }

    def __init__(
        self_,
        metadata: Union[SyntheticsCIBatchMetadata, UnsetType] = unset,
        results: Union[List[SyntheticsBatchResult], UnsetType] = unset,
        status: Union[SyntheticsStatus, UnsetType] = unset,
        **kwargs,
    ):
        """
        Wrapper object that contains the details of a batch.

        :param metadata: Metadata for the Synthetics tests run.
        :type metadata: SyntheticsCIBatchMetadata, optional

        :param results: List of results for the batch.
        :type results: [SyntheticsBatchResult], optional

        :param status: Determines whether or not the batch has passed, failed, or is in progress.
        :type status: SyntheticsStatus, optional
        """
        if metadata is not unset:
            kwargs["metadata"] = metadata
        if results is not unset:
            kwargs["results"] = results
        if status is not unset:
            kwargs["status"] = status
        super().__init__(kwargs)
