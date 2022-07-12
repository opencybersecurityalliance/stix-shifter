from abc import ABCMeta, abstractmethod


class BaseQueryConnector(object, metaclass=ABCMeta):
    @abstractmethod
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
