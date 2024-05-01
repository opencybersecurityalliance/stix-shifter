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


class SyntheticsSSLCertificateIssuer(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "c": (str,),
            "cn": (str,),
            "l": (str,),
            "o": (str,),
            "ou": (str,),
            "st": (str,),
        }

    attribute_map = {
        "c": "C",
        "cn": "CN",
        "l": "L",
        "o": "O",
        "ou": "OU",
        "st": "ST",
    }

    def __init__(
        self_,
        c: Union[str, UnsetType] = unset,
        cn: Union[str, UnsetType] = unset,
        l: Union[str, UnsetType] = unset,
        o: Union[str, UnsetType] = unset,
        ou: Union[str, UnsetType] = unset,
        st: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object describing the issuer of a SSL certificate.

        :param c: Country Name that issued the certificate.
        :type c: str, optional

        :param cn: Common Name that issued certificate.
        :type cn: str, optional

        :param l: Locality that issued the certificate.
        :type l: str, optional

        :param o: Organization that issued the certificate.
        :type o: str, optional

        :param ou: Organizational Unit that issued the certificate.
        :type ou: str, optional

        :param st: State Or Province Name that issued the certificate.
        :type st: str, optional
        """
        if c is not unset:
            kwargs["c"] = c
        if cn is not unset:
            kwargs["cn"] = cn
        if l is not unset:
            kwargs["l"] = l
        if o is not unset:
            kwargs["o"] = o
        if ou is not unset:
            kwargs["ou"] = ou
        if st is not unset:
            kwargs["st"] = st
        super().__init__(kwargs)
