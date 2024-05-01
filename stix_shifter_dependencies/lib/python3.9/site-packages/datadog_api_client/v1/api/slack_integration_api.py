# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v1.model.slack_integration_channels import SlackIntegrationChannels
from datadog_api_client.v1.model.slack_integration_channel import SlackIntegrationChannel


class SlackIntegrationApi:
    """
    Configure your `Datadog-Slack integration <https://docs.datadoghq.com/integrations/slack>`_
    directly through the Datadog API.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_slack_integration_channel_endpoint = _Endpoint(
            settings={
                "response_type": (SlackIntegrationChannel,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/slack/configuration/accounts/{account_name}/channels",
                "operation_id": "create_slack_integration_channel",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "account_name": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "account_name",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (SlackIntegrationChannel,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._get_slack_integration_channel_endpoint = _Endpoint(
            settings={
                "response_type": (SlackIntegrationChannel,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/slack/configuration/accounts/{account_name}/channels/{channel_name}",
                "operation_id": "get_slack_integration_channel",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "account_name": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "account_name",
                    "location": "path",
                },
                "channel_name": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "channel_name",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_slack_integration_channels_endpoint = _Endpoint(
            settings={
                "response_type": (SlackIntegrationChannels,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/slack/configuration/accounts/{account_name}/channels",
                "operation_id": "get_slack_integration_channels",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "account_name": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "account_name",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._remove_slack_integration_channel_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/slack/configuration/accounts/{account_name}/channels/{channel_name}",
                "operation_id": "remove_slack_integration_channel",
                "http_method": "DELETE",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "account_name": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "account_name",
                    "location": "path",
                },
                "channel_name": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "channel_name",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._update_slack_integration_channel_endpoint = _Endpoint(
            settings={
                "response_type": (SlackIntegrationChannel,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/slack/configuration/accounts/{account_name}/channels/{channel_name}",
                "operation_id": "update_slack_integration_channel",
                "http_method": "PATCH",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "account_name": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "account_name",
                    "location": "path",
                },
                "channel_name": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "channel_name",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (SlackIntegrationChannel,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_slack_integration_channel(
        self,
        account_name: str,
        body: SlackIntegrationChannel,
    ) -> SlackIntegrationChannel:
        """Create a Slack integration channel.

        Add a channel to your Datadog-Slack integration.

        :param account_name: Your Slack account name.
        :type account_name: str
        :param body: Payload describing Slack channel to be created
        :type body: SlackIntegrationChannel
        :rtype: SlackIntegrationChannel
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_name"] = account_name

        kwargs["body"] = body

        return self._create_slack_integration_channel_endpoint.call_with_http_info(**kwargs)

    def get_slack_integration_channel(
        self,
        account_name: str,
        channel_name: str,
    ) -> SlackIntegrationChannel:
        """Get a Slack integration channel.

        Get a channel configured for your Datadog-Slack integration.

        :param account_name: Your Slack account name.
        :type account_name: str
        :param channel_name: The name of the Slack channel being operated on.
        :type channel_name: str
        :rtype: SlackIntegrationChannel
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_name"] = account_name

        kwargs["channel_name"] = channel_name

        return self._get_slack_integration_channel_endpoint.call_with_http_info(**kwargs)

    def get_slack_integration_channels(
        self,
        account_name: str,
    ) -> SlackIntegrationChannels:
        """Get all channels in a Slack integration.

        Get a list of all channels configured for your Datadog-Slack integration.

        :param account_name: Your Slack account name.
        :type account_name: str
        :rtype: SlackIntegrationChannels
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_name"] = account_name

        return self._get_slack_integration_channels_endpoint.call_with_http_info(**kwargs)

    def remove_slack_integration_channel(
        self,
        account_name: str,
        channel_name: str,
    ) -> None:
        """Remove a Slack integration channel.

        Remove a channel from your Datadog-Slack integration.

        :param account_name: Your Slack account name.
        :type account_name: str
        :param channel_name: The name of the Slack channel being operated on.
        :type channel_name: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_name"] = account_name

        kwargs["channel_name"] = channel_name

        return self._remove_slack_integration_channel_endpoint.call_with_http_info(**kwargs)

    def update_slack_integration_channel(
        self,
        account_name: str,
        channel_name: str,
        body: SlackIntegrationChannel,
    ) -> SlackIntegrationChannel:
        """Update a Slack integration channel.

        Update a channel used in your Datadog-Slack integration.

        :param account_name: Your Slack account name.
        :type account_name: str
        :param channel_name: The name of the Slack channel being operated on.
        :type channel_name: str
        :param body: Payload describing fields and values to be updated.
        :type body: SlackIntegrationChannel
        :rtype: SlackIntegrationChannel
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_name"] = account_name

        kwargs["channel_name"] = channel_name

        kwargs["body"] = body

        return self._update_slack_integration_channel_endpoint.call_with_http_info(**kwargs)
