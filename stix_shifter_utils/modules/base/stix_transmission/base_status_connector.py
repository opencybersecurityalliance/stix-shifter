from abc import ABCMeta, abstractmethod
from enum import Enum


class Status(Enum):
    COMPLETED = 'COMPLETED'
    ERROR = 'ERROR'
    CANCELED = 'CANCELED'
    TIMEOUT = 'TIMEOUT'
    RUNNING = 'RUNNING'


class BaseStatusConnector(object, metaclass=ABCMeta):
    @abstractmethod
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
