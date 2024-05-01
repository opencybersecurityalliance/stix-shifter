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
    from datadog_api_client.v1.model.synthetics_api_test_config import SyntheticsAPITestConfig
    from datadog_api_client.v1.model.synthetics_test_options import SyntheticsTestOptions
    from datadog_api_client.v1.model.synthetics_test_pause_status import SyntheticsTestPauseStatus
    from datadog_api_client.v1.model.synthetics_test_details_sub_type import SyntheticsTestDetailsSubType
    from datadog_api_client.v1.model.synthetics_api_test_type import SyntheticsAPITestType


class SyntheticsAPITest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_api_test_config import SyntheticsAPITestConfig
        from datadog_api_client.v1.model.synthetics_test_options import SyntheticsTestOptions
        from datadog_api_client.v1.model.synthetics_test_pause_status import SyntheticsTestPauseStatus
        from datadog_api_client.v1.model.synthetics_test_details_sub_type import SyntheticsTestDetailsSubType
        from datadog_api_client.v1.model.synthetics_api_test_type import SyntheticsAPITestType

        return {
            "config": (SyntheticsAPITestConfig,),
            "locations": ([str],),
            "message": (str,),
            "monitor_id": (int,),
            "name": (str,),
            "options": (SyntheticsTestOptions,),
            "public_id": (str,),
            "status": (SyntheticsTestPauseStatus,),
            "subtype": (SyntheticsTestDetailsSubType,),
            "tags": ([str],),
            "type": (SyntheticsAPITestType,),
        }

    attribute_map = {
        "config": "config",
        "locations": "locations",
        "message": "message",
        "monitor_id": "monitor_id",
        "name": "name",
        "options": "options",
        "public_id": "public_id",
        "status": "status",
        "subtype": "subtype",
        "tags": "tags",
        "type": "type",
    }
    read_only_vars = {
        "monitor_id",
        "public_id",
    }

    def __init__(
        self_,
        config: SyntheticsAPITestConfig,
        locations: List[str],
        message: str,
        name: str,
        options: SyntheticsTestOptions,
        type: SyntheticsAPITestType,
        monitor_id: Union[int, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        status: Union[SyntheticsTestPauseStatus, UnsetType] = unset,
        subtype: Union[SyntheticsTestDetailsSubType, UnsetType] = unset,
        tags: Union[List[str], UnsetType] = unset,
        **kwargs,
    ):
        """
        Object containing details about a Synthetic API test.

        :param config: Configuration object for a Synthetic API test.
        :type config: SyntheticsAPITestConfig

        :param locations: Array of locations used to run the test.
        :type locations: [str]

        :param message: Notification message associated with the test.
        :type message: str

        :param monitor_id: The associated monitor ID.
        :type monitor_id: int, optional

        :param name: Name of the test.
        :type name: str

        :param options: Object describing the extra options for a Synthetic test.
        :type options: SyntheticsTestOptions

        :param public_id: The public ID for the test.
        :type public_id: str, optional

        :param status: Define whether you want to start ( ``live`` ) or pause ( ``paused`` ) a
            Synthetic test.
        :type status: SyntheticsTestPauseStatus, optional

        :param subtype: The subtype of the Synthetic API test, ``http`` , ``ssl`` , ``tcp`` ,
            ``dns`` , ``icmp`` , ``udp`` , ``websocket`` , ``grpc`` or ``multi``.
        :type subtype: SyntheticsTestDetailsSubType, optional

        :param tags: Array of tags attached to the test.
        :type tags: [str], optional

        :param type: Type of the Synthetic test, ``api``.
        :type type: SyntheticsAPITestType
        """
        if monitor_id is not unset:
            kwargs["monitor_id"] = monitor_id
        if public_id is not unset:
            kwargs["public_id"] = public_id
        if status is not unset:
            kwargs["status"] = status
        if subtype is not unset:
            kwargs["subtype"] = subtype
        if tags is not unset:
            kwargs["tags"] = tags
        super().__init__(kwargs)

        self_.config = config
        self_.locations = locations
        self_.message = message
        self_.name = name
        self_.options = options
        self_.type = type
