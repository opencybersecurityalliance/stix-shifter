from stix_shifter_modules.aws_athena.entry_point import EntryPoint
from unittest.mock import patch
import json
import unittest
from stix_shifter.stix_transmission import stix_transmission
from tests.utils.async_utils import get_aws_mock_response
from botocore.exceptions import ClientError
from botocore.exceptions import ParamValidationError
import datetime
from dateutil.tz import tzlocal

CONFIGURATION = {
    "auth": {
        "aws_access_key_id": "abc",
        "aws_secret_access_key": "xyz"
    }
}

IAM_CONFIG = {
    "auth": {
        "aws_access_key_id": "abc",
        "aws_secret_access_key": "xyz",
        "aws_iam_role": "ABC"
    }
}

CONNECTION = {
    "region": "us-east-1",
    "s3_bucket_location": "s3://queryresults-athena-s3/",
    "vpcflow_database_name": "all",
    "vpcflow_table_name": "gd_logs",
    "guardduty_database_name": "gd_logs",
    "guardduty_table_name": "gd_logs"
}

class AWSMockJsonResponse:

    @staticmethod
    def assume_role(**kwargs):
        json_response = {'Credentials': {'AccessKeyId': 'abc', 'SecretAccessKey': 'xyz', 'SessionToken': '123abc'}}
        return json_response

    @staticmethod
    def list_work_groups(**kwargs):
        json_response = {
            'WorkGroups': [{
                'Name': 'AmazonAthenaPreviewFunctionality',
                'State': 'ENABLED',
                'Description': '',
                'CreationTime': datetime.datetime(2020, 7, 2, 18, 44, 21, 668000, tzinfo=tzlocal())
            }, {
                'Name': 'primary',
                'State': 'ENABLED',
                'Description': '',
                'CreationTime': datetime.datetime(2020, 6, 10, 16, 36, 33, 561000, tzinfo=tzlocal())
            }],
            'ResponseMetadata': {
                'RequestId': '241b172b-13d2-4497-90c6-743e4a6046ac',
                'HTTPStatusCode': 200,
                'HTTPHeaders': {
                    'content-type': 'application/x-amz-json-1.1',
                    'date': 'Wed, 30 Sep 2020 07:04:32 GMT',
                    'x-amzn-requestid': '241b172b-13d2-4497-90c6-743e4a6046ac',
                    'content-length': '413',
                    'connection': 'keep-alive'
                },
                'RetryAttempts': 0
            }
        }
        return json_response

    @staticmethod
    def start_query_execution(**kwargs):
        json_response = {
            'QueryExecutionId': '4214e100-9990-4161-9038-b431ec45661a',
            'ResponseMetadata': {
                'RequestId': '3139018f-7c6f-45ed-8462-26a3cd566472',
                'HTTPStatusCode': 200,
                'HTTPHeaders': {
                    'content-type': 'application/x-amz-json-1.1',
                    'date': 'Wed, 30 Sep 2020 07:14:03 GMT',
                    'x-amzn-requestid': '3139018f-7c6f-45ed-8462-26a3cd566472',
                    'content-length': '59',
                    'connection': 'keep-alive'
                },
                'RetryAttempts': 0
            }
        }
        return json_response

    @staticmethod
    def stop_query_execution(**kwargs):
        json_response = {"success": True}
        return json_response

    @staticmethod
    def delete_objects(**kwargs):
        json_response = {"success": True}
        return json_response

    @staticmethod
    def get_query_results(**kwargs):
        json_response = {
            'UpdateCount': 0,
            'ResultSet': {
                'Rows': [{
                    'Data': [{
                        'VarCharValue': 'version'
                    }, {
                        'VarCharValue': 'account'
                    }, {
                        'VarCharValue': 'interfaceid'
                    }, {
                        'VarCharValue': 'sourceaddress'
                    }, {
                        'VarCharValue': 'protocol'
                    }, {
                        'VarCharValue': 'action'
                    }
                    ]
                }, {
                    'Data': [{
                        'VarCharValue': '2'
                    }, {
                        'VarCharValue': '979326520502'
                    }, {
                        'VarCharValue': 'eni-0bb88d3d170cebfc0'
                    }, {
                        'VarCharValue': '99.79.68.141'
                    }, {
                        'VarCharValue': '6'
                    }, {
                        'VarCharValue': 'ACCEPT'
                    }]
                }],
            },
            'ResponseMetadata': {
                'RequestId': '396c4d92-ca40-4807-ae91-74b393a37aa7',
                'HTTPStatusCode': 200,
                'HTTPHeaders': {
                    'content-type': 'application/x-amz-json-1.1',
                    'date': 'Wed, 30 Sep 2020 08:02:32 GMT',
                    'x-amzn-requestid': '396c4d92-ca40-4807-ae91-74b393a37aa7',
                    'content-length': '7214',
                    'connection': 'keep-alive'
                },
                'RetryAttempts': 0
            }
        }
        return json_response

    @staticmethod
    def get_query_paginated_results(**kwargs):
        json_response = [{
            'Data': [{
                'VarCharValue': 'version'
            }, {
                'VarCharValue': 'account'
            }, {
                'VarCharValue': 'interfaceid'
            }, {
                'VarCharValue': 'sourceaddress'
            }, {
                'VarCharValue': 'protocol'
            }, {
                'VarCharValue': 'action'
            }
            ]
        }, {
            'Data': [{
                'VarCharValue': '2'
            }, {
                'VarCharValue': '979326520502'
            }, {
                'VarCharValue': 'eni-0bb88d3d170cebfc0'
            }, {
                'VarCharValue': '99.79.68.141'
            }, {
                'VarCharValue': '6'
            }, {
                'VarCharValue': 'ACCEPT'
            }]
        }]
        return json_response

    @staticmethod
    def get_query_execution(**kwargs):
        json_response = {
            'QueryExecution': {
                'QueryExecutionId': '3fdb8f84-6ad6-4f7c-8e9e-7bf3db87c274',
                'Query': 'SELECT * FROM logs_db.vpc_flow_logs limit 1',
                'StatementType': 'DML',
                'ResultConfiguration': {
                    'OutputLocation': 's3://queryresults-athena-s3/3fdb8f84-6ad6-4f7c-8e9e-7bf3db87c274.csv'
                },
                'QueryExecutionContext': {},
                'Status': {
                    'State': 'SUCCEEDED',
                    'SubmissionDateTime': datetime.datetime(2020, 9, 30, 13, 31, 28, 856000, tzinfo=tzlocal()),
                    'CompletionDateTime': datetime.datetime(2020, 9, 30, 13, 31, 31, 313000, tzinfo=tzlocal())
                },
                'Statistics': {
                    'EngineExecutionTimeInMillis': 2280,
                    'DataScannedInBytes': 1493800,
                    'TotalExecutionTimeInMillis': 2457,
                    'QueryQueueTimeInMillis': 117,
                    'QueryPlanningTimeInMillis': 1819,
                    'ServiceProcessingTimeInMillis': 60
                },
                'WorkGroup': 'primary'
            },
            'ResponseMetadata': {
                'RequestId': '870cfb1e-734f-40b2-bab0-cc44affa21d4',
                'HTTPStatusCode': 200,
                'HTTPHeaders': {
                    'content-type': 'application/x-amz-json-1.1',
                    'date': 'Wed, 30 Sep 2020 08:10:16 GMT',
                    'x-amzn-requestid': '870cfb1e-734f-40b2-bab0-cc44affa21d4',
                    'content-length': '1275',
                    'connection': 'keep-alive'
                },
                'RetryAttempts': 0
            }
        }
        return json_response

