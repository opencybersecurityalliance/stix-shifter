# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Dict, List, Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class AWSAccount(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "access_key_id": (str,),
            "account_id": (str,),
            "account_specific_namespace_rules": ({str: (bool,)},),
            "cspm_resource_collection_enabled": (bool,),
            "excluded_regions": ([str],),
            "filter_tags": ([str],),
            "host_tags": ([str],),
            "metrics_collection_enabled": (bool,),
            "resource_collection_enabled": (bool,),
            "role_name": (str,),
            "secret_access_key": (str,),
        }

    attribute_map = {
        "access_key_id": "access_key_id",
        "account_id": "account_id",
        "account_specific_namespace_rules": "account_specific_namespace_rules",
        "cspm_resource_collection_enabled": "cspm_resource_collection_enabled",
        "excluded_regions": "excluded_regions",
        "filter_tags": "filter_tags",
        "host_tags": "host_tags",
        "metrics_collection_enabled": "metrics_collection_enabled",
        "resource_collection_enabled": "resource_collection_enabled",
        "role_name": "role_name",
        "secret_access_key": "secret_access_key",
    }

    def __init__(
        self_,
        access_key_id: Union[str, UnsetType] = unset,
        account_id: Union[str, UnsetType] = unset,
        account_specific_namespace_rules: Union[Dict[str, bool], UnsetType] = unset,
        cspm_resource_collection_enabled: Union[bool, UnsetType] = unset,
        excluded_regions: Union[List[str], UnsetType] = unset,
        filter_tags: Union[List[str], UnsetType] = unset,
        host_tags: Union[List[str], UnsetType] = unset,
        metrics_collection_enabled: Union[bool, UnsetType] = unset,
        resource_collection_enabled: Union[bool, UnsetType] = unset,
        role_name: Union[str, UnsetType] = unset,
        secret_access_key: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Returns the AWS account associated with this integration.

        :param access_key_id: Your AWS access key ID. Only required if your AWS account is a GovCloud or China account.
        :type access_key_id: str, optional

        :param account_id: Your AWS Account ID without dashes.
        :type account_id: str, optional

        :param account_specific_namespace_rules: An object, (in the form ``{"namespace1":true/false, "namespace2":true/false}`` ),
            that enables or disables metric collection for specific AWS namespaces for this
            AWS account only.
        :type account_specific_namespace_rules: {str: (bool,)}, optional

        :param cspm_resource_collection_enabled: Whether Datadog collects cloud security posture management resources from your AWS account. This includes additional resources not covered under the general ``resource_collection``.
        :type cspm_resource_collection_enabled: bool, optional

        :param excluded_regions: An array of AWS regions to exclude from metrics collection.
        :type excluded_regions: [str], optional

        :param filter_tags: The array of EC2 tags (in the form ``key:value`` ) defines a filter that Datadog uses when collecting metrics from EC2.
            Wildcards, such as ``?`` (for single characters) and ``*`` (for multiple characters) can also be used.
            Only hosts that match one of the defined tags
            will be imported into Datadog. The rest will be ignored.
            Host matching a given tag can also be excluded by adding ``!`` before the tag.
            For example, ``env:production,instance-type:c1.*,!region:us-east-1``
        :type filter_tags: [str], optional

        :param host_tags: Array of tags (in the form ``key:value`` ) to add to all hosts
            and metrics reporting through this integration.
        :type host_tags: [str], optional

        :param metrics_collection_enabled: Whether Datadog collects metrics for this AWS account.
        :type metrics_collection_enabled: bool, optional

        :param resource_collection_enabled: Whether Datadog collects a standard set of resources from your AWS account.
        :type resource_collection_enabled: bool, optional

        :param role_name: Your Datadog role delegation name.
        :type role_name: str, optional

        :param secret_access_key: Your AWS secret access key. Only required if your AWS account is a GovCloud or China account.
        :type secret_access_key: str, optional
        """
        if access_key_id is not unset:
            kwargs["access_key_id"] = access_key_id
        if account_id is not unset:
            kwargs["account_id"] = account_id
        if account_specific_namespace_rules is not unset:
            kwargs["account_specific_namespace_rules"] = account_specific_namespace_rules
        if cspm_resource_collection_enabled is not unset:
            kwargs["cspm_resource_collection_enabled"] = cspm_resource_collection_enabled
        if excluded_regions is not unset:
            kwargs["excluded_regions"] = excluded_regions
        if filter_tags is not unset:
            kwargs["filter_tags"] = filter_tags
        if host_tags is not unset:
            kwargs["host_tags"] = host_tags
        if metrics_collection_enabled is not unset:
            kwargs["metrics_collection_enabled"] = metrics_collection_enabled
        if resource_collection_enabled is not unset:
            kwargs["resource_collection_enabled"] = resource_collection_enabled
        if role_name is not unset:
            kwargs["role_name"] = role_name
        if secret_access_key is not unset:
            kwargs["secret_access_key"] = secret_access_key
        super().__init__(kwargs)
