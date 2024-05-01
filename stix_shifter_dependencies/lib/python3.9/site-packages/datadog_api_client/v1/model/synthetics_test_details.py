# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.synthetics_test_config import SyntheticsTestConfig
    from datadog_api_client.v1.model.creator import Creator
    from datadog_api_client.v1.model.synthetics_test_options import SyntheticsTestOptions
    from datadog_api_client.v1.model.synthetics_test_pause_status import SyntheticsTestPauseStatus
    from datadog_api_client.v1.model.synthetics_step import SyntheticsStep
    from datadog_api_client.v1.model.synthetics_test_details_sub_type import SyntheticsTestDetailsSubType
    from datadog_api_client.v1.model.synthetics_test_details_type import SyntheticsTestDetailsType


class SyntheticsTestDetails(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_test_config import SyntheticsTestConfig
        from datadog_api_client.v1.model.creator import Creator
        from datadog_api_client.v1.model.synthetics_test_options import SyntheticsTestOptions
        from datadog_api_client.v1.model.synthetics_test_pause_status import SyntheticsTestPauseStatus
        from datadog_api_client.v1.model.synthetics_step import SyntheticsStep
        from datadog_api_client.v1.model.synthetics_test_details_sub_type import SyntheticsTestDetailsSubType
        from datadog_api_client.v1.model.synthetics_test_details_type import SyntheticsTestDetailsType

        return {
            "config": (SyntheticsTestConfig,),
            "creator": (Creator,),
            "locations": ([str],),
            "message": (str,),
            "monitor_id": (int,),
            "name": (str,),
            "options": (SyntheticsTestOptions,),
            "public_id": (str,),
            "status": (SyntheticsTestPauseStatus,),
            "steps": ([SyntheticsStep],),
            "subtype": (SyntheticsTestDetailsSubType,),
            "tags": ([str],),
            "type": (SyntheticsTestDetailsType,),
        }

    attribute_map = {
        "config": "config",
        "creator": "creator",
        "locations": "locations",
        "message": "message",
        "monitor_id": "monitor_id",
        "name": "name",
        "options": "options",
        "public_id": "public_id",
        "status": "status",
        "steps": "steps",
        "subtype": "subtype",
        "tags": "tags",
        "type": "type",
    }
    read_only_vars = {
        "creator",
        "monitor_id",
        "public_id",
    }

    def __init__(
        self_,
        config: Union[SyntheticsTestConfig, UnsetType] = unset,
        creator: Union[Creator, UnsetType] = unset,
        locations: Union[List[str], UnsetType] = unset,
        message: Union[str, UnsetType] = unset,
        monitor_id: Union[int, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        options: Union[SyntheticsTestOptions, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        status: Union[SyntheticsTestPauseStatus, UnsetType] = unset,
        steps: Union[List[SyntheticsStep], UnsetType] = unset,
        subtype: Union[SyntheticsTestDetailsSubType, UnsetType] = unset,
        tags: Union[List[str], UnsetType] = unset,
        type: Union[SyntheticsTestDetailsType, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object containing details about your Synthetic test.

        :param config: Configuration object for a Synthetic test.
        :type config: SyntheticsTestConfig, optional

        :param creator: Object describing the creator of the shared element.
        :type creator: Creator, optional

        :param locations: Array of locations used to run the test.
        :type locations: [str], optional

        :param message: Notification message associated with the test.
        :type message: str, optional

        :param monitor_id: The associated monitor ID.
        :type monitor_id: int, optional

        :param name: Name of the test.
        :type name: str, optional

        :param options: Object describing the extra options for a Synthetic test.
        :type options: SyntheticsTestOptions, optional

        :param public_id: The test public ID.
        :type public_id: str, optional

        :param status: Define whether you want to start ( ``live`` ) or pause ( ``paused`` ) a
            Synthetic test.
        :type status: SyntheticsTestPauseStatus, optional

        :param steps: For browser test, the steps of the test.
        :type steps: [SyntheticsStep], optional

        :param subtype: The subtype of the Synthetic API test, ``http`` , ``ssl`` , ``tcp`` ,
            ``dns`` , ``icmp`` , ``udp`` , ``websocket`` , ``grpc`` or ``multi``.
        :type subtype: SyntheticsTestDetailsSubType, optional

        :param tags: Array of tags attached to the test.
        :type tags: [str], optional

        :param type: Type of the Synthetic test, either ``api`` or ``browser``.
        :type type: SyntheticsTestDetailsType, optional
        """
        if config is not unset:
            kwargs["config"] = config
        if creator is not unset:
            kwargs["creator"] = creator
        if locations is not unset:
            kwargs["locations"] = locations
        if message is not unset:
            kwargs["message"] = message
        if monitor_id is not unset:
            kwargs["monitor_id"] = monitor_id
        if name is not unset:
            kwargs["name"] = name
        if options is not unset:
            kwargs["options"] = options
        if public_id is not unset:
            kwargs["public_id"] = public_id
        if status is not unset:
            kwargs["status"] = status
        if steps is not unset:
            kwargs["steps"] = steps
        if subtype is not unset:
            kwargs["subtype"] = subtype
        if tags is not unset:
            kwargs["tags"] = tags
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
