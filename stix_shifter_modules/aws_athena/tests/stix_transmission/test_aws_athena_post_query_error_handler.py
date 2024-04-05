
import unittest
from unittest.mock import patch
import stix_shifter_modules

from stix_shifter_modules.aws_athena.stix_transmission.boto3_client import BOTO3Client
from stix_shifter_modules.aws_athena.stix_transmission.post_query_connector_error_handling import PostQueryConnectorErrorHandler
from stix_shifter_modules.aws_athena.tests.stix_transmission.test_aws_athena import AWSMockJsonResponse
from tests.utils.async_utils import get_aws_mock_response

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


ip_address_column_not_found = {'success': True, 'status': 'ERROR', 'message': "COLUMN_NOT_FOUND: line 1:877: Column 'dst_endpoint.ip' cannot be resolved or requester is not authorized to access requested resources", 'progress': 0}
equal_query = 'SELECT CAST(metadata as JSON) AS metadata, CAST(time as JSON) AS time, CAST(cloud as JSON) AS cloud, CAST(api as JSON) AS api, CAST(ref_event_uid as JSON) AS ref_event_uid, CAST(src_endpoint as JSON) AS src_endpoint, CAST(resources as JSON) AS resources, CAST(identity as JSON) AS identity, CAST(http_request as JSON) AS http_request, CAST(class_name as JSON) AS class_name, CAST(class_uid as JSON) AS class_uid, CAST(category_name as JSON) AS category_name, CAST(category_uid as JSON) AS category_uid, CAST(severity_id as JSON) AS severity_id, CAST(severity as JSON) AS severity, CAST(activity_name as JSON) AS activity_name, CAST(activity_id as JSON) AS activity_id, CAST(type_uid as JSON) AS type_uid, CAST(type_name as JSON) AS type_name, CAST(unmapped as JSON) AS unmapped FROM cf_moose_db."cloudtrail" WHERE ((lower(dst_endpoint.ip) = lower(\'192.168.0.52\') OR lower(src_endpoint.ip) = lower(\'192.168.0.52\')) AND time BETWEEN 1641026590000 AND 1698748990000)'
doesnt_equal_query = 'SELECT CAST(metadata as JSON) AS metadata, CAST(time as JSON) AS time, CAST(cloud as JSON) AS cloud, CAST(api as JSON) AS api, CAST(ref_event_uid as JSON) AS ref_event_uid, CAST(src_endpoint as JSON) AS src_endpoint, CAST(resources as JSON) AS resources, CAST(identity as JSON) AS identity, CAST(http_request as JSON) AS http_request, CAST(class_name as JSON) AS class_name, CAST(class_uid as JSON) AS class_uid, CAST(category_name as JSON) AS category_name, CAST(category_uid as JSON) AS category_uid, CAST(severity_id as JSON) AS severity_id, CAST(severity as JSON) AS severity, CAST(activity_name as JSON) AS activity_name, CAST(activity_id as JSON) AS activity_id, CAST(type_uid as JSON) AS type_uid, CAST(type_name as JSON) AS type_name, CAST(unmapped as JSON) AS unmapped FROM cf_moose_db."cloudtrail" WHERE ((lower(dst_endpoint.ip) != lower(\'192.168.0.52\') OR lower(src_endpoint.ip) != lower(\'192.168.0.52\')) AND time BETWEEN 1641026590000 AND 1698748990000)'
greater_than_query = 'SELECT CAST(metadata as JSON) AS metadata, CAST(time as JSON) AS time, CAST(cloud as JSON) AS cloud, CAST(api as JSON) AS api, CAST(ref_event_uid as JSON) AS ref_event_uid, CAST(src_endpoint as JSON) AS src_endpoint, CAST(resources as JSON) AS resources, CAST(identity as JSON) AS identity, CAST(http_request as JSON) AS http_request, CAST(class_name as JSON) AS class_name, CAST(class_uid as JSON) AS class_uid, CAST(category_name as JSON) AS category_name, CAST(category_uid as JSON) AS category_uid, CAST(severity_id as JSON) AS severity_id, CAST(severity as JSON) AS severity, CAST(activity_name as JSON) AS activity_name, CAST(activity_id as JSON) AS activity_id, CAST(type_uid as JSON) AS type_uid, CAST(type_name as JSON) AS type_name, CAST(unmapped as JSON) AS unmapped FROM cf_moose_db."cloudtrail" WHERE ((lower(dst_endpoint.ip) > lower(\'192.168.0.52\') OR lower(src_endpoint.ip) > lower(\'192.168.0.52\')) AND time BETWEEN 1641026590000 AND 1698748990000)'
in_query = 'SELECT CAST(metadata as JSON) AS metadata, CAST(time as JSON) AS time, CAST(cloud as JSON) AS cloud, CAST(api as JSON) AS api, CAST(ref_event_uid as JSON) AS ref_event_uid, CAST(src_endpoint as JSON) AS src_endpoint, CAST(resources as JSON) AS resources, CAST(identity as JSON) AS identity, CAST(http_request as JSON) AS http_request, CAST(class_name as JSON) AS class_name, CAST(class_uid as JSON) AS class_uid, CAST(category_name as JSON) AS category_name, CAST(category_uid as JSON) AS category_uid, CAST(severity_id as JSON) AS severity_id, CAST(severity as JSON) AS severity, CAST(activity_name as JSON) AS activity_name, CAST(activity_id as JSON) AS activity_id, CAST(type_uid as JSON) AS type_uid, CAST(type_name as JSON) AS type_name, CAST(unmapped as JSON) AS unmapped FROM cf_moose_db."cloudtrail" WHERE ((dst_endpoint.ip IN (\'172.31.92.201\', \'172.31.30.227\') OR src_endpoint.ip IN (\'172.31.92.201\', \'172.31.30.227\')) AND time BETWEEN 1641026590000 AND 1698748990000)'
like_query = 'SELECT CAST(metadata as JSON) AS metadata, CAST(time as JSON) AS time, CAST(cloud as JSON) AS cloud, CAST(api as JSON) AS api, CAST(ref_event_uid as JSON) AS ref_event_uid, CAST(src_endpoint as JSON) AS src_endpoint, CAST(resources as JSON) AS resources, CAST(identity as JSON) AS identity, CAST(http_request as JSON) AS http_request, CAST(class_name as JSON) AS class_name, CAST(class_uid as JSON) AS class_uid, CAST(category_name as JSON) AS category_name, CAST(category_uid as JSON) AS category_uid, CAST(severity_id as JSON) AS severity_id, CAST(severity as JSON) AS severity, CAST(activity_name as JSON) AS activity_name, CAST(activity_id as JSON) AS activity_id, CAST(type_uid as JSON) AS type_uid, CAST(type_name as JSON) AS type_name, CAST(unmapped as JSON) AS unmapped FROM cf_moose_db."cloudtrail" WHERE ((lower(dst_endpoint.ip) LIKE lower(\'192.168.0.52\') OR lower(src_endpoint.ip) LIKE lower(\'192.168.0.52\')) AND time BETWEEN 1641026590000 AND 1698748990000)'
match_query = 'SELECT CAST(metadata as JSON) AS metadata, CAST(time as JSON) AS time, CAST(cloud as JSON) AS cloud, CAST(api as JSON) AS api, CAST(ref_event_uid as JSON) AS ref_event_uid, CAST(src_endpoint as JSON) AS src_endpoint, CAST(resources as JSON) AS resources, CAST(identity as JSON) AS identity, CAST(http_request as JSON) AS http_request, CAST(class_name as JSON) AS class_name, CAST(class_uid as JSON) AS class_uid, CAST(category_name as JSON) AS category_name, CAST(category_uid as JSON) AS category_uid, CAST(severity_id as JSON) AS severity_id, CAST(severity as JSON) AS severity, CAST(activity_name as JSON) AS activity_name, CAST(activity_id as JSON) AS activity_id, CAST(type_uid as JSON) AS type_uid, CAST(type_name as JSON) AS type_name, CAST(unmapped as JSON) AS unmapped FROM cf_moose_db."cloudtrail" WHERE ((REGEXP_LIKE(CAST(dst_endpoint.ip as varchar), \'192.168.0.52\') OR REGEXP_LIKE(CAST(src_endpoint.ip as varchar), \'192.168.0.52\')) AND time BETWEEN 1641026590000 AND 1698748990000)'


