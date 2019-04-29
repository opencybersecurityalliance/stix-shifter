from stix_shifter.stix_transmission.src.modules.elastic_ecs import elastic_ecs_connector
from unittest.mock import patch
import unittest
import json
import os
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter.utils.error_response import ErrorCode


class ElasticEcsMockResponse:
    def __init__(self, response_code, object):
        self.code = response_code
        self.object = object

    def read(self):
        return bytearray(self.object, 'utf-8')


@patch('stix_shifter.stix_transmission.src.modules.elastic_ecs.api_client.APIClient.__init__',  autospec=True)
class TestElasticEcsConnection(unittest.TestCase, object):
    def test_is_async(self, mock_api_client):
        mock_api_client.return_value = None
        module = elastic_ecs_connector

        config = {
            "auth": {
                "SEC": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": "8080",
            "ceft": "cert"
        }

        check_async = module.Connector(connection, config).is_async

        assert check_async is False

    @patch('stix_shifter.stix_transmission.src.modules.elastic_ecs.api_client.APIClient.ping_box')
    def test_ping_endpoint(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '["mock", "placeholder"]'

        mock_ping_response.return_value = ElasticEcsMockResponse(200, mocked_return_value)

        config = {
            "auth": {
                "SEC": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": "8080",
            "ceft": "cert"
        }

        transmission = stix_transmission.StixTransmission('elastic_ecs', connection, config)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success']

    @patch('stix_shifter.stix_transmission.src.modules.elastic_ecs.api_client.APIClient.ping_box')
    def test_ping_endpoint_exception(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '["mock", "placeholder"]'
        mock_ping_response.return_value = ElasticEcsMockResponse(200, mocked_return_value)
        mock_ping_response.side_effect = Exception('exception')
        config = {
            "auth": {
                "SEC": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": "8080",
            "ceft": "cert"
        }

        transmission = stix_transmission.StixTransmission('elastic_ecs', connection, config)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == ErrorCode.TRANSMISSION_UNKNOWN.value

    def test_query_response(self, mock_api_client):
        mock_api_client.return_value = None

        config = {
            "auth": {
                "SEC": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": "8080",
            "ceft": "cert"
        }

        query = '(source.port : "64966" OR client.port : "64966")'
        transmission = stix_transmission.StixTransmission('elastic_ecs', connection, config)
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == query

    @patch('stix_shifter.stix_transmission.src.modules.elastic_ecs.api_client.APIClient.run_search',
           autospec=True)
    def test_results_response(self, mock_results_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = """ {
                    "hits" : {
                        "total" : {
                            "value" : 5,
                            "relation" : "eq"
                        },
                        "max_score" : 3.0,
                        "hits" : [
                            {
                            "_source":   {
                            "@timestamp": "2019-04-12T12:41:07.237Z", 
                            "client": {
                                "port": 64966, 
                                "bytes": 39, 
                                "ip": "0.0.0.0"
                            }, 
                            "source": {
                                "port": 64966, 
                                "bytes": 39, 
                                "ip": "0.0.0.0"
                            }, 
                            "event": {
                                "duration": 96890000, 
                                "kind": "event", 
                                "start": "2019-04-12T12:41:07.237Z", 
                                "end": "2019-04-12T12:41:07.334Z", 
                                "category": "network_traffic", 
                                "dataset": "dns"
                            }
                            }
                        }
                    ]
                }
            } """
        mock_results_response.return_value = ElasticEcsMockResponse(200, mocked_return_value)

        config = {
            "auth": {
                "SEC": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": "8080",
            "ceft": "cert"
        }

        search_id = '(source.port : "64966" OR client.port : "64966")'
        offset = 0
        length = 1
        transmission = stix_transmission.StixTransmission('elastic_ecs', connection, config)
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert results_response['success']
        assert 'data' in results_response
        assert len(results_response['data']) > 0

    @patch('stix_shifter.stix_transmission.src.modules.elastic_ecs.api_client.APIClient.run_search',
           autospec=True)
    def test_results_response_exception(self, mock_results_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = """ {    } """
        mock_results_response.return_value = ElasticEcsMockResponse(404, mocked_return_value)

        config = {
            "auth": {
                "SEC": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": "8080",
            "ceft": "cert"
        }

        search_id = '(source.port : "64966" OR client.port : "64966")'
        offset = 0
        length = 1
        transmission = stix_transmission.StixTransmission('elastic_ecs', connection, config)
        results_response = transmission.results(search_id, offset, length)

        assert results_response['code'] == 'unknown'
        assert results_response['success'] is False


    @patch('stix_shifter.stix_transmission.src.modules.elastic_ecs.api_client.APIClient.run_search',
           autospec=True)
    def test_query_flow(self, mock_results_response, mock_api_client):
        mock_api_client.return_value = None
        results_mock = """ {
                    "hits" : {
                        "total" : {
                            "value" : 5,
                            "relation" : "eq"
                        },
                        "max_score" : 3.0,
                        "hits" : [
                            {
                            "_source":   {
                            "@timestamp": "2019-04-12T12:41:07.237Z", 
                            "client": {
                                "port": 64966, 
                                "bytes": 39, 
                                "ip": "0.0.0.0"
                            }, 
                            "source": {
                                "port": 64966, 
                                "bytes": 39, 
                                "ip": "0.0.0.0"
                            }, 
                            "event": {
                                "duration": 96890000, 
                                "kind": "event", 
                                "start": "2019-04-12T12:41:07.237Z", 
                                "end": "2019-04-12T12:41:07.334Z", 
                                "category": "network_traffic", 
                                "dataset": "dns"
                            }
                            }
                        }
                    ]
                }
            } """

        mock_results_response.return_value = ElasticEcsMockResponse(200, results_mock)
        module = elastic_ecs_connector

        config = {
            "auth": {
                "SEC": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": "8080",
            "ceft": "cert"
        }

        query = '(source.port : "64966" OR client.port : "64966")'

        transmission = stix_transmission.StixTransmission('elastic_ecs', connection, config)
        query_response = transmission.query(query)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == '(source.port : "64966" OR client.port : "64966")'

        offset = 0
        length = 1
        results_response = module.Connector(connection, config).create_results_connection(query, offset, length)

        assert results_response is not None
        assert 'data' in results_response
        assert len(results_response['data']) > 0
