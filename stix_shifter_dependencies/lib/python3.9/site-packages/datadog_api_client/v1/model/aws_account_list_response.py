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
    from datadog_api_client.v1.model.aws_account import AWSAccount


class AWSAccountListResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.aws_account import AWSAccount

        return {
            "accounts": ([AWSAccount],),
        }

    attribute_map = {
        "accounts": "accounts",
    }

    def __init__(self_, accounts: Union[List[AWSAccount], UnsetType] = unset, **kwargs):
        """
        List of enabled AWS accounts.

        :param accounts: List of enabled AWS accounts.
        :type accounts: [AWSAccount], optional
        """
        if accounts is not unset:
            kwargs["accounts"] = accounts
        super().__init__(kwargs)
