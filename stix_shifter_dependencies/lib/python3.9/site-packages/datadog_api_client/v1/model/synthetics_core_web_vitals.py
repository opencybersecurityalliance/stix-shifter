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


class SyntheticsCoreWebVitals(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "_cls": (float,),
            "lcp": (float,),
            "url": (str,),
        }

    attribute_map = {
        "_cls": "cls",
        "lcp": "lcp",
        "url": "url",
    }

    def __init__(
        self_,
        _cls: Union[float, UnsetType] = unset,
        lcp: Union[float, UnsetType] = unset,
        url: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Core Web Vitals attached to a browser test step.

        :param _cls: Cumulative Layout Shift.
        :type _cls: float, optional

        :param lcp: Largest Contentful Paint in milliseconds.
        :type lcp: float, optional

        :param url: URL attached to the metrics.
        :type url: str, optional
        """
        if _cls is not unset:
            kwargs["_cls"] = _cls
        if lcp is not unset:
            kwargs["lcp"] = lcp
        if url is not unset:
            kwargs["url"] = url
        super().__init__(kwargs)
