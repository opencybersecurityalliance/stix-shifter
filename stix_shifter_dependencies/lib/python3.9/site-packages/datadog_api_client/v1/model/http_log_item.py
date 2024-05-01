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


class HTTPLogItem(ModelNormal):
    @cached_property
    def additional_properties_type(_):
        return (str,)

    @cached_property
    def openapi_types(_):
        return {
            "ddsource": (str,),
            "ddtags": (str,),
            "hostname": (str,),
            "message": (str,),
            "service": (str,),
        }

    attribute_map = {
        "ddsource": "ddsource",
        "ddtags": "ddtags",
        "hostname": "hostname",
        "message": "message",
        "service": "service",
    }

    def __init__(
        self_,
        message: str,
        ddsource: Union[str, UnsetType] = unset,
        ddtags: Union[str, UnsetType] = unset,
        hostname: Union[str, UnsetType] = unset,
        service: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Logs that are sent over HTTP.

        :param ddsource: The integration name associated with your log: the technology from which the log originated.
            When it matches an integration name, Datadog automatically installs the corresponding parsers and facets.
            See `reserved attributes <https://docs.datadoghq.com/logs/log_collection/#reserved-attributes>`_.
        :type ddsource: str, optional

        :param ddtags: Tags associated with your logs.
        :type ddtags: str, optional

        :param hostname: The name of the originating host of the log.
        :type hostname: str, optional

        :param message: The message `reserved attribute <https://docs.datadoghq.com/logs/log_collection/#reserved-attributes>`_
            of your log. By default, Datadog ingests the value of the message attribute as the body of the log entry.
            That value is then highlighted and displayed in the Logstream, where it is indexed for full text search.
        :type message: str

        :param service: The name of the application or service generating the log events.
            It is used to switch from Logs to APM, so make sure you define the same value when you use both products.
            See `reserved attributes <https://docs.datadoghq.com/logs/log_collection/#reserved-attributes>`_.
        :type service: str, optional
        """
        if ddsource is not unset:
            kwargs["ddsource"] = ddsource
        if ddtags is not unset:
            kwargs["ddtags"] = ddtags
        if hostname is not unset:
            kwargs["hostname"] = hostname
        if service is not unset:
            kwargs["service"] = service
        super().__init__(kwargs)

        self_.message = message
