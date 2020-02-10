from stix_shifter.stix_transmission.src.modules.aws_cloud_watch_logs import aws_cloud_watch_logs_connector
from unittest.mock import patch
import json
import unittest
from stix_shifter.stix_transmission import stix_transmission
from botocore.exceptions import ClientError

CONFIG = {
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
    "options": {"region": "xyz"}
}


class AWSMockJsonResponse:
    def __init__(self):
        self.client = None

    @staticmethod
    def assume_role(**kwargs):
        json_response = {'Credentials': {'AccessKeyId': 'abc', 'SecretAccessKey': 'xyz', 'SessionToken': '123abc'}}
        return json_response

    @staticmethod
    def describe_log_groups(**kwargs):
        json_response = {
            "logGroups": [
                {
                    "arn": "arn:aws:logs:us-east-1:979326520502:log-group:/aws/events/guardduty:*",
                    "creationTime": 1571122789371,
                    "logGroupName": "/aws/events/guardduty",
                    "metricFilterCount": 0,
                    "storedBytes": 196184
                }]
        }
        return json_response

    @staticmethod
    def start_query(**kwargs):
        json_response = {"queryId": "0c8ed381-f1c8-406d-a293-406b64607870"}
        return json_response

    @staticmethod
    def stop_query(**kwargs):
        json_response = {"success": True}
        return json_response

    @staticmethod
    def get_query_results(**kwargs):
        json_response = {
            "results": [
                [
                    {
                        "field": "@timestamp",
                        "value": "2019-10-30 11:01:03.000"
                    },
                    {
                        "field": "srcAddr",
                        "value": "172.31.88.63"
                    },
                    {
                        "field": "dstAddr",
                        "value": "54.239.30.195"
                    },
                    {
                        "field": "srcPort",
                        "value": "41900"
                    },
                    {
                        "field": "dstPort",
                        "value": "443"
                    },
                    {
                        "field": "protocol",
                        "value": "6"
                    },
                    {
                        "field": "start",
                        "value": "1572433263"
                    },
                    {
                        "field": "end",
                        "value": "1572433309"
                    },
                    {
                        "field": "accountId",
                        "value": "979326520502"
                    },
                    {
                        "field": "interfaceId",
                        "value": "eni-02e70b8e842c70a2f"
                    },
                    {
                        "field": "bytes",
                        "value": "3646"
                    },
                    {
                        "field": "packets",
                        "value": "16"
                    },
                    {
                        "field": "@ptr",
                        "value":
                            "CloKIQodOTc5MzI2NTIwNTAyOlVTRWFzdDFfRmxvd0xvZ3MQBBI1GhgCBdlAMFMAAAAAg2XOMQAF25"
                            "bRkAAAADIgASiwj8Li4S0wmPPN4uEtOChAsi1IrihQrSEQHhgB"
                    }
                ]
            ],
            "statistics": {
                "bytesScanned": 7.1185346E7,
                "recordsMatched": 254533.0,
                "recordsScanned": 492595.0
            },
            "status": "Complete"
        }
        return json_response


class MockStatusResponse:
    @staticmethod
    def get_query_results(**kwargs):
        json_response = {
            "results": [
                [
                    {
                        "field": "@timestamp",
                        "value": "2019-10-30 11:01:03.000"
                    },
                    {
                        "field": "srcAddr",
                        "value": "172.31.88.63"
                    },
                    {
                        "field": "dstAddr",
                        "value": "54.239.30.195"
                    },
                    {
                        "field": "srcPort",
                        "value": "41900"
                    },
                    {
                        "field": "dstPort",
                        "value": "443"
                    },
                    {
                        "field": "protocol",
                        "value": "6"
                    },
                    {
                        "field": "start",
                        "value": "1572433263"
                    },
                    {
                        "field": "end",
                        "value": "1572433309"
                    },
                    {
                        "field": "accountId",
                        "value": "979326520502"
                    },
                    {
                        "field": "interfaceId",
                        "value": "eni-02e70b8e842c70a2f"
                    },
                    {
                        "field": "bytes",
                        "value": "3646"
                    },
                    {
                        "field": "packets",
                        "value": "16"
                    },
                    {
                        "field": "@ptr",
                        "value":
                            "CloKIQodOTc5MzI2NTIwNTAyOlVTRWFzdDFfRmxvd0xvZ3MQBBI1GhgCBdlAMFMAAAAAg2XOMQAF25"
                            "bRkAAAADIgASiwj8Li4S0wmPPN4uEtOChAsi1IrihQrSEQHhgB"
                    }
                ]
            ],
            "statistics": {
                "bytesScanned": 7.1185346E7,
                "recordsMatched": 254533.0,
                "recordsScanned": 492595.0
            },
            "status": "Running"
        }
        return json_response


