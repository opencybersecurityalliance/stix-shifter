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
    from datadog_api_client.v1.model.synthetics_deleted_test import SyntheticsDeletedTest


class SyntheticsDeleteTestsResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_deleted_test import SyntheticsDeletedTest

        return {
            "deleted_tests": ([SyntheticsDeletedTest],),
        }

    attribute_map = {
        "deleted_tests": "deleted_tests",
    }

    def __init__(self_, deleted_tests: Union[List[SyntheticsDeletedTest], UnsetType] = unset, **kwargs):
        """
        Response object for deleting Synthetic tests.

        :param deleted_tests: Array of objects containing a deleted Synthetic test ID with
            the associated deletion timestamp.
        :type deleted_tests: [SyntheticsDeletedTest], optional
        """
        if deleted_tests is not unset:
            kwargs["deleted_tests"] = deleted_tests
        super().__init__(kwargs)
