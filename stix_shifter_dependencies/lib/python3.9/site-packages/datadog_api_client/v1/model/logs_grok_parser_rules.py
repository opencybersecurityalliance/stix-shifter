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


class LogsGrokParserRules(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "match_rules": (str,),
            "support_rules": (str,),
        }

    attribute_map = {
        "match_rules": "match_rules",
        "support_rules": "support_rules",
    }

    def __init__(self_, match_rules: str, support_rules: Union[str, UnsetType] = unset, **kwargs):
        """
        Set of rules for the grok parser.

        :param match_rules: List of match rules for the grok parser, separated by a new line.
        :type match_rules: str

        :param support_rules: List of support rules for the grok parser, separated by a new line.
        :type support_rules: str, optional
        """
        if support_rules is not unset:
            kwargs["support_rules"] = support_rules
        super().__init__(kwargs)

        self_.match_rules = match_rules