equal_query_replaced_column = 'SELECT CAST(metadata as JSON) AS metadata, CAST(time as JSON) AS time, CAST(cloud as JSON) AS cloud, CAST(api as JSON) AS api, CAST(ref_event_uid as JSON) AS ref_event_uid, CAST(src_endpoint as JSON) AS src_endpoint, CAST(resources as JSON) AS resources, CAST(identity as JSON) AS identity, CAST(http_request as JSON) AS http_request, CAST(class_name as JSON) AS class_name, CAST(class_uid as JSON) AS class_uid, CAST(category_name as JSON) AS category_name, CAST(category_uid as JSON) AS category_uid, CAST(severity_id as JSON) AS severity_id, CAST(severity as JSON) AS severity, CAST(activity_name as JSON) AS activity_name, CAST(activity_id as JSON) AS activity_id, CAST(type_uid as JSON) AS type_uid, CAST(type_name as JSON) AS type_name, CAST(unmapped as JSON) AS unmapped FROM cf_moose_db."cloudtrail" WHERE ((FALSE OR lower(src_endpoint.ip) = lower(\'192.168.0.52\')) AND time BETWEEN 1641026590000 AND 1698748990000)'
doesnt_equal_query_replaced_column = 'SELECT CAST(metadata as JSON) AS metadata, CAST(time as JSON) AS time, CAST(cloud as JSON) AS cloud, CAST(api as JSON) AS api, CAST(ref_event_uid as JSON) AS ref_event_uid, CAST(src_endpoint as JSON) AS src_endpoint, CAST(resources as JSON) AS resources, CAST(identity as JSON) AS identity, CAST(http_request as JSON) AS http_request, CAST(class_name as JSON) AS class_name, CAST(class_uid as JSON) AS class_uid, CAST(category_name as JSON) AS category_name, CAST(category_uid as JSON) AS category_uid, CAST(severity_id as JSON) AS severity_id, CAST(severity as JSON) AS severity, CAST(activity_name as JSON) AS activity_name, CAST(activity_id as JSON) AS activity_id, CAST(type_uid as JSON) AS type_uid, CAST(type_name as JSON) AS type_name, CAST(unmapped as JSON) AS unmapped FROM cf_moose_db."cloudtrail" WHERE ((TRUE OR lower(src_endpoint.ip) != lower(\'192.168.0.52\')) AND time BETWEEN 1641026590000 AND 1698748990000)'
greater_than_query_replaced_column = 'SELECT CAST(metadata as JSON) AS metadata, CAST(time as JSON) AS time, CAST(cloud as JSON) AS cloud, CAST(api as JSON) AS api, CAST(ref_event_uid as JSON) AS ref_event_uid, CAST(src_endpoint as JSON) AS src_endpoint, CAST(resources as JSON) AS resources, CAST(identity as JSON) AS identity, CAST(http_request as JSON) AS http_request, CAST(class_name as JSON) AS class_name, CAST(class_uid as JSON) AS class_uid, CAST(category_name as JSON) AS category_name, CAST(category_uid as JSON) AS category_uid, CAST(severity_id as JSON) AS severity_id, CAST(severity as JSON) AS severity, CAST(activity_name as JSON) AS activity_name, CAST(activity_id as JSON) AS activity_id, CAST(type_uid as JSON) AS type_uid, CAST(type_name as JSON) AS type_name, CAST(unmapped as JSON) AS unmapped FROM cf_moose_db."cloudtrail" WHERE ((FALSE OR lower(src_endpoint.ip) > lower(\'192.168.0.52\')) AND time BETWEEN 1641026590000 AND 1698748990000)'
in_query_replaced_column = 'SELECT CAST(metadata as JSON) AS metadata, CAST(time as JSON) AS time, CAST(cloud as JSON) AS cloud, CAST(api as JSON) AS api, CAST(ref_event_uid as JSON) AS ref_event_uid, CAST(src_endpoint as JSON) AS src_endpoint, CAST(resources as JSON) AS resources, CAST(identity as JSON) AS identity, CAST(http_request as JSON) AS http_request, CAST(class_name as JSON) AS class_name, CAST(class_uid as JSON) AS class_uid, CAST(category_name as JSON) AS category_name, CAST(category_uid as JSON) AS category_uid, CAST(severity_id as JSON) AS severity_id, CAST(severity as JSON) AS severity, CAST(activity_name as JSON) AS activity_name, CAST(activity_id as JSON) AS activity_id, CAST(type_uid as JSON) AS type_uid, CAST(type_name as JSON) AS type_name, CAST(unmapped as JSON) AS unmapped FROM cf_moose_db."cloudtrail" WHERE ((FALSE OR src_endpoint.ip IN (\'172.31.92.201\', \'172.31.30.227\')) AND time BETWEEN 1641026590000 AND 1698748990000)'
like_query_replaced_column = 'SELECT CAST(metadata as JSON) AS metadata, CAST(time as JSON) AS time, CAST(cloud as JSON) AS cloud, CAST(api as JSON) AS api, CAST(ref_event_uid as JSON) AS ref_event_uid, CAST(src_endpoint as JSON) AS src_endpoint, CAST(resources as JSON) AS resources, CAST(identity as JSON) AS identity, CAST(http_request as JSON) AS http_request, CAST(class_name as JSON) AS class_name, CAST(class_uid as JSON) AS class_uid, CAST(category_name as JSON) AS category_name, CAST(category_uid as JSON) AS category_uid, CAST(severity_id as JSON) AS severity_id, CAST(severity as JSON) AS severity, CAST(activity_name as JSON) AS activity_name, CAST(activity_id as JSON) AS activity_id, CAST(type_uid as JSON) AS type_uid, CAST(type_name as JSON) AS type_name, CAST(unmapped as JSON) AS unmapped FROM cf_moose_db."cloudtrail" WHERE ((FALSE OR lower(src_endpoint.ip) LIKE lower(\'192.168.0.52\')) AND time BETWEEN 1641026590000 AND 1698748990000)'
match_query_replaced_column = 'SELECT CAST(metadata as JSON) AS metadata, CAST(time as JSON) AS time, CAST(cloud as JSON) AS cloud, CAST(api as JSON) AS api, CAST(ref_event_uid as JSON) AS ref_event_uid, CAST(src_endpoint as JSON) AS src_endpoint, CAST(resources as JSON) AS resources, CAST(identity as JSON) AS identity, CAST(http_request as JSON) AS http_request, CAST(class_name as JSON) AS class_name, CAST(class_uid as JSON) AS class_uid, CAST(category_name as JSON) AS category_name, CAST(category_uid as JSON) AS category_uid, CAST(severity_id as JSON) AS severity_id, CAST(severity as JSON) AS severity, CAST(activity_name as JSON) AS activity_name, CAST(activity_id as JSON) AS activity_id, CAST(type_uid as JSON) AS type_uid, CAST(type_name as JSON) AS type_name, CAST(unmapped as JSON) AS unmapped FROM cf_moose_db."cloudtrail" WHERE ((FALSE OR REGEXP_LIKE(CAST(src_endpoint.ip as varchar), \'192.168.0.52\')) AND time BETWEEN 1641026590000 AND 1698748990000)'


