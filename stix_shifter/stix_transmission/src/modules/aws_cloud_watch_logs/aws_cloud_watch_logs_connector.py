from ..base.base_connector import BaseConnector
from .aws_cloud_watch_logs_ping import AWSCloudWatchLogsPing
from .aws_cloud_watch_logs_query_connector import AWSCloudWatchLogsQueryConnector
from .aws_cloud_watch_logs_status_connector import AWSCloudWatchLogsStatusConnector
from .aws_cloud_watch_logs_delete_connector import AWSCloudWatchLogsDeleteConnector
from .aws_cloud_watch_logs_results_connector import AWSCloudWatchLogsResultsConnector
from .aws_cloud_watch_logs_boto3_client import BOTO3Client


class Connector(BaseConnector):
    def __init__(self, connection, configuration):
        self.boto3_client = BOTO3Client(connection, configuration)
        self.results_connector = AWSCloudWatchLogsResultsConnector(self.boto3_client.client)
        self.status_connector = AWSCloudWatchLogsStatusConnector(self.boto3_client.client)
        self.delete_connector = AWSCloudWatchLogsDeleteConnector(self.boto3_client.client)
        self.query_connector = AWSCloudWatchLogsQueryConnector(self.boto3_client.client,
                                                               self.boto3_client.log_group_names)
        self.ping_connector = AWSCloudWatchLogsPing(self.boto3_client.client)
        self.is_async = True