class MockStatusResponseRunning:

    @staticmethod
    def get_query_execution(**kwargs):
        json_response = {
            'QueryExecution': {
                'QueryExecutionId': '3fdb8f84-6ad6-4f7c-8e9e-7bf3db87c274',
                'Query': 'SELECT * FROM logs_db.vpc_flow_logs limit 1',
                'StatementType': 'DML',
                'ResultConfiguration': {
                    'OutputLocation': 's3://queryresults-athena-s3/3fdb8f84-6ad6-4f7c-8e9e-7bf3db87c274.csv'
                },
                'QueryExecutionContext': {},
                'Status': {
                    'State': 'RUNNING',
                    'SubmissionDateTime': datetime.datetime(2020, 9, 30, 13, 31, 28, 856000, tzinfo=tzlocal()),
                    'CompletionDateTime': datetime.datetime(2020, 9, 30, 13, 31, 31, 313000, tzinfo=tzlocal())
                },
                'Statistics': {
                    'EngineExecutionTimeInMillis': 2280,
                    'DataScannedInBytes': 1493800,
                    'TotalExecutionTimeInMillis': 2457,
                    'QueryQueueTimeInMillis': 117,
                    'QueryPlanningTimeInMillis': 1819,
                    'ServiceProcessingTimeInMillis': 60
                },
                'WorkGroup': 'primary'
            },
            'ResponseMetadata': {
                'RequestId': '870cfb1e-734f-40b2-bab0-cc44affa21d4',
                'HTTPStatusCode': 200,
                'HTTPHeaders': {
                    'content-type': 'application/x-amz-json-1.1',
                    'date': 'Wed, 30 Sep 2020 08:10:16 GMT',
                    'x-amzn-requestid': '870cfb1e-734f-40b2-bab0-cc44affa21d4',
                    'content-length': '1275',
                    'connection': 'keep-alive'
                },
                'RetryAttempts': 0
            }
        }
        return json_response


