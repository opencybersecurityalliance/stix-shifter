from abc import ABCMeta, abstractmethod


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
