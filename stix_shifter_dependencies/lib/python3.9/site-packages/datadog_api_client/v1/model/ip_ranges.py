# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.ip_prefixes_agents import IPPrefixesAgents
    from datadog_api_client.v1.model.ip_prefixes_api import IPPrefixesAPI
    from datadog_api_client.v1.model.ip_prefixes_apm import IPPrefixesAPM
    from datadog_api_client.v1.model.ip_prefixes_logs import IPPrefixesLogs
    from datadog_api_client.v1.model.ip_prefixes_orchestrator import IPPrefixesOrchestrator
    from datadog_api_client.v1.model.ip_prefixes_process import IPPrefixesProcess
    from datadog_api_client.v1.model.ip_prefixes_synthetics import IPPrefixesSynthetics
    from datadog_api_client.v1.model.ip_prefixes_synthetics_private_locations import (
        IPPrefixesSyntheticsPrivateLocations,
    )
    from datadog_api_client.v1.model.ip_prefixes_webhooks import IPPrefixesWebhooks


class IPRanges(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.ip_prefixes_agents import IPPrefixesAgents
        from datadog_api_client.v1.model.ip_prefixes_api import IPPrefixesAPI
        from datadog_api_client.v1.model.ip_prefixes_apm import IPPrefixesAPM
        from datadog_api_client.v1.model.ip_prefixes_logs import IPPrefixesLogs
        from datadog_api_client.v1.model.ip_prefixes_orchestrator import IPPrefixesOrchestrator
        from datadog_api_client.v1.model.ip_prefixes_process import IPPrefixesProcess
        from datadog_api_client.v1.model.ip_prefixes_synthetics import IPPrefixesSynthetics
        from datadog_api_client.v1.model.ip_prefixes_synthetics_private_locations import (
            IPPrefixesSyntheticsPrivateLocations,
        )
        from datadog_api_client.v1.model.ip_prefixes_webhooks import IPPrefixesWebhooks

        return {
            "agents": (IPPrefixesAgents,),
            "api": (IPPrefixesAPI,),
            "apm": (IPPrefixesAPM,),
            "logs": (IPPrefixesLogs,),
            "modified": (str,),
            "orchestrator": (IPPrefixesOrchestrator,),
            "process": (IPPrefixesProcess,),
            "synthetics": (IPPrefixesSynthetics,),
            "synthetics_private_locations": (IPPrefixesSyntheticsPrivateLocations,),
            "version": (int,),
            "webhooks": (IPPrefixesWebhooks,),
        }

    attribute_map = {
        "agents": "agents",
        "api": "api",
        "apm": "apm",
        "logs": "logs",
        "modified": "modified",
        "orchestrator": "orchestrator",
        "process": "process",
        "synthetics": "synthetics",
        "synthetics_private_locations": "synthetics-private-locations",
        "version": "version",
        "webhooks": "webhooks",
    }

    def __init__(
        self_,
        agents: Union[IPPrefixesAgents, UnsetType] = unset,
        api: Union[IPPrefixesAPI, UnsetType] = unset,
        apm: Union[IPPrefixesAPM, UnsetType] = unset,
        logs: Union[IPPrefixesLogs, UnsetType] = unset,
        modified: Union[str, UnsetType] = unset,
        orchestrator: Union[IPPrefixesOrchestrator, UnsetType] = unset,
        process: Union[IPPrefixesProcess, UnsetType] = unset,
        synthetics: Union[IPPrefixesSynthetics, UnsetType] = unset,
        synthetics_private_locations: Union[IPPrefixesSyntheticsPrivateLocations, UnsetType] = unset,
        version: Union[int, UnsetType] = unset,
        webhooks: Union[IPPrefixesWebhooks, UnsetType] = unset,
        **kwargs,
    ):
        """
        IP ranges.

        :param agents: Available prefix information for the Agent endpoints.
        :type agents: IPPrefixesAgents, optional

        :param api: Available prefix information for the API endpoints.
        :type api: IPPrefixesAPI, optional

        :param apm: Available prefix information for the APM endpoints.
        :type apm: IPPrefixesAPM, optional

        :param logs: Available prefix information for the Logs endpoints.
        :type logs: IPPrefixesLogs, optional

        :param modified: Date when last updated, in the form ``YYYY-MM-DD-hh-mm-ss``.
        :type modified: str, optional

        :param orchestrator: Available prefix information for the Orchestrator endpoints.
        :type orchestrator: IPPrefixesOrchestrator, optional

        :param process: Available prefix information for the Process endpoints.
        :type process: IPPrefixesProcess, optional

        :param synthetics: Available prefix information for the Synthetics endpoints.
        :type synthetics: IPPrefixesSynthetics, optional

        :param synthetics_private_locations: Available prefix information for the Synthetics Private Locations endpoints.
        :type synthetics_private_locations: IPPrefixesSyntheticsPrivateLocations, optional

        :param version: Version of the IP list.
        :type version: int, optional

        :param webhooks: Available prefix information for the Webhook endpoints.
        :type webhooks: IPPrefixesWebhooks, optional
        """
        if agents is not unset:
            kwargs["agents"] = agents
        if api is not unset:
            kwargs["api"] = api
        if apm is not unset:
            kwargs["apm"] = apm
        if logs is not unset:
            kwargs["logs"] = logs
        if modified is not unset:
            kwargs["modified"] = modified
        if orchestrator is not unset:
            kwargs["orchestrator"] = orchestrator
        if process is not unset:
            kwargs["process"] = process
        if synthetics is not unset:
            kwargs["synthetics"] = synthetics
        if synthetics_private_locations is not unset:
            kwargs["synthetics_private_locations"] = synthetics_private_locations
        if version is not unset:
            kwargs["version"] = version
        if webhooks is not unset:
            kwargs["webhooks"] = webhooks
        super().__init__(kwargs)
