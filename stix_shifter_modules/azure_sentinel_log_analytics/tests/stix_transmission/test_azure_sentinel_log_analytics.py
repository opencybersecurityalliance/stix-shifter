from stix_shifter_modules.azure_sentinel_log_analytics.entry_point import EntryPoint
import unittest
from unittest.mock import patch
from stix_shifter.stix_transmission import stix_transmission


class AzureSentinelMockResponse:
    def __init__(self, response_code, obj):
        self.code = response_code
        self.object = obj

    def read(self):
        return self.object


class MockToken:
    token = "access_token123"


class ClientSecretMockResponse:

    @staticmethod
    def get_token(scope):
        return MockToken


@patch('stix_shifter_modules.azure_sentinel_log_analytics.stix_transmission.connector.ClientSecretCredential')
@patch('stix_shifter_modules.azure_sentinel_log_analytics.stix_transmission.api_client.APIClient.__init__')
class TestAzureSentinalConnection(unittest.TestCase, object):
    def connection(self):
        return {
            "host": "host",
            "port": 443,
            "workspaceId": "abc12345"
        }

    def config(self):
        return {
            "auth": {
                "tenant": "abc12345",
                "clientId": "abc12345",
                "clientSecret": "abc12345"
            }
        }

    def test_is_async(self, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mock_generate_token.return_value = ClientSecretMockResponse
        entry_point = EntryPoint(self.connection(), self.config())
        check_async = entry_point.is_async()

        assert check_async is False

    @patch('stix_shifter_modules.azure_sentinel_log_analytics.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_endpoint(self, mock_ping_response, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mock_generate_token.return_value = ClientSecretMockResponse
        mocked_return_value = '["mock", "placeholder"]'

        mock_ping_response.return_value = AzureSentinelMockResponse(200, mocked_return_value)
        transmission = stix_transmission.StixTransmission('azure_sentinel_log_analytics', self.connection(), self.config())
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success']

    @patch('stix_shifter_modules.azure_sentinel_log_analytics.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_endpoint_exception(self, mock_ping_response, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mock_generate_token.return_value = ClientSecretMockResponse
        mocked_return_value = """{
          "error": {
            "code": "BadRequest",
            "message": "Resource not found for the segment 'alert'.",
            "innerError": {
              "request-id": "ba365a15-50ff-4041-bdc4-9dbacbd45239",
              "date": "2019-11-26T11:36:27"
            }
          }
        }"""
        mock_ping_response.return_value = AzureSentinelMockResponse(400, mocked_return_value)

        transmission = stix_transmission.StixTransmission('azure_sentinel_log_analytics', self.connection(), self.config())
        ping_response = transmission.ping()
        assert ping_response['success'] is False
        assert ping_response[
                   'error'] == "azure_sentinel_log_analytics connector error => Resource not found for the segment \'alert\'."
        assert ping_response['code'] == "invalid_parameter"

    def test_query_connection(self, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mock_generate_token.return_value = ClientSecretMockResponse

        query = "SecurityEvent | where IpAddress == '80.66.76.145'"
        transmission = stix_transmission.StixTransmission('azure_sentinel_log_analytics', self.connection(), self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == query

    def test_status_query(self, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mock_generate_token.return_value = ClientSecretMockResponse

        search_id = "SecurityEvent | where IpAddress == '80.66.76.145'"

        entry_point = EntryPoint(self.connection(), self.config())
        status_response = entry_point.create_status_connection(search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True

    @patch(
        'stix_shifter_modules.azure_sentinel_log_analytics.stix_transmission.connector.Connector.create_results_connection')
    def test_results_all_response(self, mock_results_response, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mock_generate_token.return_value = ClientSecretMockResponse
        mocked_return_value = {
            "success": True,
            "data": [
                {
                    "TenantId": "e00daaf8-d6a4-4410-b50b-f5ef61c9cb45",
                    "TimeGenerated": "2022-07-03 09:12:07.122000+00:00",
                    "DisplayName": "AlertLog",
                    "AlertName": "AlertLog",
                    "AlertSeverity": "Medium",
                    "Description": "",
                    "ProviderName": "ASI Scheduled Alerts",
                    "VendorName": "Microsoft",
                    "VendorOriginalId": "d38cf0b5-84bf-486d-8de3-26cc0a561be7",
                    "SystemAlertId": "6dfa10b7-7523-ecb0-646d-28ccf9c06772",
                    "ResourceId": "",
                    "SourceComputerId": "",
                    "AlertType": "e00daaf8-d6a4-4410-b50b-f5ef61c9cb45_9c4be437-b74c-440c-aa09-764367744a23",
                    "ConfidenceLevel": "",
                    "ConfidenceScore": "None",
                    "IsIncident": "False",
                    "StartTime": "2022-07-03 08:33:37.792000+00:00",
                    "EndTime": "2022-07-03 08:33:37.792000+00:00",
                    "ProcessingEndTime": "2022-07-03 09:12:06.758000+00:00",
                    "RemediationSteps": "",
                    "ExtendedProperties": "{\"Query Period\":\"00:05:00\",\"Trigger Operator\":\"GreaterThan\",\"Trigger Threshold\":\"0\",\"Correlation Id\":\"e00daaf8-d6a4-4410-b50b-f5ef61c9cb45_9c4be437-b74c-440c-aa09-764367744a23_637924344629201027\",\"Search Query Results Overall Count\":\"1\",\"Data Sources\":\"[\\\"loganaly\\\"]\",\"Query\":\"// might contain sensitive data\\nlet alertedEvent = datatable(compressedRec: string)\\n['eAGlVttu2zgQ/RXBL90Fylj3i99SJ9sGSNogNvqwdVGMyGEsVBcvKWXjBvn3HcqWLTtONnX8YEjknMMzw9HMPAy+LFBBnVXlZyhwMBq8g0Zk9YX8XNXn95mu9TvrusozvrSAG7OTwftdzFfIGwO8yriqdCXrk9Omnlcq+9WaDBcGnaEe7hMPV4TEd4l3mBPFRSkrVbQwyGn9lAzusno5qaFuNBlMGs4RBYonm52KgxZNqjuGQ8sdlvZuUFeN4vhRVc1itWTMuMoWRtWFoDXB3VDKIGJ2kETM5zxmsZ24DCBIEzeRsfQSwo0rpTCHDQwjIT3uxsyVMcECT7A4cl0mE5Ap8sTzfCN6DHmOiuwjmboSYptFjpcwPw6AJZByFvJAOL4TgLRhY3+xOBVCoV67OIYabyu1pLfV5fXWOm83G5+m0+sb/KdBXa/Q16qiC67pzuj9YTbI9LgqFnkGJcfxHPnP2WA0G/wFucbZ4P1soNZBu6x46y5tl02e045B6LpSukUkri9jcMjlMBXMT2PBEi+VLJEQohvyVMZpS9ilTIv69jCbrZeWZyizMluF1KyOzN9woaq7TKDSwxdzsIfWQ186ThoEHhO+i8xHD1icpMg8l4MX+hyEzw35++3hE6zfdv4OgR460gMpZMKEzemCuUkIP5KkQ0DoeBjZEO9J2MJvUKJCCm9PCGkoa0rsM9TZbUnXfUkJMZ1D+eXfktRdVQQlTeXtS46ZT3rDeITEHbKzTC9yWO5wnv5qFFoT5I0irdYHcmJegPr5Es9Xkm8Sq+MI7BPvxH42ODvnHXHT/+OAVcB9VjSFVUnLs6o2uJaeV00urBQt0YVfWFTOrCV9G5buFZFnD9v3klx8wclzKZHXW1V71XUPd6qNqIISpJ+5fVl6+JrC9upk3x6oh91lj+kN1Ycmy+uL8lmBO8H+PejB65qMLYoaNHlt/dF3eGS9xuE/nz1swqlMviWWzzJfgyIPyN/2FkcPjwetzk235GgeryqxVbJ2do/9/B6LdQ9bsX77/vi9rbbUfMu66w5tyV21htVmW1Ha1WM8NBQFVSG4xZbj2CGhJZpnNHYoPl/JmQ0eqVedG/HUootMm29nmtFpNRSmd7s2dVeb9HlTOx55wchxTxzften3txkD+gJWja47a0doNxLoITe9bxWbbUMcKgTRytNtPhwdqcfe+NEODEew9GezliNKnUCkQci8wOXMBzdgwB3OMOFOGGEA4KS9c6/XH3d/nLM2AThg+HT4O2T9+qGpvc4zqKFV74eeSG0umQtpSCCf2o9D7cdDO/JsCO3ICQg0xRJMXTNDlm0LABkzEYLPfN+xWRrYKZMBytDhCU/9FkFp8hFLEykUT1PFG3nRSZRsUmXSejFZ6hoLsm472H4G/RDrqWcwziErukGsfd7ubUer7dqnLq1XkOlygd0h3ahKyz/enBuP/wEakf8J']\\n| extend raw = todynamic(zlib_decompress_from_base64_string(compressedRec)) | evaluate bag_unpack(raw) | project-away compressedRec;\\nalertedEvent\",\"OriginalQuery\":\"union AzureActivity\\n\",\"Query Start Time UTC\":\"2022-07-03 08:31:02Z\",\"Query End Time UTC\":\"2022-07-03 08:36:02Z\",\"Analytic Rule Ids\":\"[\\\"9c4be437-b74c-440c-aa09-764367744a23\\\"]\",\"Event Grouping\":\"AlertPerEvent\",\"Analytic Rule Name\":\"AlertLog\",\"ProcessedBySentinel\":\"True\",\"Alert generation status\":\"Full alert created\"}",
                    "Entities": "",
                    "SourceSystem": "Detection",
                    "WorkspaceSubscriptionId": "dc26ff57-0597-4cc8-8092-aa5b929f8f39",
                    "WorkspaceResourceGroup": "newresource",
                    "ExtendedLinks": "",
                    "ProductName": "Azure Sentinel",
                    "ProductComponentName": "Scheduled Alerts",
                    "AlertLink": "",
                    "Status": "New",
                    "CompromisedEntity": "",
                    "Tactics": "ResourceDevelopment",
                    "Techniques": "",
                    "Type": "SecurityAlert"
                }
            ]
        }
        mock_results_response.return_value = mocked_return_value
        offset = 0
        length = 1
        search_id = "SecurityAlert | where AlertName == 'AlertLog' | limit {len}".format(len=length)
        entry_point = EntryPoint(self.connection(), self.config())
        results_response = entry_point.create_results_connection(search_id, offset, length)

        assert results_response is not None
        assert results_response['success']
        assert 'data' in results_response
        assert results_response['data'] is not None

    @patch(
        'stix_shifter_modules.azure_sentinel_log_analytics.stix_transmission.connector.Connector.create_results_connection')
    def test_results_all_response_empty(self, mock_results_response, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mock_generate_token.return_value = ClientSecretMockResponse
        mocked_return_value = {
            "success": True,
            "data": []
        }
        mock_results_response.return_value = mocked_return_value
        offset = 0
        length = 1
        search_id = "SecurityAlert | where AlertName == 'AlertLog' | limit {len}".format(len=length)
        entry_point = EntryPoint(self.connection(), self.config())
        results_response = entry_point.create_results_connection(search_id, offset, length)

        assert 'success' in results_response
        assert results_response['success'] is True
        assert 'data' in results_response
        assert len(results_response['data']) == 0

    @patch('stix_shifter_modules.azure_sentinel_log_analytics.stix_transmission.api_client.APIClient.run_search')
    def test_results_response_exception(self, mock_results_response, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mock_generate_token.return_value = ClientSecretMockResponse
        mocked_return_value = {
                "code": "BadRequest",
                "message": "Invalid filter clause",
                "innerError": {
                    "request-id": "e8904fd5-0f2c-496d-9ed0-4ee5c58946ff",
                    "date": "2019-11-26T11:30:51"
                }
            }

        mock_results_response.return_value = {"success": False, "error": mocked_return_value}

        query = "'SecurityEvent | where IpAddress == '66.76.45'"
        offset = 0
        length = 1
        transmission = stix_transmission.StixTransmission('azure_sentinel_log_analytics', self.connection(), self.config())
        results_response = transmission.results(query, offset, length)

        assert results_response['success'] is False
        assert results_response['error'] == "azure_sentinel_log_analytics connector error => Invalid filter clause"
        assert results_response['code'] == "invalid_parameter"