class TestAWSConnection(unittest.IsolatedAsyncioTestCase):  
    #----Test Against the check_status_for_missing_column method
    @staticmethod
    @patch('stix_shifter_modules.aws_athena.stix_transmission.boto3_client.BOTO3Client.makeRequest')
    async def test_no_column_missing(mock_status_query):
        mock_status_query.return_value = get_aws_mock_response(AWSMockJsonResponse.get_query_execution(**{}))
        client = BOTO3Client(CONNECTION, CONFIGURATION)
        test_query = "test"
        query_response = await PostQueryConnectorErrorHandler.check_status_for_missing_column(client, "1", test_query)

        assert query_response == True
    
    @staticmethod
    @patch('time.sleep')
    @patch('stix_shifter_modules.aws_athena.stix_transmission.boto3_client.BOTO3Client.makeRequest')
    async def test_stuck_waiting(mock_status_query, mock_time):
        mock_status_query.return_value = get_aws_mock_response(AWSMockJsonResponse.get_query_execution_running_status(**{}))
        mock_time.return_value = "do_nothing"
        client = BOTO3Client(CONNECTION, CONFIGURATION)
        test_query = "test"
        query_response = await PostQueryConnectorErrorHandler.check_status_for_missing_column(client, "1", test_query)

        assert query_response == True

    #----Test Against the _remove_invalid_column_table method
    @staticmethod
    @patch('stix_shifter_modules.aws_athena.stix_transmission.status_connector.StatusConnector.create_status_connection')
    async def test_column_missing_equals(mock_status_query):
        mock_status_query.return_value = ip_address_column_not_found
        client = BOTO3Client(CONNECTION, CONFIGURATION)
        query_response = await PostQueryConnectorErrorHandler.check_status_for_missing_column(client, "1", equal_query)
        assert query_response == equal_query_replaced_column
        
    @staticmethod
    @patch('stix_shifter_modules.aws_athena.stix_transmission.status_connector.StatusConnector.create_status_connection')
    async def test_column_missing_doesnt_equal(mock_status_query):
        mock_status_query.return_value = ip_address_column_not_found
        client = BOTO3Client(CONNECTION, CONFIGURATION)
        query_response = await PostQueryConnectorErrorHandler.check_status_for_missing_column(client, "1", doesnt_equal_query)
        assert query_response == doesnt_equal_query_replaced_column

    @staticmethod
    @patch('stix_shifter_modules.aws_athena.stix_transmission.status_connector.StatusConnector.create_status_connection')
    async def test_column_missing_greater_than(mock_status_query):
        mock_status_query.return_value = ip_address_column_not_found
        client = BOTO3Client(CONNECTION, CONFIGURATION)
        query_response = await PostQueryConnectorErrorHandler.check_status_for_missing_column(client, "1", greater_than_query)

        assert query_response == greater_than_query_replaced_column
        
    @staticmethod
    @patch('stix_shifter_modules.aws_athena.stix_transmission.status_connector.StatusConnector.create_status_connection')
    async def test_column_missing_in_query(mock_status_query):
        mock_status_query.return_value = ip_address_column_not_found
        client = BOTO3Client(CONNECTION, CONFIGURATION)
        query_response = await PostQueryConnectorErrorHandler.check_status_for_missing_column(client, "1", in_query)

        assert query_response == in_query_replaced_column
        
    @staticmethod
    @patch('stix_shifter_modules.aws_athena.stix_transmission.status_connector.StatusConnector.create_status_connection')
    async def test_column_missing_like_query(mock_status_query):
        mock_status_query.return_value = ip_address_column_not_found
        client = BOTO3Client(CONNECTION, CONFIGURATION)
        query_response = await PostQueryConnectorErrorHandler.check_status_for_missing_column(client, "1", like_query)

        assert query_response == like_query_replaced_column

    @staticmethod
    @patch('stix_shifter_modules.aws_athena.stix_transmission.status_connector.StatusConnector.create_status_connection')
    async def test_column_missing_match_query(mock_status_query):
        mock_status_query.return_value = ip_address_column_not_found
        client = BOTO3Client(CONNECTION, CONFIGURATION)
        query_response = await PostQueryConnectorErrorHandler.check_status_for_missing_column(client, "1", match_query)

        assert query_response == match_query_replaced_column