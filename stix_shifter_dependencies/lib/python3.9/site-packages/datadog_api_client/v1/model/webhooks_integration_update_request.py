# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.webhooks_integration_encoding import WebhooksIntegrationEncoding


class WebhooksIntegrationUpdateRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.webhooks_integration_encoding import WebhooksIntegrationEncoding

        return {
            "custom_headers": (str,),
            "encode_as": (WebhooksIntegrationEncoding,),
            "name": (str,),
            "payload": (str, none_type),
            "url": (str,),
        }

    attribute_map = {
        "custom_headers": "custom_headers",
        "encode_as": "encode_as",
        "name": "name",
        "payload": "payload",
        "url": "url",
    }

    def __init__(
        self_,
        custom_headers: Union[str, UnsetType] = unset,
        encode_as: Union[WebhooksIntegrationEncoding, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        payload: Union[str, none_type, UnsetType] = unset,
        url: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Update request of a Webhooks integration object.

        *All properties are optional.*

        :param custom_headers: If ``null`` , uses no header.
            If given a JSON payload, these will be headers attached to your webhook.
        :type custom_headers: str, optional

        :param encode_as: Encoding type. Can be given either ``json`` or ``form``.
        :type encode_as: WebhooksIntegrationEncoding, optional

        :param name: The name of the webhook. It corresponds with ``<WEBHOOK_NAME>``.
            Learn more on how to use it in
            `monitor notifications <https://docs.datadoghq.com/monitors/notify>`_.
        :type name: str, optional

        :param payload: If ``null`` , uses the default payload.
            If given a JSON payload, the webhook returns the payload
            specified by the given payload.
            `Webhooks variable usage <https://docs.datadoghq.com/integrations/webhooks/#usage>`_.
        :type payload: str, none_type, optional

        :param url: URL of the webhook.
        :type url: str, optional
        """
        if custom_headers is not unset:
            kwargs["custom_headers"] = custom_headers
        if encode_as is not unset:
            kwargs["encode_as"] = encode_as
        if name is not unset:
            kwargs["name"] = name
        if payload is not unset:
            kwargs["payload"] = payload
        if url is not unset:
            kwargs["url"] = url
        super().__init__(kwargs)
