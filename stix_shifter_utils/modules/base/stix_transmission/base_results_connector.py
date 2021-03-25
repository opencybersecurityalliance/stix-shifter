from abc import ABCMeta, abstractmethod
import json


class BaseResultsConnector(object, metaclass=ABCMeta):
    @abstractmethod
    def create_results_connection(self, search_id, offset, length):
        """
        Creates a connection to the specified datasource to retrieve query results

        Args:
            search_id (str): The datasource query ID.
            offset: data offset to start fetch from.
            length: data length to fetch

        Returns:
            dict: The return value.
                keys:
                    success (bool): True or False
                    data (str): The query result data
                    error (str): error message (when success=False)
        """
        raise NotImplementedError()

    def create_results_stix_connection(self, entry_point, search_id, offset, length, data_source):
        result = entry_point.create_results_connection(search_id, offset, length)
        if result and 'success' in result and result['success']:
            result = entry_point.translate_results(data_source, json.dumps(result['data']))
        return result
