# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, List, Union, TYPE_CHECKING

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
    from datadog_api_client.v1.model.agent_check import AgentCheck
    from datadog_api_client.v1.model.host_meta_install_method import HostMetaInstallMethod


class HostMeta(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.agent_check import AgentCheck
        from datadog_api_client.v1.model.host_meta_install_method import HostMetaInstallMethod

        return {
            "agent_checks": ([AgentCheck],),
            "agent_version": (str,),
            "cpu_cores": (int,),
            "fbsd_v": ([bool, date, datetime, dict, float, int, list, str, none_type],),
            "gohai": (str,),
            "install_method": (HostMetaInstallMethod,),
            "mac_v": ([bool, date, datetime, dict, float, int, list, str, none_type],),
            "machine": (str,),
            "nix_v": ([bool, date, datetime, dict, float, int, list, str, none_type],),
            "platform": (str,),
            "processor": (str,),
            "python_v": (str,),
            "socket_fqdn": (str,),
            "socket_hostname": (str,),
            "win_v": ([bool, date, datetime, dict, float, int, list, str, none_type],),
        }

    attribute_map = {
        "agent_checks": "agent_checks",
        "agent_version": "agent_version",
        "cpu_cores": "cpuCores",
        "fbsd_v": "fbsdV",
        "gohai": "gohai",
        "install_method": "install_method",
        "mac_v": "macV",
        "machine": "machine",
        "nix_v": "nixV",
        "platform": "platform",
        "processor": "processor",
        "python_v": "pythonV",
        "socket_fqdn": "socket-fqdn",
        "socket_hostname": "socket-hostname",
        "win_v": "winV",
    }

    def __init__(
        self_,
        agent_checks: Union[List[AgentCheck], UnsetType] = unset,
        agent_version: Union[str, UnsetType] = unset,
        cpu_cores: Union[int, UnsetType] = unset,
        fbsd_v: Union[List[Any], UnsetType] = unset,
        gohai: Union[str, UnsetType] = unset,
        install_method: Union[HostMetaInstallMethod, UnsetType] = unset,
        mac_v: Union[List[Any], UnsetType] = unset,
        machine: Union[str, UnsetType] = unset,
        nix_v: Union[List[Any], UnsetType] = unset,
        platform: Union[str, UnsetType] = unset,
        processor: Union[str, UnsetType] = unset,
        python_v: Union[str, UnsetType] = unset,
        socket_fqdn: Union[str, UnsetType] = unset,
        socket_hostname: Union[str, UnsetType] = unset,
        win_v: Union[List[Any], UnsetType] = unset,
        **kwargs,
    ):
        """
        Metadata associated with your host.

        :param agent_checks: A list of Agent checks running on the host.
        :type agent_checks: [AgentCheck], optional

        :param agent_version: The Datadog Agent version.
        :type agent_version: str, optional

        :param cpu_cores: The number of cores.
        :type cpu_cores: int, optional

        :param fbsd_v: An array of Mac versions.
        :type fbsd_v: [bool, date, datetime, dict, float, int, list, str, none_type], optional

        :param gohai: JSON string containing system information.
        :type gohai: str, optional

        :param install_method: Agent install method.
        :type install_method: HostMetaInstallMethod, optional

        :param mac_v: An array of Mac versions.
        :type mac_v: [bool, date, datetime, dict, float, int, list, str, none_type], optional

        :param machine: The machine architecture.
        :type machine: str, optional

        :param nix_v: Array of Unix versions.
        :type nix_v: [bool, date, datetime, dict, float, int, list, str, none_type], optional

        :param platform: The OS platform.
        :type platform: str, optional

        :param processor: The processor.
        :type processor: str, optional

        :param python_v: The Python version.
        :type python_v: str, optional

        :param socket_fqdn: The socket fqdn.
        :type socket_fqdn: str, optional

        :param socket_hostname: The socket hostname.
        :type socket_hostname: str, optional

        :param win_v: An array of Windows versions.
        :type win_v: [bool, date, datetime, dict, float, int, list, str, none_type], optional
        """
        if agent_checks is not unset:
            kwargs["agent_checks"] = agent_checks
        if agent_version is not unset:
            kwargs["agent_version"] = agent_version
        if cpu_cores is not unset:
            kwargs["cpu_cores"] = cpu_cores
        if fbsd_v is not unset:
            kwargs["fbsd_v"] = fbsd_v
        if gohai is not unset:
            kwargs["gohai"] = gohai
        if install_method is not unset:
            kwargs["install_method"] = install_method
        if mac_v is not unset:
            kwargs["mac_v"] = mac_v
        if machine is not unset:
            kwargs["machine"] = machine
        if nix_v is not unset:
            kwargs["nix_v"] = nix_v
        if platform is not unset:
            kwargs["platform"] = platform
        if processor is not unset:
            kwargs["processor"] = processor
        if python_v is not unset:
            kwargs["python_v"] = python_v
        if socket_fqdn is not unset:
            kwargs["socket_fqdn"] = socket_fqdn
        if socket_hostname is not unset:
            kwargs["socket_hostname"] = socket_hostname
        if win_v is not unset:
            kwargs["win_v"] = win_v
        super().__init__(kwargs)
