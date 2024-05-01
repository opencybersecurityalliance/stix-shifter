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
    from datadog_api_client.v1.model.synthetics_ci_batch_metadata import SyntheticsCIBatchMetadata


class SyntheticsTriggerTest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_ci_batch_metadata import SyntheticsCIBatchMetadata

        return {
            "metadata": (SyntheticsCIBatchMetadata,),
            "public_id": (str,),
        }

    attribute_map = {
        "metadata": "metadata",
        "public_id": "public_id",
    }

    def __init__(self_, public_id: str, metadata: Union[SyntheticsCIBatchMetadata, UnsetType] = unset, **kwargs):
        """
        Test configuration for Synthetics

        :param metadata: Metadata for the Synthetics tests run.
        :type metadata: SyntheticsCIBatchMetadata, optional

        :param public_id: The public ID of the Synthetics test to trigger.
        :type public_id: str
        """
        if metadata is not unset:
            kwargs["metadata"] = metadata
        super().__init__(kwargs)

        self_.public_id = public_id
