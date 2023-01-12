from .base_ping_connector import BasePingConnector
from .base_query_connector import BaseQueryConnector
from .base_status_connector import BaseStatusConnector
from .base_delete_connector import BaseDeleteConnector
from .base_results_connector import BaseResultsConnector
import json
import time


class BaseConnector:
    async def create_query_connection(self, query):
        """
        Creates a connection to the specified datasource to send a query

        Args:
            query (str): The datasource query.

        Returns:
            dict: The return value.
                keys:
                    success (bool): True or False
                    search_id (str): query ID
                    error (str): error message (when success=False)
        """
        raise NotImplementedError()

    async def create_status_connection(self, search_id, metadata=None):
        """
        Creates a connection to the specified datasource to determine the status of a given query

        Args:
            search_id (str): The datasource query ID.

        Returns:
            dict: The return value.
                keys:
                    success (bool): True or False
                    status (enum 'Status'): 
                    progress (int): percentage of progress (0-100)
                    error (str): error message (when success=False)
        """
        raise NotImplementedError()

    async def create_results_connection(self, search_id, offset, length, metadata=None):
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

    async def delete_query_connection(self, search_id):
        """
        Deletes a query from the specified datasource

        Args:
            search_id (str): The datasource query ID.

        Returns:
            dict: The return value.
                keys:
                    success (bool): True or False
                    error (str): error message (when success=False)
        """
        raise NotImplementedError()

    async def ping_connection(self):
        """
        Sends a basic request to the datasource to confirm we are connected and authenticated

        Args:
            None.

        Returns:
            dict: The return value.
                keys:
                    success (bool): True or False
                    error (str): error message (when success=False)
        """
        raise NotImplementedError()

    async def create_results_stix_connection(self, entry_point, search_id, offset, length, data_source, metadata=None):
        stats = []
        if metadata:
            result = await entry_point.create_results_connection(search_id, offset, length, metadata)
        else:
            result = await entry_point.create_results_connection(search_id, offset, length)
        stats.append({'action': 'transmission', 'time': int(time.time()*1000)})
        metadata = None
        if 'metadata' in result:            
            metadata = result['metadata']
            del result['metadata']
        if result.get('success'):
            data = result['data']
            data = data[:length]
            result = await entry_point.translate_results(json.dumps(data_source), json.dumps(data))
            stats.append({'action': 'translation', 'time': int(time.time()*1000)})
        result['stats'] = stats
        if metadata:
            result['metadata'] = metadata
        return result
