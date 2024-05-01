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


class MonthlyUsageAttributionValues(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "api_percentage": (float,),
            "api_usage": (float,),
            "apm_fargate_percentage": (float,),
            "apm_fargate_usage": (float,),
            "apm_host_percentage": (float,),
            "apm_host_usage": (float,),
            "appsec_fargate_percentage": (float,),
            "appsec_fargate_usage": (float,),
            "appsec_percentage": (float,),
            "appsec_usage": (float,),
            "browser_percentage": (float,),
            "browser_usage": (float,),
            "container_excl_agent_percentage": (float,),
            "container_excl_agent_usage": (float,),
            "container_percentage": (float,),
            "container_usage": (float,),
            "cspm_containers_percentage": (float,),
            "cspm_containers_usage": (float,),
            "cspm_hosts_percentage": (float,),
            "cspm_hosts_usage": (float,),
            "custom_ingested_timeseries_percentage": (float,),
            "custom_ingested_timeseries_usage": (float,),
            "custom_timeseries_percentage": (float,),
            "custom_timeseries_usage": (float,),
            "cws_containers_percentage": (float,),
            "cws_containers_usage": (float,),
            "cws_hosts_percentage": (float,),
            "cws_hosts_usage": (float,),
            "dbm_hosts_percentage": (float,),
            "dbm_hosts_usage": (float,),
            "dbm_queries_percentage": (float,),
            "dbm_queries_usage": (float,),
            "estimated_indexed_logs_percentage": (float,),
            "estimated_indexed_logs_usage": (float,),
            "estimated_indexed_spans_percentage": (float,),
            "estimated_indexed_spans_usage": (float,),
            "estimated_ingested_logs_percentage": (float,),
            "estimated_ingested_logs_usage": (float,),
            "estimated_ingested_spans_percentage": (float,),
            "estimated_ingested_spans_usage": (float,),
            "estimated_rum_sessions_percentage": (float,),
            "estimated_rum_sessions_usage": (float,),
            "fargate_percentage": (float,),
            "fargate_usage": (float,),
            "functions_percentage": (float,),
            "functions_usage": (float,),
            "infra_host_percentage": (float,),
            "infra_host_usage": (float,),
            "invocations_percentage": (float,),
            "invocations_usage": (float,),
            "npm_host_percentage": (float,),
            "npm_host_usage": (float,),
            "profiled_container_percentage": (float,),
            "profiled_container_usage": (float,),
            "profiled_fargate_percentage": (float,),
            "profiled_fargate_usage": (float,),
            "profiled_host_percentage": (float,),
            "profiled_host_usage": (float,),
            "snmp_percentage": (float,),
            "snmp_usage": (float,),
            "universal_service_monitoring_percentage": (float,),
            "universal_service_monitoring_usage": (float,),
        }

    attribute_map = {
        "api_percentage": "api_percentage",
        "api_usage": "api_usage",
        "apm_fargate_percentage": "apm_fargate_percentage",
        "apm_fargate_usage": "apm_fargate_usage",
        "apm_host_percentage": "apm_host_percentage",
        "apm_host_usage": "apm_host_usage",
        "appsec_fargate_percentage": "appsec_fargate_percentage",
        "appsec_fargate_usage": "appsec_fargate_usage",
        "appsec_percentage": "appsec_percentage",
        "appsec_usage": "appsec_usage",
        "browser_percentage": "browser_percentage",
        "browser_usage": "browser_usage",
        "container_excl_agent_percentage": "container_excl_agent_percentage",
        "container_excl_agent_usage": "container_excl_agent_usage",
        "container_percentage": "container_percentage",
        "container_usage": "container_usage",
        "cspm_containers_percentage": "cspm_containers_percentage",
        "cspm_containers_usage": "cspm_containers_usage",
        "cspm_hosts_percentage": "cspm_hosts_percentage",
        "cspm_hosts_usage": "cspm_hosts_usage",
        "custom_ingested_timeseries_percentage": "custom_ingested_timeseries_percentage",
        "custom_ingested_timeseries_usage": "custom_ingested_timeseries_usage",
        "custom_timeseries_percentage": "custom_timeseries_percentage",
        "custom_timeseries_usage": "custom_timeseries_usage",
        "cws_containers_percentage": "cws_containers_percentage",
        "cws_containers_usage": "cws_containers_usage",
        "cws_hosts_percentage": "cws_hosts_percentage",
        "cws_hosts_usage": "cws_hosts_usage",
        "dbm_hosts_percentage": "dbm_hosts_percentage",
        "dbm_hosts_usage": "dbm_hosts_usage",
        "dbm_queries_percentage": "dbm_queries_percentage",
        "dbm_queries_usage": "dbm_queries_usage",
        "estimated_indexed_logs_percentage": "estimated_indexed_logs_percentage",
        "estimated_indexed_logs_usage": "estimated_indexed_logs_usage",
        "estimated_indexed_spans_percentage": "estimated_indexed_spans_percentage",
        "estimated_indexed_spans_usage": "estimated_indexed_spans_usage",
        "estimated_ingested_logs_percentage": "estimated_ingested_logs_percentage",
        "estimated_ingested_logs_usage": "estimated_ingested_logs_usage",
        "estimated_ingested_spans_percentage": "estimated_ingested_spans_percentage",
        "estimated_ingested_spans_usage": "estimated_ingested_spans_usage",
        "estimated_rum_sessions_percentage": "estimated_rum_sessions_percentage",
        "estimated_rum_sessions_usage": "estimated_rum_sessions_usage",
        "fargate_percentage": "fargate_percentage",
        "fargate_usage": "fargate_usage",
        "functions_percentage": "functions_percentage",
        "functions_usage": "functions_usage",
        "infra_host_percentage": "infra_host_percentage",
        "infra_host_usage": "infra_host_usage",
        "invocations_percentage": "invocations_percentage",
        "invocations_usage": "invocations_usage",
        "npm_host_percentage": "npm_host_percentage",
        "npm_host_usage": "npm_host_usage",
        "profiled_container_percentage": "profiled_container_percentage",
        "profiled_container_usage": "profiled_container_usage",
        "profiled_fargate_percentage": "profiled_fargate_percentage",
        "profiled_fargate_usage": "profiled_fargate_usage",
        "profiled_host_percentage": "profiled_host_percentage",
        "profiled_host_usage": "profiled_host_usage",
        "snmp_percentage": "snmp_percentage",
        "snmp_usage": "snmp_usage",
        "universal_service_monitoring_percentage": "universal_service_monitoring_percentage",
        "universal_service_monitoring_usage": "universal_service_monitoring_usage",
    }

    def __init__(
        self_,
        api_percentage: Union[float, UnsetType] = unset,
        api_usage: Union[float, UnsetType] = unset,
        apm_fargate_percentage: Union[float, UnsetType] = unset,
        apm_fargate_usage: Union[float, UnsetType] = unset,
        apm_host_percentage: Union[float, UnsetType] = unset,
        apm_host_usage: Union[float, UnsetType] = unset,
        appsec_fargate_percentage: Union[float, UnsetType] = unset,
        appsec_fargate_usage: Union[float, UnsetType] = unset,
        appsec_percentage: Union[float, UnsetType] = unset,
        appsec_usage: Union[float, UnsetType] = unset,
        browser_percentage: Union[float, UnsetType] = unset,
        browser_usage: Union[float, UnsetType] = unset,
        container_excl_agent_percentage: Union[float, UnsetType] = unset,
        container_excl_agent_usage: Union[float, UnsetType] = unset,
        container_percentage: Union[float, UnsetType] = unset,
        container_usage: Union[float, UnsetType] = unset,
        cspm_containers_percentage: Union[float, UnsetType] = unset,
        cspm_containers_usage: Union[float, UnsetType] = unset,
        cspm_hosts_percentage: Union[float, UnsetType] = unset,
        cspm_hosts_usage: Union[float, UnsetType] = unset,
        custom_ingested_timeseries_percentage: Union[float, UnsetType] = unset,
        custom_ingested_timeseries_usage: Union[float, UnsetType] = unset,
        custom_timeseries_percentage: Union[float, UnsetType] = unset,
        custom_timeseries_usage: Union[float, UnsetType] = unset,
        cws_containers_percentage: Union[float, UnsetType] = unset,
        cws_containers_usage: Union[float, UnsetType] = unset,
        cws_hosts_percentage: Union[float, UnsetType] = unset,
        cws_hosts_usage: Union[float, UnsetType] = unset,
        dbm_hosts_percentage: Union[float, UnsetType] = unset,
        dbm_hosts_usage: Union[float, UnsetType] = unset,
        dbm_queries_percentage: Union[float, UnsetType] = unset,
        dbm_queries_usage: Union[float, UnsetType] = unset,
        estimated_indexed_logs_percentage: Union[float, UnsetType] = unset,
        estimated_indexed_logs_usage: Union[float, UnsetType] = unset,
        estimated_indexed_spans_percentage: Union[float, UnsetType] = unset,
        estimated_indexed_spans_usage: Union[float, UnsetType] = unset,
        estimated_ingested_logs_percentage: Union[float, UnsetType] = unset,
        estimated_ingested_logs_usage: Union[float, UnsetType] = unset,
        estimated_ingested_spans_percentage: Union[float, UnsetType] = unset,
        estimated_ingested_spans_usage: Union[float, UnsetType] = unset,
        estimated_rum_sessions_percentage: Union[float, UnsetType] = unset,
        estimated_rum_sessions_usage: Union[float, UnsetType] = unset,
        fargate_percentage: Union[float, UnsetType] = unset,
        fargate_usage: Union[float, UnsetType] = unset,
        functions_percentage: Union[float, UnsetType] = unset,
        functions_usage: Union[float, UnsetType] = unset,
        infra_host_percentage: Union[float, UnsetType] = unset,
        infra_host_usage: Union[float, UnsetType] = unset,
        invocations_percentage: Union[float, UnsetType] = unset,
        invocations_usage: Union[float, UnsetType] = unset,
        npm_host_percentage: Union[float, UnsetType] = unset,
        npm_host_usage: Union[float, UnsetType] = unset,
        profiled_container_percentage: Union[float, UnsetType] = unset,
        profiled_container_usage: Union[float, UnsetType] = unset,
        profiled_fargate_percentage: Union[float, UnsetType] = unset,
        profiled_fargate_usage: Union[float, UnsetType] = unset,
        profiled_host_percentage: Union[float, UnsetType] = unset,
        profiled_host_usage: Union[float, UnsetType] = unset,
        snmp_percentage: Union[float, UnsetType] = unset,
        snmp_usage: Union[float, UnsetType] = unset,
        universal_service_monitoring_percentage: Union[float, UnsetType] = unset,
        universal_service_monitoring_usage: Union[float, UnsetType] = unset,
        **kwargs,
    ):
        """
        Fields in Usage Summary by tag(s).

        :param api_percentage: The percentage of synthetic API test usage by tag(s).
        :type api_percentage: float, optional

        :param api_usage: The synthetic API test usage by tag(s).
        :type api_usage: float, optional

        :param apm_fargate_percentage: The percentage of APM ECS Fargate task usage by tag(s).
        :type apm_fargate_percentage: float, optional

        :param apm_fargate_usage: The APM ECS Fargate task usage by tag(s).
        :type apm_fargate_usage: float, optional

        :param apm_host_percentage: The percentage of APM host usage by tag(s).
        :type apm_host_percentage: float, optional

        :param apm_host_usage: The APM host usage by tag(s).
        :type apm_host_usage: float, optional

        :param appsec_fargate_percentage: The percentage of Application Security Monitoring ECS Fargate task usage by tag(s).
        :type appsec_fargate_percentage: float, optional

        :param appsec_fargate_usage: The Application Security Monitoring ECS Fargate task usage by tag(s).
        :type appsec_fargate_usage: float, optional

        :param appsec_percentage: The percentage of Application Security Monitoring host usage by tag(s).
        :type appsec_percentage: float, optional

        :param appsec_usage: The Application Security Monitoring host usage by tag(s).
        :type appsec_usage: float, optional

        :param browser_percentage: The percentage of synthetic browser test usage by tag(s).
        :type browser_percentage: float, optional

        :param browser_usage: The synthetic browser test usage by tag(s).
        :type browser_usage: float, optional

        :param container_excl_agent_percentage: The percentage of container usage without the Datadog Agent by tag(s).
        :type container_excl_agent_percentage: float, optional

        :param container_excl_agent_usage: The container usage without the Datadog Agent by tag(s).
        :type container_excl_agent_usage: float, optional

        :param container_percentage: The percentage of container usage by tag(s).
        :type container_percentage: float, optional

        :param container_usage: The container usage by tag(s).
        :type container_usage: float, optional

        :param cspm_containers_percentage: The percentage of CSPM container usage by tag(s).
        :type cspm_containers_percentage: float, optional

        :param cspm_containers_usage: The CSPM container usage by tag(s).
        :type cspm_containers_usage: float, optional

        :param cspm_hosts_percentage: The percentage of CSPM host usage by by tag(s).
        :type cspm_hosts_percentage: float, optional

        :param cspm_hosts_usage: The CSPM host usage by tag(s).
        :type cspm_hosts_usage: float, optional

        :param custom_ingested_timeseries_percentage: The percentage of ingested custom metrics usage by tag(s).
        :type custom_ingested_timeseries_percentage: float, optional

        :param custom_ingested_timeseries_usage: The ingested custom metrics usage by tag(s).
        :type custom_ingested_timeseries_usage: float, optional

        :param custom_timeseries_percentage: The percentage of indexed custom metrics usage by tag(s).
        :type custom_timeseries_percentage: float, optional

        :param custom_timeseries_usage: The indexed custom metrics usage by tag(s).
        :type custom_timeseries_usage: float, optional

        :param cws_containers_percentage: The percentage of Cloud Workload Security container usage by tag(s).
        :type cws_containers_percentage: float, optional

        :param cws_containers_usage: The Cloud Workload Security container usage by tag(s).
        :type cws_containers_usage: float, optional

        :param cws_hosts_percentage: The percentage of Cloud Workload Security host usage by tag(s).
        :type cws_hosts_percentage: float, optional

        :param cws_hosts_usage: The Cloud Workload Security host usage by tag(s).
        :type cws_hosts_usage: float, optional

        :param dbm_hosts_percentage: The percentage of Database Monitoring host usage by tag(s).
        :type dbm_hosts_percentage: float, optional

        :param dbm_hosts_usage: The Database Monitoring host usage by tag(s).
        :type dbm_hosts_usage: float, optional

        :param dbm_queries_percentage: The percentage of Database Monitoring queries usage by tag(s).
        :type dbm_queries_percentage: float, optional

        :param dbm_queries_usage: The Database Monitoring queries usage by tag(s).
        :type dbm_queries_usage: float, optional

        :param estimated_indexed_logs_percentage: The percentage of estimated live indexed logs usage by tag(s).
        :type estimated_indexed_logs_percentage: float, optional

        :param estimated_indexed_logs_usage: The estimated live indexed logs usage by tag(s).
        :type estimated_indexed_logs_usage: float, optional

        :param estimated_indexed_spans_percentage: The percentage of estimated indexed spans usage by tag(s).
        :type estimated_indexed_spans_percentage: float, optional

        :param estimated_indexed_spans_usage: The estimated indexed spans usage by tag(s).
        :type estimated_indexed_spans_usage: float, optional

        :param estimated_ingested_logs_percentage: The percentage of estimated live ingested logs usage by tag(s).
        :type estimated_ingested_logs_percentage: float, optional

        :param estimated_ingested_logs_usage: The estimated live ingested logs usage by tag(s).
        :type estimated_ingested_logs_usage: float, optional

        :param estimated_ingested_spans_percentage: The percentage of estimated ingested spans usage by tag(s).
        :type estimated_ingested_spans_percentage: float, optional

        :param estimated_ingested_spans_usage: The estimated ingested spans usage by tag(s).
        :type estimated_ingested_spans_usage: float, optional

        :param estimated_rum_sessions_percentage: The percentage of estimated rum sessions usage by tag(s).
        :type estimated_rum_sessions_percentage: float, optional

        :param estimated_rum_sessions_usage: The estimated rum sessions usage by tag(s).
        :type estimated_rum_sessions_usage: float, optional

        :param fargate_percentage: The percentage of Fargate usage by tags.
        :type fargate_percentage: float, optional

        :param fargate_usage: The Fargate usage by tags.
        :type fargate_usage: float, optional

        :param functions_percentage: The percentage of Lambda function usage by tag(s).
        :type functions_percentage: float, optional

        :param functions_usage: The Lambda function usage by tag(s).
        :type functions_usage: float, optional

        :param infra_host_percentage: The percentage of infrastructure host usage by tag(s).
        :type infra_host_percentage: float, optional

        :param infra_host_usage: The infrastructure host usage by tag(s).
        :type infra_host_usage: float, optional

        :param invocations_percentage: The percentage of Lambda invocation usage by tag(s).
        :type invocations_percentage: float, optional

        :param invocations_usage: The Lambda invocation usage by tag(s).
        :type invocations_usage: float, optional

        :param npm_host_percentage: The percentage of network host usage by tag(s).
        :type npm_host_percentage: float, optional

        :param npm_host_usage: The network host usage by tag(s).
        :type npm_host_usage: float, optional

        :param profiled_container_percentage: The percentage of profiled container usage by tag(s).
        :type profiled_container_percentage: float, optional

        :param profiled_container_usage: The profiled container usage by tag(s).
        :type profiled_container_usage: float, optional

        :param profiled_fargate_percentage: The percentage of profiled Fargate task usage by tag(s).
        :type profiled_fargate_percentage: float, optional

        :param profiled_fargate_usage: The profiled Fargate task usage by tag(s).
        :type profiled_fargate_usage: float, optional

        :param profiled_host_percentage: The percentage of profiled hosts usage by tag(s).
        :type profiled_host_percentage: float, optional

        :param profiled_host_usage: The profiled hosts usage by tag(s).
        :type profiled_host_usage: float, optional

        :param snmp_percentage: The percentage of network device usage by tag(s).
        :type snmp_percentage: float, optional

        :param snmp_usage: The network device usage by tag(s).
        :type snmp_usage: float, optional

        :param universal_service_monitoring_percentage: The percentage of universal service monitoring usage by tag(s).
        :type universal_service_monitoring_percentage: float, optional

        :param universal_service_monitoring_usage: The universal service monitoring usage by tag(s).
        :type universal_service_monitoring_usage: float, optional
        """
        if api_percentage is not unset:
            kwargs["api_percentage"] = api_percentage
        if api_usage is not unset:
            kwargs["api_usage"] = api_usage
        if apm_fargate_percentage is not unset:
            kwargs["apm_fargate_percentage"] = apm_fargate_percentage
        if apm_fargate_usage is not unset:
            kwargs["apm_fargate_usage"] = apm_fargate_usage
        if apm_host_percentage is not unset:
            kwargs["apm_host_percentage"] = apm_host_percentage
        if apm_host_usage is not unset:
            kwargs["apm_host_usage"] = apm_host_usage
        if appsec_fargate_percentage is not unset:
            kwargs["appsec_fargate_percentage"] = appsec_fargate_percentage
        if appsec_fargate_usage is not unset:
            kwargs["appsec_fargate_usage"] = appsec_fargate_usage
        if appsec_percentage is not unset:
            kwargs["appsec_percentage"] = appsec_percentage
        if appsec_usage is not unset:
            kwargs["appsec_usage"] = appsec_usage
        if browser_percentage is not unset:
            kwargs["browser_percentage"] = browser_percentage
        if browser_usage is not unset:
            kwargs["browser_usage"] = browser_usage
        if container_excl_agent_percentage is not unset:
            kwargs["container_excl_agent_percentage"] = container_excl_agent_percentage
        if container_excl_agent_usage is not unset:
            kwargs["container_excl_agent_usage"] = container_excl_agent_usage
        if container_percentage is not unset:
            kwargs["container_percentage"] = container_percentage
        if container_usage is not unset:
            kwargs["container_usage"] = container_usage
        if cspm_containers_percentage is not unset:
            kwargs["cspm_containers_percentage"] = cspm_containers_percentage
        if cspm_containers_usage is not unset:
            kwargs["cspm_containers_usage"] = cspm_containers_usage
        if cspm_hosts_percentage is not unset:
            kwargs["cspm_hosts_percentage"] = cspm_hosts_percentage
        if cspm_hosts_usage is not unset:
            kwargs["cspm_hosts_usage"] = cspm_hosts_usage
        if custom_ingested_timeseries_percentage is not unset:
            kwargs["custom_ingested_timeseries_percentage"] = custom_ingested_timeseries_percentage
        if custom_ingested_timeseries_usage is not unset:
            kwargs["custom_ingested_timeseries_usage"] = custom_ingested_timeseries_usage
        if custom_timeseries_percentage is not unset:
            kwargs["custom_timeseries_percentage"] = custom_timeseries_percentage
        if custom_timeseries_usage is not unset:
            kwargs["custom_timeseries_usage"] = custom_timeseries_usage
        if cws_containers_percentage is not unset:
            kwargs["cws_containers_percentage"] = cws_containers_percentage
        if cws_containers_usage is not unset:
            kwargs["cws_containers_usage"] = cws_containers_usage
        if cws_hosts_percentage is not unset:
            kwargs["cws_hosts_percentage"] = cws_hosts_percentage
        if cws_hosts_usage is not unset:
            kwargs["cws_hosts_usage"] = cws_hosts_usage
        if dbm_hosts_percentage is not unset:
            kwargs["dbm_hosts_percentage"] = dbm_hosts_percentage
        if dbm_hosts_usage is not unset:
            kwargs["dbm_hosts_usage"] = dbm_hosts_usage
        if dbm_queries_percentage is not unset:
            kwargs["dbm_queries_percentage"] = dbm_queries_percentage
        if dbm_queries_usage is not unset:
            kwargs["dbm_queries_usage"] = dbm_queries_usage
        if estimated_indexed_logs_percentage is not unset:
            kwargs["estimated_indexed_logs_percentage"] = estimated_indexed_logs_percentage
        if estimated_indexed_logs_usage is not unset:
            kwargs["estimated_indexed_logs_usage"] = estimated_indexed_logs_usage
        if estimated_indexed_spans_percentage is not unset:
            kwargs["estimated_indexed_spans_percentage"] = estimated_indexed_spans_percentage
        if estimated_indexed_spans_usage is not unset:
            kwargs["estimated_indexed_spans_usage"] = estimated_indexed_spans_usage
        if estimated_ingested_logs_percentage is not unset:
            kwargs["estimated_ingested_logs_percentage"] = estimated_ingested_logs_percentage
        if estimated_ingested_logs_usage is not unset:
            kwargs["estimated_ingested_logs_usage"] = estimated_ingested_logs_usage
        if estimated_ingested_spans_percentage is not unset:
            kwargs["estimated_ingested_spans_percentage"] = estimated_ingested_spans_percentage
        if estimated_ingested_spans_usage is not unset:
            kwargs["estimated_ingested_spans_usage"] = estimated_ingested_spans_usage
        if estimated_rum_sessions_percentage is not unset:
            kwargs["estimated_rum_sessions_percentage"] = estimated_rum_sessions_percentage
        if estimated_rum_sessions_usage is not unset:
            kwargs["estimated_rum_sessions_usage"] = estimated_rum_sessions_usage
        if fargate_percentage is not unset:
            kwargs["fargate_percentage"] = fargate_percentage
        if fargate_usage is not unset:
            kwargs["fargate_usage"] = fargate_usage
        if functions_percentage is not unset:
            kwargs["functions_percentage"] = functions_percentage
        if functions_usage is not unset:
            kwargs["functions_usage"] = functions_usage
        if infra_host_percentage is not unset:
            kwargs["infra_host_percentage"] = infra_host_percentage
        if infra_host_usage is not unset:
            kwargs["infra_host_usage"] = infra_host_usage
        if invocations_percentage is not unset:
            kwargs["invocations_percentage"] = invocations_percentage
        if invocations_usage is not unset:
            kwargs["invocations_usage"] = invocations_usage
        if npm_host_percentage is not unset:
            kwargs["npm_host_percentage"] = npm_host_percentage
        if npm_host_usage is not unset:
            kwargs["npm_host_usage"] = npm_host_usage
        if profiled_container_percentage is not unset:
            kwargs["profiled_container_percentage"] = profiled_container_percentage
        if profiled_container_usage is not unset:
            kwargs["profiled_container_usage"] = profiled_container_usage
        if profiled_fargate_percentage is not unset:
            kwargs["profiled_fargate_percentage"] = profiled_fargate_percentage
        if profiled_fargate_usage is not unset:
            kwargs["profiled_fargate_usage"] = profiled_fargate_usage
        if profiled_host_percentage is not unset:
            kwargs["profiled_host_percentage"] = profiled_host_percentage
        if profiled_host_usage is not unset:
            kwargs["profiled_host_usage"] = profiled_host_usage
        if snmp_percentage is not unset:
            kwargs["snmp_percentage"] = snmp_percentage
        if snmp_usage is not unset:
            kwargs["snmp_usage"] = snmp_usage
        if universal_service_monitoring_percentage is not unset:
            kwargs["universal_service_monitoring_percentage"] = universal_service_monitoring_percentage
        if universal_service_monitoring_usage is not unset:
            kwargs["universal_service_monitoring_usage"] = universal_service_monitoring_usage
        super().__init__(kwargs)
