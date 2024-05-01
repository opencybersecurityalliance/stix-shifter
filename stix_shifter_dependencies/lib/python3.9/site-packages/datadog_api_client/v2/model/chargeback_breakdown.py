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


class ChargebackBreakdown(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "charge_type": (str,),
            "cost": (float,),
            "product_name": (str,),
        }

    attribute_map = {
        "charge_type": "charge_type",
        "cost": "cost",
        "product_name": "product_name",
    }

    def __init__(
        self_,
        charge_type: Union[str, UnsetType] = unset,
        cost: Union[float, UnsetType] = unset,
        product_name: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Charges breakdown.

        :param charge_type: The type of charge for a particular product.
        :type charge_type: str, optional

        :param cost: The cost for a particular product and charge type during a given month.
        :type cost: float, optional

        :param product_name: The product for which cost is being reported.
        :type product_name: str, optional
        """
        if charge_type is not unset:
            kwargs["charge_type"] = charge_type
        if cost is not unset:
            kwargs["cost"] = cost
        if product_name is not unset:
            kwargs["product_name"] = product_name
        super().__init__(kwargs)
