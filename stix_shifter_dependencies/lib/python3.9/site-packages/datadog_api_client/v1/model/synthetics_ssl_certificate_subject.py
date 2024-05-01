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


class SyntheticsSSLCertificateSubject(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "c": (str,),
            "cn": (str,),
            "l": (str,),
            "o": (str,),
            "ou": (str,),
            "st": (str,),
            "alt_name": (str,),
        }

    attribute_map = {
        "c": "C",
        "cn": "CN",
        "l": "L",
        "o": "O",
        "ou": "OU",
        "st": "ST",
        "alt_name": "altName",
    }

    def __init__(
        self_,
        c: Union[str, UnsetType] = unset,
        cn: Union[str, UnsetType] = unset,
        l: Union[str, UnsetType] = unset,
        o: Union[str, UnsetType] = unset,
        ou: Union[str, UnsetType] = unset,
        st: Union[str, UnsetType] = unset,
        alt_name: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object describing the SSL certificate used for the test.

        :param c: Country Name associated with the certificate.
        :type c: str, optional

        :param cn: Common Name that associated with the certificate.
        :type cn: str, optional

        :param l: Locality associated with the certificate.
        :type l: str, optional

        :param o: Organization associated with the certificate.
        :type o: str, optional

        :param ou: Organizational Unit associated with the certificate.
        :type ou: str, optional

        :param st: State Or Province Name associated with the certificate.
        :type st: str, optional

        :param alt_name: Subject Alternative Name associated with the certificate.
        :type alt_name: str, optional
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
        if alt_name is not unset:
            kwargs["alt_name"] = alt_name
        super().__init__(kwargs)
