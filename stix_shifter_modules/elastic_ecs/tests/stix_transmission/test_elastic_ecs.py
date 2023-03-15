from stix_shifter_modules.elastic_ecs.entry_point import EntryPoint
from stix_shifter_modules.elastic_ecs.stix_transmission.connector import UnexpectedResponseException
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from stix_shifter_utils.utils.error_response import ErrorCode
from tests.utils.async_utils import get_mock_response


from unittest.mock import patch
import unittest


class TestElasticEcsConnection(unittest.TestCase, object):
    def test_is_async(self):
        entry_point = EntryPoint()
        check_async = entry_point.is_async()

        assert check_async is False

    @patch('stix_shifter_modules.elastic_ecs.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_endpoint(self, mock_ping_response):
        mocked_return_value = '["mock", "placeholder"]'

        mock_ping_response.return_value = get_mock_response(200, mocked_return_value, 'byte')

        config = {
            "auth": {
                "username": "bla",
                "password": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": 8080,
            "selfSignedCert": "cert",
            "indices": "index1,index2"
        }

        transmission = stix_transmission.StixTransmission('elastic_ecs', connection, config)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success']

    @patch('stix_shifter_modules.elastic_ecs.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_endpoint_exception(self, mock_ping_response):
        mock_ping_response.side_effect = UnexpectedResponseException('exception')
        config = {
            "auth": {
                "username": "bla",
                "password": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": 8080,
            "selfSignedCert": "cert",
            "indices": "index1"
        }

        ping_response = None

        transmission = stix_transmission.StixTransmission('elastic_ecs', connection, config)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == ErrorCode.TRANSMISSION_UNKNOWN.value


    def test_query_response(self):
        config = {
            "auth": {
                "username": "bla",
                "password": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": 8080,
            "selfSignedCert": "cert",
            "indices": "index1,index2"
        }

        query = '(source.port : "64966" OR client.port : "64966")'
        transmission = stix_transmission.StixTransmission('elastic_ecs', connection, config)
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == query

    @patch('stix_shifter_modules.elastic_ecs.stix_transmission.api_client.APIClient.search_pagination', autospec=True)
    def test_results_response(self, mock_results_response):
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
                            },
                            "sort": [1555072867]
                        }
                    ]
                }
            } """
        mock_results_response.return_value = get_mock_response(200, mocked_return_value, 'byte')

        config = {
            "auth": {
                "username": "bla",
                "password": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": 8080,
            "selfSignedCert": "cert",
            "indices": "index1,index2"
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
        assert len(results_response['metadata']) >= 1

    @patch('stix_shifter_modules.elastic_ecs.stix_transmission.api_client.APIClient.search_pagination', autospec=True)
    def test_results_response_exception(self, mock_results_response):
        mocked_return_value = """ {    } """
        mock_results_response.return_value = get_mock_response(404, mocked_return_value, 'byte')

        config = {
            "auth": {
                "username": "bla",
                "password": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": 8080,
            "selfSignedCert": "cert",
            "indices": ""
        }

        search_id = '(source.port : "64966" OR client.port : "64966")'
        offset = 0
        length = 1
        transmission = stix_transmission.StixTransmission('elastic_ecs', connection, config)
        results_response = transmission.results(search_id, offset, length)

        assert results_response['code'] == 'unknown'
        assert results_response['success'] is False


    @patch('stix_shifter_modules.elastic_ecs.stix_transmission.api_client.APIClient.search_pagination', autospec=True)
    def test_query_flow(self, mock_results_response):
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
                            },
                            "sort": [1555072867]
                        }
                    ]
                }
            } """

        mock_results_response.return_value = get_mock_response(200, results_mock, 'byte')

        config = {
            "auth": {
                "username": "bla",
                "password": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": 8080,
            "selfSignedCert": "cert"
        }

        query = '(source.port : "64966" OR client.port : "64966")'

        transmission = stix_transmission.StixTransmission('elastic_ecs', connection, config)
        query_response = transmission.query(query)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == '(source.port : "64966" OR client.port : "64966")'

        offset = 0
        length = 1
        results_response = transmission.results(query_response['search_id'], offset, length)

        assert results_response is not None
        assert 'data' in results_response
        assert len(results_response['data']) > 0
        assert len(results_response['metadata']) >= 1


    @patch('stix_shifter_modules.elastic_ecs.stix_transmission.api_client.APIClient.get_max_result_window', autospec=True)
    def test_pagesize(self, mock_results_response):
        mocked_return_value = """ {
                "index1": {
                  "settings": {
                    "index": {
                      "creation_date": "1676581113776"
                    }
                  },
                  "defaults": {
                    "index": {
                      "max_result_window": "20000"
                    }
                  }
                },
                "index2": {
                  "settings": {
                    "index": {
                      "max_result_window": "30000",
                      "creation_date": "1676580367477"
                    }
                  },
                  "defaults": {
                    "index": {
                    }
                  }
                }
            } """
        mock_results_response.return_value = get_mock_response(200, mocked_return_value, 'byte')

        config = {
            "auth": {
                "username": "bla",
                "password": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": 8080,
            "selfSignedCert": "cert",
            "indices": "index1,index2"
        }

        transmission = stix_transmission.StixTransmission('elastic_ecs', connection, config)
        search_id = '(source.port : "64966" OR client.port : "64966")'
        offset = 0
        length = 1
        results_response = transmission.results(search_id, offset, length)
        max_result_window = transmission.entry_point._BaseEntryPoint__results_connector.max_result_window

        assert max_result_window == 20000

    @patch('stix_shifter_modules.elastic_ecs.stix_transmission.api_client.APIClient.get_max_result_window')
    def test_pagesize_exception(self, mock_result_response):
        mocked_return_value = '["mock", "placeholder"]'
        mock_result_response.return_value = get_mock_response(200, mocked_return_value, 'byte')
        mock_result_response.side_effect = Exception('exception')
        config = {
            "auth": {
                "username": "bla",
                "password": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": 8080,
            "selfSignedCert": "cert",
            "indices": "index1"
        }

        transmission = stix_transmission.StixTransmission('elastic_ecs', connection, config)
        search_id = '(source.port : "64966" OR client.port : "64966")'
        offset = 0
        length = 1
        results_response = transmission.results(search_id, offset, length)
        max_result_window = transmission.entry_point._BaseEntryPoint__results_connector.max_result_window
        assert max_result_window == 10000