from abc import ABCMeta, abstractmethod


class BaseDeleteConnector(object, metaclass=ABCMeta):
    @abstractmethod
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