class AWSMockJsonResponseALB:

    @staticmethod
    def get_query_results(**kwargs):
        json_response = {
            'UpdateCount': 0,
            'ResultSet': {
                'Rows': [{
                    'Data': [{
                        'VarCharValue': 'type'
                    }, {
                        'VarCharValue': 'time'
                    }, {
                        'VarCharValue': 'elb'
                    }, {
                        'VarCharValue': 'useridentity'
                    }]
                }, {
                    'Data': [{
                        'VarCharValue': 'http'
                    }, {
                        'VarCharValue': '2020-06-15T07:04:18.737784Z'
                    }, {
                        'VarCharValue': 'app/apache-alb/d68fc3aeae65675d'
                    }, {
                        'VarCharValue': '{type=IAMUser, principalid=AIDA6IBDIZS3JEPRO2CBA, '
                                        'arn=arn:aws:iam::979326520502:user/murali_k@hcl.com, accountid=979326520502, '
                                        'invokedby=signin.amazonaws.com, accesskeyid=ASIA6IBDIZS3PHL7F75J, '
                                        'username=murali_k@hcl.com, sessioncontext={attributes={'
                                        'mfaauthenticated=false, creationdate=2019-10-15T06:12:34Z} '
                    }]
                }],
            },
            'ResponseMetadata': {
                'RequestId': '396c4d92-ca40-4807-ae91-74b393a37aa7',
                'HTTPStatusCode': 200,
                'HTTPHeaders': {
                    'content-type': 'application/x-amz-json-1.1',
                    'date': 'Wed, 30 Sep 2020 08:02:32 GMT',
                    'x-amzn-requestid': '396c4d92-ca40-4807-ae91-74b393a37aa7',
                    'content-length': '7214',
                    'connection': 'keep-alive'
                },
                'RetryAttempts': 0
            }
        }
        return json_response

    @staticmethod
    def get_query_execution(**kwargs):
        json_response = {
            'QueryExecution': {
                'QueryExecutionId': '3fdb8f84-6ad6-4f7c-8e9e-7bf3db87c274',
                'Query': 'SELECT * FROM logs_db.vpc_flow_logs limit 1',
                'StatementType': 'DML',
                'ResultConfiguration': {
                    'OutputLocation': 's3://queryresults-athena-s3/3fdb8f84-6ad6-4f7c-8e9e-7bf3db87c274.csv'
                }
            },
            'ResponseMetadata': {
                'RequestId': '870cfb1e-734f-40b2-bab0-cc44affa21d4',
                'HTTPStatusCode': 200,
                'HTTPHeaders': {
                    'content-type': 'application/x-amz-json-1.1',
                    'date': 'Wed, 30 Sep 2020 08:10:16 GMT',
                    'x-amzn-requestid': '870cfb1e-734f-40b2-bab0-cc44affa21d4',
                    'content-length': '1275',
                    'connection': 'keep-alive'
                },
                'RetryAttempts': 0
            }
        }
        return json_response

    @staticmethod
    def delete_objects(**kwargs):
        json_response = {"success": True}
        return json_response

    @staticmethod
    def get_paginator(method='get_query_results'):
        paginator_obj = AWSAthenaPaginateALB()
        return paginator_obj


class AWSAthenaPaginateALB(AWSMockJsonResponseALB):
    def paginate(self, **kwargs):
        return [self.get_query_results()]


