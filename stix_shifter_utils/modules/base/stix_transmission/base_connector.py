from .base_ping import BasePing
from .base_query_connector import BaseQueryConnector
from .base_status_connector import BaseStatusConnector
from .base_delete_connector import BaseDeleteConnector
from .base_results_connector import BaseResultsConnector


class BaseConnector:
    def __init__(self, connection, configuration):
        """
        Args:
            connection (dict): The datasource connection info.
            configuration (dict): The datasource configuration info.
        """
        self.query_connector = BaseQueryConnector()
        self.status_connector = BaseStatusConnector()
        self.delete_connector = BaseDeleteConnector()
        self.results_connector = BaseResultsConnector()
        self.ping_connector = BasePing()

    def create_query_connection(self, query):
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
        return self.query_connector.create_query_connection(query)

    def create_status_connection(self, search_id):
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
        return self.status_connector.create_status_connection(search_id)

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
        return self.results_connector.create_results_connection(search_id, offset, length)

    def delete_query_connection(self, search_id):
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
        return self.delete_connector.delete_query_connection(search_id)

    def ping(self):
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
        return self.ping_connector.ping()
