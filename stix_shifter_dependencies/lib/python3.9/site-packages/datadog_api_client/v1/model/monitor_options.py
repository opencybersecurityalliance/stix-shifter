# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Dict, List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.monitor_options_aggregation import MonitorOptionsAggregation
    from datadog_api_client.v1.model.monitor_device_id import MonitorDeviceID
    from datadog_api_client.v1.model.monitor_options_notification_presets import MonitorOptionsNotificationPresets
    from datadog_api_client.v1.model.on_missing_data_option import OnMissingDataOption
    from datadog_api_client.v1.model.monitor_renotify_status_type import MonitorRenotifyStatusType
    from datadog_api_client.v1.model.monitor_options_scheduling_options import MonitorOptionsSchedulingOptions
    from datadog_api_client.v1.model.monitor_threshold_window_options import MonitorThresholdWindowOptions
    from datadog_api_client.v1.model.monitor_thresholds import MonitorThresholds
    from datadog_api_client.v1.model.monitor_formula_and_function_query_definition import (
        MonitorFormulaAndFunctionQueryDefinition,
    )
    from datadog_api_client.v1.model.monitor_formula_and_function_event_query_definition import (
        MonitorFormulaAndFunctionEventQueryDefinition,
    )


class MonitorOptions(ModelNormal):
    validations = {
        "min_failure_duration": {
            "inclusive_maximum": 7200,
            "inclusive_minimum": 0,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.monitor_options_aggregation import MonitorOptionsAggregation
        from datadog_api_client.v1.model.monitor_device_id import MonitorDeviceID
        from datadog_api_client.v1.model.monitor_options_notification_presets import MonitorOptionsNotificationPresets
        from datadog_api_client.v1.model.on_missing_data_option import OnMissingDataOption
        from datadog_api_client.v1.model.monitor_renotify_status_type import MonitorRenotifyStatusType
        from datadog_api_client.v1.model.monitor_options_scheduling_options import MonitorOptionsSchedulingOptions
        from datadog_api_client.v1.model.monitor_threshold_window_options import MonitorThresholdWindowOptions
        from datadog_api_client.v1.model.monitor_thresholds import MonitorThresholds
        from datadog_api_client.v1.model.monitor_formula_and_function_query_definition import (
            MonitorFormulaAndFunctionQueryDefinition,
        )

        return {
            "aggregation": (MonitorOptionsAggregation,),
            "device_ids": ([MonitorDeviceID],),
            "enable_logs_sample": (bool,),
            "enable_samples": (bool,),
            "escalation_message": (str,),
            "evaluation_delay": (int, none_type),
            "group_retention_duration": (str,),
            "groupby_simple_monitor": (bool,),
            "include_tags": (bool,),
            "locked": (bool,),
            "min_failure_duration": (int, none_type),
            "min_location_failed": (int, none_type),
            "new_group_delay": (int, none_type),
            "new_host_delay": (int, none_type),
            "no_data_timeframe": (int, none_type),
            "notification_preset_name": (MonitorOptionsNotificationPresets,),
            "notify_audit": (bool,),
            "notify_by": ([str],),
            "notify_no_data": (bool,),
            "on_missing_data": (OnMissingDataOption,),
            "renotify_interval": (int, none_type),
            "renotify_occurrences": (int, none_type),
            "renotify_statuses": ([MonitorRenotifyStatusType], none_type),
            "require_full_window": (bool,),
            "scheduling_options": (MonitorOptionsSchedulingOptions,),
            "silenced": (
                {
                    str: (
                        int,
                        none_type,
                    )
                },
            ),
            "synthetics_check_id": (str, none_type),
            "threshold_windows": (MonitorThresholdWindowOptions,),
            "thresholds": (MonitorThresholds,),
            "timeout_h": (int, none_type),
            "variables": ([MonitorFormulaAndFunctionQueryDefinition],),
        }

    attribute_map = {
        "aggregation": "aggregation",
        "device_ids": "device_ids",
        "enable_logs_sample": "enable_logs_sample",
        "enable_samples": "enable_samples",
        "escalation_message": "escalation_message",
        "evaluation_delay": "evaluation_delay",
        "group_retention_duration": "group_retention_duration",
        "groupby_simple_monitor": "groupby_simple_monitor",
        "include_tags": "include_tags",
        "locked": "locked",
        "min_failure_duration": "min_failure_duration",
        "min_location_failed": "min_location_failed",
        "new_group_delay": "new_group_delay",
        "new_host_delay": "new_host_delay",
        "no_data_timeframe": "no_data_timeframe",
        "notification_preset_name": "notification_preset_name",
        "notify_audit": "notify_audit",
        "notify_by": "notify_by",
        "notify_no_data": "notify_no_data",
        "on_missing_data": "on_missing_data",
        "renotify_interval": "renotify_interval",
        "renotify_occurrences": "renotify_occurrences",
        "renotify_statuses": "renotify_statuses",
        "require_full_window": "require_full_window",
        "scheduling_options": "scheduling_options",
        "silenced": "silenced",
        "synthetics_check_id": "synthetics_check_id",
        "threshold_windows": "threshold_windows",
        "thresholds": "thresholds",
        "timeout_h": "timeout_h",
        "variables": "variables",
    }
    read_only_vars = {
        "aggregation",
        "device_ids",
    }

    def __init__(
        self_,
        aggregation: Union[MonitorOptionsAggregation, UnsetType] = unset,
        device_ids: Union[List[MonitorDeviceID], UnsetType] = unset,
        enable_logs_sample: Union[bool, UnsetType] = unset,
        enable_samples: Union[bool, UnsetType] = unset,
        escalation_message: Union[str, UnsetType] = unset,
        evaluation_delay: Union[int, none_type, UnsetType] = unset,
        group_retention_duration: Union[str, UnsetType] = unset,
        groupby_simple_monitor: Union[bool, UnsetType] = unset,
        include_tags: Union[bool, UnsetType] = unset,
        locked: Union[bool, UnsetType] = unset,
        min_failure_duration: Union[int, none_type, UnsetType] = unset,
        min_location_failed: Union[int, none_type, UnsetType] = unset,
        new_group_delay: Union[int, none_type, UnsetType] = unset,
        new_host_delay: Union[int, none_type, UnsetType] = unset,
        no_data_timeframe: Union[int, none_type, UnsetType] = unset,
        notification_preset_name: Union[MonitorOptionsNotificationPresets, UnsetType] = unset,
        notify_audit: Union[bool, UnsetType] = unset,
        notify_by: Union[List[str], UnsetType] = unset,
        notify_no_data: Union[bool, UnsetType] = unset,
        on_missing_data: Union[OnMissingDataOption, UnsetType] = unset,
        renotify_interval: Union[int, none_type, UnsetType] = unset,
        renotify_occurrences: Union[int, none_type, UnsetType] = unset,
        renotify_statuses: Union[List[MonitorRenotifyStatusType], none_type, UnsetType] = unset,
        require_full_window: Union[bool, UnsetType] = unset,
        scheduling_options: Union[MonitorOptionsSchedulingOptions, UnsetType] = unset,
        silenced: Union[Dict[str, Union[int, none_type]], UnsetType] = unset,
        synthetics_check_id: Union[str, none_type, UnsetType] = unset,
        threshold_windows: Union[MonitorThresholdWindowOptions, UnsetType] = unset,
        thresholds: Union[MonitorThresholds, UnsetType] = unset,
        timeout_h: Union[int, none_type, UnsetType] = unset,
        variables: Union[
            List[Union[MonitorFormulaAndFunctionQueryDefinition, MonitorFormulaAndFunctionEventQueryDefinition]],
            UnsetType,
        ] = unset,
        **kwargs,
    ):
        """
        List of options associated with your monitor.

        :param aggregation: Type of aggregation performed in the monitor query.
        :type aggregation: MonitorOptionsAggregation, optional

        :param device_ids: IDs of the device the Synthetics monitor is running on. **Deprecated**.
        :type device_ids: [MonitorDeviceID], optional

        :param enable_logs_sample: Whether or not to send a log sample when the log monitor triggers.
        :type enable_logs_sample: bool, optional

        :param enable_samples: Whether or not to send a list of samples when the monitor triggers. This is only used by CI Test and Pipeline monitors.
        :type enable_samples: bool, optional

        :param escalation_message: We recommend using the `is_renotify <https://docs.datadoghq.com/monitors/notify/?tab=is_alert#renotify>`_ ,
            block in the original message instead.
            A message to include with a re-notification. Supports the ``@username`` notification we allow elsewhere.
            Not applicable if ``renotify_interval`` is ``None``.
        :type escalation_message: str, optional

        :param evaluation_delay: Time (in seconds) to delay evaluation, as a non-negative integer. For example, if the value is set to ``300`` (5min),
            the timeframe is set to ``last_5m`` and the time is 7:00, the monitor evaluates data from 6:50 to 6:55.
            This is useful for AWS CloudWatch and other backfilled metrics to ensure the monitor always has data during evaluation.
        :type evaluation_delay: int, none_type, optional

        :param group_retention_duration: The time span after which groups with missing data are dropped from the monitor state.
            The minimum value is one hour, and the maximum value is 72 hours.
            Example values are: "60m", "1h", and "2d".
            This option is only available for APM Trace Analytics, Audit Trail, CI, Error Tracking, Event, Logs, and RUM monitors.
        :type group_retention_duration: str, optional

        :param groupby_simple_monitor: Whether the log alert monitor triggers a single alert or multiple alerts when any group breaches a threshold.
        :type groupby_simple_monitor: bool, optional

        :param include_tags: A Boolean indicating whether notifications from this monitor automatically inserts its triggering tags into the title.

            **Examples**

            * If ``True`` , ``[Triggered on {host:h1}] Monitor Title``
            * If ``False`` , ``[Triggered] Monitor Title``
        :type include_tags: bool, optional

        :param locked: Whether or not the monitor is locked (only editable by creator and admins). Use ``restricted_roles`` instead. **Deprecated**.
        :type locked: bool, optional

        :param min_failure_duration: How long the test should be in failure before alerting (integer, number of seconds, max 7200).
        :type min_failure_duration: int, none_type, optional

        :param min_location_failed: The minimum number of locations in failure at the same time during
            at least one moment in the ``min_failure_duration`` period ( ``min_location_failed`` and ``min_failure_duration``
            are part of the advanced alerting rules - integer, >= 1).
        :type min_location_failed: int, none_type, optional

        :param new_group_delay: Time (in seconds) to skip evaluations for new groups.

            For example, this option can be used to skip evaluations for new hosts while they initialize.

            Must be a non negative integer.
        :type new_group_delay: int, none_type, optional

        :param new_host_delay: Time (in seconds) to allow a host to boot and applications
            to fully start before starting the evaluation of monitor results.
            Should be a non negative integer.

            Use new_group_delay instead. **Deprecated**.
        :type new_host_delay: int, none_type, optional

        :param no_data_timeframe: The number of minutes before a monitor notifies after data stops reporting.
            Datadog recommends at least 2x the monitor timeframe for query alerts or 2 minutes for service checks.
            If omitted, 2x the evaluation timeframe is used for query alerts, and 24 hours is used for service checks.
        :type no_data_timeframe: int, none_type, optional

        :param notification_preset_name: Toggles the display of additional content sent in the monitor notification.
        :type notification_preset_name: MonitorOptionsNotificationPresets, optional

        :param notify_audit: A Boolean indicating whether tagged users is notified on changes to this monitor.
        :type notify_audit: bool, optional

        :param notify_by: Controls what granularity a monitor alerts on. Only available for monitors with groupings.
            For instance, a monitor grouped by ``cluster`` , ``namespace`` , and ``pod`` can be configured to only notify on each
            new ``cluster`` violating the alert conditions by setting ``notify_by`` to ``["cluster"]``. Tags mentioned
            in ``notify_by`` must be a subset of the grouping tags in the query.
            For example, a query grouped by ``cluster`` and ``namespace`` cannot notify on ``region``.
            Setting ``notify_by`` to ``[*]`` configures the monitor to notify as a simple-alert.
        :type notify_by: [str], optional

        :param notify_no_data: A Boolean indicating whether this monitor notifies when data stops reporting.
        :type notify_no_data: bool, optional

        :param on_missing_data: Controls how groups or monitors are treated if an evaluation does not return any data points.
            The default option results in different behavior depending on the monitor query type.
            For monitors using Count queries, an empty monitor evaluation is treated as 0 and is compared to the threshold conditions.
            For monitors using any query type other than Count, for example Gauge, Measure, or Rate, the monitor shows the last known status.
            This option is only available for APM Trace Analytics, Audit Trail, CI, Error Tracking, Event, Logs, and RUM monitors.
        :type on_missing_data: OnMissingDataOption, optional

        :param renotify_interval: The number of minutes after the last notification before a monitor re-notifies on the current status.
            It only re-notifies if it’s not resolved.
        :type renotify_interval: int, none_type, optional

        :param renotify_occurrences: The number of times re-notification messages should be sent on the current status at the provided re-notification interval.
        :type renotify_occurrences: int, none_type, optional

        :param renotify_statuses: The types of monitor statuses for which re-notification messages are sent.
        :type renotify_statuses: [MonitorRenotifyStatusType], none_type, optional

        :param require_full_window: A Boolean indicating whether this monitor needs a full window of data before it’s evaluated.
            We highly recommend you set this to ``false`` for sparse metrics,
            otherwise some evaluations are skipped. Default is false.
        :type require_full_window: bool, optional

        :param scheduling_options: Configuration options for scheduling.
        :type scheduling_options: MonitorOptionsSchedulingOptions, optional

        :param silenced: Information about the downtime applied to the monitor. **Deprecated**.
        :type silenced: {str: (int, none_type,)}, optional

        :param synthetics_check_id: ID of the corresponding Synthetic check. **Deprecated**.
        :type synthetics_check_id: str, none_type, optional

        :param threshold_windows: Alerting time window options.
        :type threshold_windows: MonitorThresholdWindowOptions, optional

        :param thresholds: List of the different monitor threshold available.
        :type thresholds: MonitorThresholds, optional

        :param timeout_h: The number of hours of the monitor not reporting data before it automatically resolves from a triggered state. The minimum allowed value is 0 hours. The maximum allowed value is 24 hours.
        :type timeout_h: int, none_type, optional

        :param variables: List of requests that can be used in the monitor query. **This feature is currently in beta.**
        :type variables: [MonitorFormulaAndFunctionQueryDefinition], optional
        """
        if aggregation is not unset:
            kwargs["aggregation"] = aggregation
        if device_ids is not unset:
            kwargs["device_ids"] = device_ids
        if enable_logs_sample is not unset:
            kwargs["enable_logs_sample"] = enable_logs_sample
        if enable_samples is not unset:
            kwargs["enable_samples"] = enable_samples
        if escalation_message is not unset:
            kwargs["escalation_message"] = escalation_message
        if evaluation_delay is not unset:
            kwargs["evaluation_delay"] = evaluation_delay
        if group_retention_duration is not unset:
            kwargs["group_retention_duration"] = group_retention_duration
        if groupby_simple_monitor is not unset:
            kwargs["groupby_simple_monitor"] = groupby_simple_monitor
        if include_tags is not unset:
            kwargs["include_tags"] = include_tags
        if locked is not unset:
            kwargs["locked"] = locked
        if min_failure_duration is not unset:
            kwargs["min_failure_duration"] = min_failure_duration
        if min_location_failed is not unset:
            kwargs["min_location_failed"] = min_location_failed
        if new_group_delay is not unset:
            kwargs["new_group_delay"] = new_group_delay
        if new_host_delay is not unset:
            kwargs["new_host_delay"] = new_host_delay
        if no_data_timeframe is not unset:
            kwargs["no_data_timeframe"] = no_data_timeframe
        if notification_preset_name is not unset:
            kwargs["notification_preset_name"] = notification_preset_name
        if notify_audit is not unset:
            kwargs["notify_audit"] = notify_audit
        if notify_by is not unset:
            kwargs["notify_by"] = notify_by
        if notify_no_data is not unset:
            kwargs["notify_no_data"] = notify_no_data
        if on_missing_data is not unset:
            kwargs["on_missing_data"] = on_missing_data
        if renotify_interval is not unset:
            kwargs["renotify_interval"] = renotify_interval
        if renotify_occurrences is not unset:
            kwargs["renotify_occurrences"] = renotify_occurrences
        if renotify_statuses is not unset:
            kwargs["renotify_statuses"] = renotify_statuses
        if require_full_window is not unset:
            kwargs["require_full_window"] = require_full_window
        if scheduling_options is not unset:
            kwargs["scheduling_options"] = scheduling_options
        if silenced is not unset:
            kwargs["silenced"] = silenced
        if synthetics_check_id is not unset:
            kwargs["synthetics_check_id"] = synthetics_check_id
        if threshold_windows is not unset:
            kwargs["threshold_windows"] = threshold_windows
        if thresholds is not unset:
            kwargs["thresholds"] = thresholds
        if timeout_h is not unset:
            kwargs["timeout_h"] = timeout_h
        if variables is not unset:
            kwargs["variables"] = variables
        super().__init__(kwargs)