class MockExceptionResponse:
    """
    Summary Json response handler
        """

    def __init__(self):
        self.client = None

    @staticmethod
    def describe_log_groups():
        response = {'Error': {'Code': 'invalid_parameter', 'Message': 'Missing the parameters.'}}
        raise ClientError(response, 'test1')

    @staticmethod
    def get_query_results(**kwargs):
        response = """{
                                     "error" : {
                                         "code" : "mapping_error",
                                         "message":"Data is invalid."},
                                        "status": AWSCWLOGS.UNKNOWN
                                     }"""
        return json.loads(response)

    @staticmethod
    def stop_query(**kwargs):
        response = {'Error': {'Code': 'authentication_fail', 'Message': 'Unable to access the data'}}
        raise ClientError(response, 'test2')


class TestAWSConnection(unittest.TestCase):
    @staticmethod
    def test_is_async():
        module = aws_cloud_watch_logs_connector

        check_async = module.Connector(CONNECTION, CONFIG).is_async
        assert check_async

    @staticmethod
    @patch(
        'stix_shifter.stix_transmission.src.modules.aws_cloud_watch_logs.aws_cloud_watch_logs_boto3_client.boto3'
        '.client')
    def test_ping(mock_ping):
        mock_ping.return_value = AWSMockJsonResponse()
        transmission = stix_transmission.StixTransmission('aws_cloud_watch_logs', CONNECTION, CONFIG)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert 'success' in ping_response
        assert ping_response['success']

    @staticmethod
    @patch(
        'stix_shifter.stix_transmission.src.modules.aws_cloud_watch_logs.aws_cloud_watch_logs_boto3_client.boto3'
        '.client')
    def test_ping_exception(mock_ping_value):
        mock_ping_value.return_value = MockExceptionResponse()
        transmission = stix_transmission.StixTransmission('aws_cloud_watch_logs', CONNECTION, CONFIG)
        ping_response = transmission.ping()
        assert ping_response is not None
        assert 'success' in ping_response
        assert ping_response['success'] is False
        assert 'error' in ping_response

    @staticmethod
    @patch(
        'stix_shifter.stix_transmission.src.modules.aws_cloud_watch_logs.aws_cloud_watch_logs_boto3_client.boto3'
        '.client')
    def test_create_query_exception(mock_create_query):
        mock_create_query.return_value = Exception("Invalid Query")
        query = 'sample query'
        transmission = stix_transmission.StixTransmission('aws_cloud_watch_logs', CONNECTION, CONFIG)
        query_response = transmission.query(query)
        assert query_response is not None
        assert 'success' in query_response
        assert query_response['success'] is False
        assert 'error' in query_response
        assert query_response['code'] == "invalid_query"

    @staticmethod
    @patch(
        'stix_shifter.stix_transmission.src.modules.aws_cloud_watch_logs.aws_cloud_watch_logs_boto3_client.boto3'
        '.client')
    def test_create_query_connection(mock_create_query):
        mock_create_query.return_value = AWSMockJsonResponse()
        query = "{\"logType\": \"vpcflow\", \"limit\": 2, \"logGroupName\": \"USEast1_FlowLogs\", " \
                "\"queryString\": \"fields @timestamp, " \
                "srcAddr, dstAddr, srcPort, dstPort, protocol, start, end, accountId, interfaceId, bytes, packets | " \
                "filter strlen(srcAddr) > 0 or strlen(dstAddr) > 0 or strlen(protocol) > 0 | " \
                "filter ((srcAddr = '172.31.88.64' OR dstAddr = '172.31.88.64'))\", \"startTime\": 1569919390," \
                " \"endTime\": 1577730600}"
        transmission = stix_transmission.StixTransmission('aws_cloud_watch_logs', CONNECTION, CONFIG)
        query_response = transmission.query(query)

        assert query_response is not None
        assert 'success' in query_response
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == "0c8ed381-f1c8-406d-a293-406b64607870:2"

    @staticmethod
    @patch(
        'stix_shifter.stix_transmission.src.modules.aws_cloud_watch_logs.aws_cloud_watch_logs_boto3_client.boto3'
        '.client')
    def test_iam_create_query_connection(mock_create_query):
        mock_create_query.return_value = AWSMockJsonResponse()
        query = "{\"logType\": \"vpcflow\", \"limit\": 10000, \"logGroupName\": \"USEast1_FlowLogs\", " \
                "\"queryString\": \"fields @timestamp, " \
                "srcAddr, dstAddr, srcPort, dstPort, protocol, start, end, accountId, interfaceId, bytes, packets | " \
                "filter strlen(srcAddr) > 0 or strlen(dstAddr) > 0 or strlen(protocol) > 0 | " \
                "filter ((srcAddr = '172.31.88.64' OR dstAddr = '172.31.88.64'))\", \"startTime\": 1569919390," \
                " \"endTime\": 1577730600}"
        transmission = stix_transmission.StixTransmission('aws_cloud_watch_logs', CONNECTION, IAM_CONFIG)
        query_response = transmission.query(query)

        assert query_response is not None
        assert 'success' in query_response
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == "0c8ed381-f1c8-406d-a293-406b64607870:10000"

    @staticmethod
    @patch(
        'stix_shifter.stix_transmission.src.modules.aws_cloud_watch_logs.aws_cloud_watch_logs_boto3_client.boto3'
        '.client')
    def test_create_results_exception(mock_create_results):
        mock_create_results.return_value = MockExceptionResponse()
        search_id = 123
        offset = 0
        length = 10
        transmission = stix_transmission.StixTransmission('aws_cloud_watch_logs', CONNECTION, CONFIG)
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] is False
        assert 'error' in results_response

    @staticmethod
    @patch(
        'stix_shifter.stix_transmission.src.modules.aws_cloud_watch_logs.aws_cloud_watch_logs_boto3_client.boto3'
        '.client')
    def test_create_results_indexerror(mock_create_results):
        mock_create_results.return_value = MockExceptionResponse()
        search_id = 123
        offset = 10
        length = 10000
        transmission = stix_transmission.StixTransmission('aws_cloud_watch_logs', CONNECTION, CONFIG)
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] is False
        assert 'error' in results_response

    @staticmethod
    @patch(
        'stix_shifter.stix_transmission.src.modules.aws_cloud_watch_logs.aws_cloud_watch_logs_boto3_client.boto3'
        '.client')
    def test_create_results_connection(mock_results):
        mock_results.return_value = AWSMockJsonResponse
        search_id = "0c8ed381-f1c8-406d-a293-406b64607870:100"
        offset = 0
        length = 2
        transmission = stix_transmission.StixTransmission('aws_cloud_watch_logs', CONNECTION, CONFIG)
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] is True
        assert 'data' in results_response
        assert results_response['data'] is not None

    @staticmethod
    @patch(
        'stix_shifter.stix_transmission.src.modules.aws_cloud_watch_logs.aws_cloud_watch_logs_boto3_client.boto3'
        '.client')
    def test_delete_query_connection(mock_delete_query):
        mock_delete_query.return_value = AWSMockJsonResponse()
        search_id = "0c8ed381-f1c8-406d-a293-406b64607870:100"
        transmission = stix_transmission.StixTransmission('aws_cloud_watch_logs', CONNECTION, CONFIG)
        delete_response = transmission.delete(search_id)

        assert delete_response is not None
        assert 'success' in delete_response
        assert delete_response['success'] is True

    @staticmethod
    @patch(
        'stix_shifter.stix_transmission.src.modules.aws_cloud_watch_logs.aws_cloud_watch_logs_boto3_client.boto3'
        '.client')
    def test_delete_query_exception(mock_create_status):
        mock_create_status.return_value = MockExceptionResponse()
        search_id = '10.20.30.40'
        transmission = stix_transmission.StixTransmission('aws_cloud_watch_logs', CONNECTION, CONFIG)
        status_response = transmission.delete(search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is False
        assert 'error' in status_response

    @staticmethod
    @patch(
        'stix_shifter.stix_transmission.src.modules.aws_cloud_watch_logs.aws_cloud_watch_logs_boto3_client.boto3'
        '.client')
    def test_create_status_connection(mock_create_status):
        mock_create_status.return_value = AWSMockJsonResponse()
        search_id = "0c8ed381-f1c8-406d-a293-406b64607870:100"
        transmission = stix_transmission.StixTransmission('aws_cloud_watch_logs', CONNECTION, CONFIG)
        status_response = transmission.status(search_id)

        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True
        assert 'status' in status_response
        assert status_response['status'] == 'COMPLETED'

    @staticmethod
    @patch(
        'stix_shifter.stix_transmission.src.modules.aws_cloud_watch_logs.aws_cloud_watch_logs_boto3_client.boto3'
        '.client')
    def test_create_status_running(mock_create_status):
        mock_create_status.return_value = MockStatusResponse()
        search_id = "0c8ed381-f1c8-406d-a293-406b64607870:100"
        transmission = stix_transmission.StixTransmission('aws_cloud_watch_logs', CONNECTION, CONFIG)
        status_response = transmission.status(search_id)

        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True
        assert 'status' in status_response
        assert status_response['status'] == 'RUNNING'

    @staticmethod
    @patch(
        'stix_shifter.stix_transmission.src.modules.aws_cloud_watch_logs.aws_cloud_watch_logs_boto3_client.boto3'
        '.client')
    def test_create_status_exception(mock_create_status):
        mock_create_status.return_value = MockExceptionResponse()
        search_id = "xyz"
        transmission = stix_transmission.StixTransmission('aws_cloud_watch_logs', CONNECTION, CONFIG)
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is False
        assert 'error' in status_response
        assert status_response['code'] == 'invalid_query'
