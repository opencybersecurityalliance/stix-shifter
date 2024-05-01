# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    date,
    datetime,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.ci_app_computes import CIAppComputes


class CIAppPipelinesBucketResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.ci_app_computes import CIAppComputes

        return {
            "by": (
                {
                    str: (
                        bool,
                        date,
                        datetime,
                        dict,
                        float,
                        int,
                        list,
                        str,
                        none_type,
                    )
                },
            ),
            "computes": (CIAppComputes,),
        }

    attribute_map = {
        "by": "by",
        "computes": "computes",
    }

    def __init__(
        self_, by: Union[Dict[str, Any], UnsetType] = unset, computes: Union[CIAppComputes, UnsetType] = unset, **kwargs
    ):
        """
        Bucket values.

        :param by: The key-value pairs for each group-by.
        :type by: {str: (bool, date, datetime, dict, float, int, list, str, none_type,)}, optional

        :param computes: A map of the metric name to value for regular compute, or a list of values for a timeseries.
        :type computes: CIAppComputes, optional
        """
        if by is not unset:
            kwargs["by"] = by
        if computes is not unset:
            kwargs["computes"] = computes
        super().__init__(kwargs)
