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
    from datadog_api_client.v2.model.security_monitoring_rule_new_value_options_forget_after import (
        SecurityMonitoringRuleNewValueOptionsForgetAfter,
    )
    from datadog_api_client.v2.model.security_monitoring_rule_new_value_options_learning_duration import (
        SecurityMonitoringRuleNewValueOptionsLearningDuration,
    )
    from datadog_api_client.v2.model.security_monitoring_rule_new_value_options_learning_method import (
        SecurityMonitoringRuleNewValueOptionsLearningMethod,
    )
    from datadog_api_client.v2.model.security_monitoring_rule_new_value_options_learning_threshold import (
        SecurityMonitoringRuleNewValueOptionsLearningThreshold,
    )


class SecurityMonitoringRuleNewValueOptions(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.security_monitoring_rule_new_value_options_forget_after import (
            SecurityMonitoringRuleNewValueOptionsForgetAfter,
        )
        from datadog_api_client.v2.model.security_monitoring_rule_new_value_options_learning_duration import (
            SecurityMonitoringRuleNewValueOptionsLearningDuration,
        )
        from datadog_api_client.v2.model.security_monitoring_rule_new_value_options_learning_method import (
            SecurityMonitoringRuleNewValueOptionsLearningMethod,
        )
        from datadog_api_client.v2.model.security_monitoring_rule_new_value_options_learning_threshold import (
            SecurityMonitoringRuleNewValueOptionsLearningThreshold,
        )

        return {
            "forget_after": (SecurityMonitoringRuleNewValueOptionsForgetAfter,),
            "learning_duration": (SecurityMonitoringRuleNewValueOptionsLearningDuration,),
            "learning_method": (SecurityMonitoringRuleNewValueOptionsLearningMethod,),
            "learning_threshold": (SecurityMonitoringRuleNewValueOptionsLearningThreshold,),
        }

    attribute_map = {
        "forget_after": "forgetAfter",
        "learning_duration": "learningDuration",
        "learning_method": "learningMethod",
        "learning_threshold": "learningThreshold",
    }

    def __init__(
        self_,
        forget_after: Union[SecurityMonitoringRuleNewValueOptionsForgetAfter, UnsetType] = unset,
        learning_duration: Union[SecurityMonitoringRuleNewValueOptionsLearningDuration, UnsetType] = unset,
        learning_method: Union[SecurityMonitoringRuleNewValueOptionsLearningMethod, UnsetType] = unset,
        learning_threshold: Union[SecurityMonitoringRuleNewValueOptionsLearningThreshold, UnsetType] = unset,
        **kwargs,
    ):
        """
        Options on new value rules.

        :param forget_after: The duration in days after which a learned value is forgotten.
        :type forget_after: SecurityMonitoringRuleNewValueOptionsForgetAfter, optional

        :param learning_duration: The duration in days during which values are learned, and after which signals will be generated for values that
            weren't learned. If set to 0, a signal will be generated for all new values after the first value is learned.
        :type learning_duration: SecurityMonitoringRuleNewValueOptionsLearningDuration, optional

        :param learning_method: The learning method used to determine when signals should be generated for values that weren't learned.
        :type learning_method: SecurityMonitoringRuleNewValueOptionsLearningMethod, optional

        :param learning_threshold: A number of occurrences after which signals will be generated for values that weren't learned.
        :type learning_threshold: SecurityMonitoringRuleNewValueOptionsLearningThreshold, optional
        """
        if forget_after is not unset:
            kwargs["forget_after"] = forget_after
        if learning_duration is not unset:
            kwargs["learning_duration"] = learning_duration
        if learning_method is not unset:
            kwargs["learning_method"] = learning_method
        if learning_threshold is not unset:
            kwargs["learning_threshold"] = learning_threshold
        super().__init__(kwargs)
