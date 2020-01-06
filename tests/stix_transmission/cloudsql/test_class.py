from stix_shifter.stix_transmission.src.modules.cloudsql import cloudsql_connector
from stix_shifter.stix_transmission.src.modules.base.base_status_connector import Status
import pandas as pd
from unittest.mock import patch
import json
import unittest


@patch('ibmcloudsql.SQLQuery.__init__', autospec=True)
@patch('ibmcloudsql.SQLQuery.logon', autospec=True)
class TestCloudSQLConnection(unittest.TestCase, object):
    def test_is_async(self, mock_api_client_logon, mock_api_client):
        mock_api_client_logon.return_value = None
        mock_api_client.return_value = None
        module = cloudsql_connector
        config = {
            "auth": {
                "bxapikey": "placeholder"
            },
            "client_info": "placeholder"
        }
        connection = {
            "instance_crn": "placeholder",
            "target_cos": "placeholder"
        }
        check_async = module.Connector(connection, config).is_async

        assert check_async

    @patch('ibmcloudsql.SQLQuery.get_jobs')
    def test_ping_endpoint(self, mock_ping_response, mock_api_client_logon,
                           mock_api_client):
        mock_api_client_logon.return_value = None
        mock_api_client.return_value = None
        mocked_return_value = '[{"job_id": "placeholder", "status": "placeholder",\
                               "user_id": "placeholder", "statement": "placeholder",\
                               "resultset_location": "placeholder", "submit_time": "placeholder",\
                               "end_time": "placeholder", "error": "placeholder", error_message": "placeholder"}]'
        mock_ping_response.return_value = mocked_return_value

        module = cloudsql_connector
        config = {
            "auth": {
                "bxapikey": "placeholder"
            },
            "client_info": "placeholder"
        }
        connection = {
            "instance_crn": "placeholder",
            "target_cos": "placeholder"
        }
        ping_response = module.Connector(connection, config).ping()

        assert ping_response is not None
        assert ping_response['success']

    @patch('ibmcloudsql.SQLQuery.submit_sql')
    def test_query_response(self, mock_query_response, mock_api_client_logon,
                            mock_api_client):
        mock_api_client_logon.return_value = None
        mock_api_client.return_value = None
        mocked_return_value = '108cb8b0-0744-4dd9-8e35-ea8311cd6211'
        mock_query_response.return_value = mocked_return_value

        module = cloudsql_connector
        config = {
            "auth": {
                "bxapikey": "placeholder"
            },
            "client_info": "placeholder"
        }
        connection = {
            "instance_crn": "placeholder",
            "target_cos": "placeholder"
        }
        query = '{"query":"SELECT target.id from cos://us-geo/at-data/rest.1*.json STORED AS JSON c"}'
        query_response = module.Connector(connection, config).create_query_connection(query)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == "108cb8b0-0744-4dd9-8e35-ea8311cd6211"

    @patch('ibmcloudsql.SQLQuery.get_job', autospec=True)
    def test_status_response(self, mock_status_response,
                             mock_api_client_logon, mock_api_client):
        mock_api_client_logon.return_value = None
        mock_api_client.return_value = None
        mocked_return_value = json.loads('{"status": "completed", "end_time": "2018-08-28T15:51:24.899Z", "submit_time": "2018-08-28T15:51:19.899Z"}')
        mock_status_response.return_value = mocked_return_value

        module = cloudsql_connector
        config = {
            "auth": {
                "bxapikey": "placeholder"
            },
            "client_info": "placeholder"
        }
        connection = {
            "instance_crn": "placeholder",
            "target_cos": "placeholder"
        }
        search_id = "108cb8b0-0744-4dd9-8e35-ea8311cd6211"
        status_response = module.Connector(connection, config).create_status_connection(search_id)

        assert status_response is not None
        assert status_response['success']
        assert 'status' in status_response
        assert status_response['status'] == Status.COMPLETED.value

    @patch('stix_shifter.stix_transmission.src.modules.cloudsql.cloudsql_results_connector.CloudSQLResultsConnector.records', autospec=True)
    def test_results_response(self, mock_results_response,
                              mock_api_client_logon, mock_api_client):
        mock_api_client_logon.return_value = None
        mock_api_client.return_value = None
        mocked_return_value = pd.DataFrame(columns=['id'])
        mocked_return_value = mocked_return_value.append([{'id': 'crn:v1:bluemix:public:iam-identity::a/::apikey:1234'}], ignore_index=True)
        mock_results_response.return_value = mocked_return_value

        module = cloudsql_connector
        config = {
            "auth": {
                "bxapikey": "placeholder"
            },
            "client_info": "placeholder"
        }
        connection = {
            "instance_crn": "placeholder",
            "target_cos": "placeholder"
        }
        search_id = "108cb8b0-0744-4dd9-8e35-ea8311cd6211"
        offset = 0
        length = 1
        results_response = module.Connector(connection, config).create_results_connection(search_id, offset, length)

        assert results_response is not None
        assert results_response['success']
        assert 'data' in results_response
        assert len(results_response['data']) > 0

    @patch('ibmcloudsql.SQLQuery.delete_result', autospec=True)
    def test_delete_response(self, mock_delete_response,
                             mock_api_client_logon, mock_api_client):
        mock_api_client_logon.return_value = None
        mock_api_client.return_value = None
        mocked_return_value = pd.DataFrame(columns=['Deleted Object'])
        mocked_return_value = mocked_return_value.append([{'Deleted Object': 'result/jobid=9b0f77b1-74e6-4953-84df-e0571a398ef7/part-00000-17db0efc-f563-45c2-9d12-560933cd01b6-c000-attempt_20181016200828_0024_m_000000_0.csv'}], ignore_index=True)
        mock_delete_response.return_value = mocked_return_value

        module = cloudsql_connector
        config = {
            "auth": {
                "bxapikey": "placeholder"
            },
            "client_info": "placeholder"
        }
        connection = {
            "instance_crn": "placeholder",
            "target_cos": "placeholder"
        }
        search_id = "108cb8b0-0744-4dd9-8e35-ea8311cd6211"
        delete_response = module.Connector(connection, config).delete_query_connection(search_id)

        assert delete_response is not None
        assert delete_response['success']

    @patch('ibmcloudsql.SQLQuery.submit_sql')
    @patch('ibmcloudsql.SQLQuery.get_job', autospec=True)
    @patch('ibmcloudsql.SQLQuery.get_result', autospec=True)
    def test_query_flow(self, mock_results_response, mock_status_response,
                        mock_query_response, mock_api_client_logon, mock_api_client):
        mock_api_client_logon.return_value = None
        mock_api_client.return_value = None
        results_mock = pd.DataFrame(columns=['id'])
        results_mock = results_mock.append([{'id': 'crn:v1:bluemix:public:iam-identity::a/::apikey:1234'}], ignore_index=True)
        query_mock = '108cb8b0-0744-4dd9-8e35-ea8311cd6211'
        status_mock = json.loads('{"status": "completed", "end_time": "2018-08-28T15:51:24.899Z", "submit_time": "2018-08-28T15:51:19.899Z"}')
        mock_results_response.return_value = results_mock
        mock_status_response.return_value = status_mock
        mock_query_response.return_value = query_mock
        module = cloudsql_connector
        config = {
            "auth": {
                "bxapikey": "placeholder"
            },
            "client_info": "placeholder"
        }
        connection = {
            "instance_crn": "placeholder",
            "target_cos": "placeholder"
        }
        query = '{"query":"SELECT target.id from cos://us-geo/at-data/rest.1*.json STORED AS JSON c"}'

        query_response = module.Connector(connection, config).create_query_connection(query)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == "108cb8b0-0744-4dd9-8e35-ea8311cd6211"

        search_id = "108cb8b0-0744-4dd9-8e35-ea8311cd6211"
        status_response = module.Connector(connection, config).create_status_connection(search_id)

        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == Status.COMPLETED.value

        offset = 0
        length = 1
        results_response = module.Connector(connection, config).create_results_connection(search_id, offset, length)

        assert results_response is not None
        assert 'data' in results_response
        assert len(results_response['data']) > 0
