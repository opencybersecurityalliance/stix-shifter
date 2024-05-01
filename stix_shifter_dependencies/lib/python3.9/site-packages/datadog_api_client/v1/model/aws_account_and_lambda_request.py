# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


class AWSAccountAndLambdaRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "account_id": (str,),
            "lambda_arn": (str,),
        }

    attribute_map = {
        "account_id": "account_id",
        "lambda_arn": "lambda_arn",
    }

    def __init__(self_, account_id: str, lambda_arn: str, **kwargs):
        """
        AWS account ID and Lambda ARN.

        :param account_id: Your AWS Account ID without dashes.
        :type account_id: str

        :param lambda_arn: ARN of the Datadog Lambda created during the Datadog-Amazon Web services Log collection setup.
        :type lambda_arn: str
        """
        super().__init__(kwargs)

        self_.account_id = account_id
        self_.lambda_arn = lambda_arn