class MockExceptionResponse:
    """
    Summary Json response handler
        """

    @staticmethod
    def list_work_groups():
        response = {'Error': {'Code': 'invalid_parameter', 'Message': 'Missing the parameters.'}}
        return ClientError(response, 'test1')

    @staticmethod
    def start_query_execution(**kwargs):
        response = {'Error': {'Code': 'authentication_fail', 'Message': 'Unable to access the data'}}
        return ClientError(response, 'test2')

    @staticmethod
    def get_query_execution(**kwargs):
        response = {'Error': {'Code': 'invalid_parameter', 'Message': 'Unable to access the data'}}
        return ParamValidationError(response=response, report='invalid_parameter')

    @staticmethod
    def get_query_results(**kwargs):
        response = """{
                                     "error" : {
                                         "code" : "mapping_error",
                                         "message":"Data is invalid."},
                                         "status": AWSATHENA.UNKNOWN
                                     }"""
        return json.loads(response)

    @staticmethod
    def stop_query_execution(**kwargs):
        response = {'Error': {'Code': 'authentication_fail', 'Message': 'Unable to access the data'}}
        return ClientError(response, 'test4')


class TestAWSConnection(unittest.TestCase):
    @staticmethod
    def test_is_async():
        entry_point = EntryPoint()
        check_async = entry_point.is_async()
        assert check_async

    @staticmethod
    @patch('stix_shifter_modules.aws_athena.stix_transmission.boto3_client.BOTO3Client.makeRequest')
    def test_create_query_connection(mock_start_query):
        mock_start_query.return_value = get_aws_mock_response(AWSMockJsonResponse.start_query_execution(**{}))
        
        query = """{"vpcflow": "endtime >= 1588310653 AND starttime BETWEEN 1588322590 AND 1604054590"}"""
        transmission = stix_transmission.StixTransmission('aws_athena', CONNECTION, CONFIGURATION)
        query_response = transmission.query(query)

        assert query_response is not None
        assert 'success' in query_response
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == "4214e100-9990-4161-9038-b431ec45661a:vpcflow"

    @staticmethod
    @patch('stix_shifter_modules.aws_athena.stix_transmission.boto3_client.BOTO3Client.makeRequest')
    def test_create_query_exception(mock_start_query):
        mock_start_query.side_effect = MockExceptionResponse.start_query_execution()
        query = """{"vpcflow": "endtime >= 1588310653 AND starttime BETWEEN 1588322590 AND 1604054590"}"""
        transmission = stix_transmission.StixTransmission('aws_athena', CONNECTION, CONFIGURATION)
        query_response = transmission.query(query)

        assert query_response is not None
        assert 'success' in query_response
        assert query_response['success'] is False
        assert 'error' in query_response
        assert query_response['code'] == "authentication_fail"

    @staticmethod
    @patch('stix_shifter_modules.aws_athena.stix_transmission.boto3_client.BOTO3Client.makeRequest')
    def test_iam_create_query_connection(mock_start_query):
        mock_start_query.return_value = get_aws_mock_response(AWSMockJsonResponse.start_query_execution(**{}))
        query = """{
            "vpcflow": "(CAST(destinationport AS varchar) IN ('38422', '38420') AND starttime BETWEEN 1603975773 AND \
            1603976073 LIMIT 100) UNION (CAST(destinationport AS varchar) = '32791' AND starttime BETWEEN 1603975773 \
            AND 1603976073 LIMIT 10)"
            }"""
        transmission = stix_transmission.StixTransmission('aws_athena', CONNECTION, IAM_CONFIG)
        query_response = transmission.query(query)

        assert query_response is not None
        assert 'success' in query_response
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == "4214e100-9990-4161-9038-b431ec45661a:vpcflow"

    @staticmethod
    @patch('stix_shifter_modules.aws_athena.stix_transmission.boto3_client.BOTO3Client.makeRequest')
    def test_create_results_exception(mock_create_results):
        mock_create_results.return_value = MockExceptionResponse()
        search_id = 123
        offset = 0
        length = 10
        transmission = stix_transmission.StixTransmission('aws_athena', CONNECTION, CONFIGURATION)
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] is False
        assert 'error' in results_response

    @staticmethod
    @patch('stix_shifter_modules.aws_athena.stix_transmission.boto3_client.BOTO3Client.makeRequest')
    def test_create_results_connection(mock_results):
        mock_results.side_effect = [
            get_aws_mock_response(AWSMockJsonResponse.get_query_results(**{})),
            get_aws_mock_response(AWSMockJsonResponse.get_query_execution(**{})),
            get_aws_mock_response(AWSMockJsonResponse.delete_objects(**{})),
        ]
        search_id = "0c8ed381-f1c8-406d-a293-406b64607870:vpcflow"
        offset = 0
        length = 2
        transmission = stix_transmission.StixTransmission('aws_athena', CONNECTION, CONFIGURATION)
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] is True
        assert 'data' in results_response
        assert results_response['data'] is not None

    @staticmethod
    @patch('stix_shifter_modules.aws_athena.stix_transmission.boto3_client.BOTO3Client.makeRequest')
    def test_delete_query_connection(mock_delete_query):
        mock_delete_query.return_value = get_aws_mock_response(AWSMockJsonResponse.stop_query_execution(**{}))
        search_id = "0c8ed381-f1c8-406d-a293-406b64607870"
        transmission = stix_transmission.StixTransmission('aws_athena', CONNECTION, CONFIGURATION)
        delete_response = transmission.delete(search_id)

        assert delete_response is not None
        assert 'success' in delete_response
        assert delete_response['success'] is True

    @staticmethod
    @patch('stix_shifter_modules.aws_athena.stix_transmission.boto3_client.BOTO3Client.makeRequest')
    def test_delete_query_exception(mock_create_status):
        response = {'Error': {'Code': 'authentication_fail', 'Message': 'Unable to access the data'}}
        mock_create_status.side_effect = ClientError(response, 'test4')
        search_id = '0c8ed381-f1c8-406d-a293-406b64604323:vpcflow'
        transmission = stix_transmission.StixTransmission('aws_athena', CONNECTION, CONFIGURATION)
        status_response = transmission.delete(search_id)

        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is False
        assert 'error' in status_response

    @staticmethod
    @patch('stix_shifter_modules.aws_athena.stix_transmission.boto3_client.BOTO3Client.makeRequest')
    def test_create_status_connection(mock_create_status):
        mock_create_status.return_value = get_aws_mock_response(AWSMockJsonResponse.get_query_execution(**{}))
        search_id = "0c8ed381-f1c8-406d-a293-406b64607870"
        transmission = stix_transmission.StixTransmission('aws_athena', CONNECTION, CONFIGURATION)
        status_response = transmission.status(search_id)

        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True
        assert 'status' in status_response
        assert status_response['status'] == 'COMPLETED'

    @staticmethod
    @patch('stix_shifter_modules.aws_athena.stix_transmission.boto3_client.BOTO3Client.makeRequest')
    def test_create_status_running(mock_create_status):
        mock_create_status.return_value = get_aws_mock_response(MockStatusResponseRunning.get_query_execution(**{}))
        search_id = "0c8ed381-f1c8-406d-a293-406b64607870"
        transmission = stix_transmission.StixTransmission('aws_athena', CONNECTION, CONFIGURATION)
        status_response = transmission.status(search_id)

        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True
        assert 'status' in status_response
        assert status_response['status'] == 'RUNNING'

    @staticmethod
    @patch('stix_shifter_modules.aws_athena.stix_transmission.boto3_client.BOTO3Client.makeRequest')
    def test_create_status_exception(mock_create_status):
        mock_create_status.side_effect = MockExceptionResponse.get_query_execution(**{})
        search_id = "xyz"
        transmission = stix_transmission.StixTransmission('aws_athena', CONNECTION, CONFIGURATION)
        status_response = transmission.status(search_id)

        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is False
        assert 'error' in status_response
        assert status_response['code'] == 'invalid_parameter'

    @staticmethod
    @patch('stix_shifter_modules.aws_athena.stix_transmission.boto3_client.BOTO3Client.makeRequest')
    def test_ping_connection(mock_create_status):
        mock_create_status.return_value = get_aws_mock_response(AWSMockJsonResponse.list_work_groups(**{}))
        transmission = stix_transmission.StixTransmission('aws_athena', CONNECTION, CONFIGURATION)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert 'success' in ping_response
        assert ping_response['success'] is True

    @staticmethod
    @patch('stix_shifter_modules.aws_athena.stix_transmission.boto3_client.BOTO3Client.makeRequest')
    def test_ping_exception(mock_create_status):
        mock_create_status.side_effect = MockExceptionResponse.list_work_groups()
        transmission = stix_transmission.StixTransmission('aws_athena', CONNECTION, CONFIGURATION)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert 'success' in ping_response
        assert ping_response['success'] is False
        assert 'error' in ping_response
        assert ping_response['code'] == 'authentication_fail'
