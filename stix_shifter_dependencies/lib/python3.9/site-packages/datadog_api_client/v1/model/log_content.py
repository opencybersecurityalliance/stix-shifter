# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict, List, Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    date,
    datetime,
    none_type,
    unset,
    UnsetType,
)


class LogContent(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "attributes": (
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
            "host": (str,),
            "message": (str,),
            "service": (str,),
            "tags": ([str],),
            "timestamp": (datetime,),
        }

    attribute_map = {
        "attributes": "attributes",
        "host": "host",
        "message": "message",
        "service": "service",
        "tags": "tags",
        "timestamp": "timestamp",
    }

    def __init__(
        self_,
        attributes: Union[Dict[str, Any], UnsetType] = unset,
        host: Union[str, UnsetType] = unset,
        message: Union[str, UnsetType] = unset,
        service: Union[str, UnsetType] = unset,
        tags: Union[List[str], UnsetType] = unset,
        timestamp: Union[datetime, UnsetType] = unset,
        **kwargs,
    ):
        """
        JSON object containing all log attributes and their associated values.

        :param attributes: JSON object of attributes from your log.
        :type attributes: {str: (bool, date, datetime, dict, float, int, list, str, none_type,)}, optional

        :param host: Name of the machine from where the logs are being sent.
        :type host: str, optional

        :param message: The message `reserved attribute <https://docs.datadoghq.com/logs/log_collection/#reserved-attributes>`_
            of your log. By default, Datadog ingests the value of the message attribute as the body of the log entry.
            That value is then highlighted and displayed in the Logstream, where it is indexed for full text search.
        :type message: str, optional

        :param service: The name of the application or service generating the log events.
            It is used to switch from Logs to APM, so make sure you define the same
            value when you use both products.
        :type service: str, optional

        :param tags: Array of tags associated with your log.
        :type tags: [str], optional

        :param timestamp: Timestamp of your log.
        :type timestamp: datetime, optional
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if host is not unset:
            kwargs["host"] = host
        if message is not unset:
            kwargs["message"] = message
        if service is not unset:
            kwargs["service"] = service
        if tags is not unset:
            kwargs["tags"] = tags
        if timestamp is not unset:
            kwargs["timestamp"] = timestamp
        super().__init__(kwargs)
