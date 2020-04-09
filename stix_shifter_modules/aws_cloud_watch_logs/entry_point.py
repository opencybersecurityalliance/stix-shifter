from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from .stix_transmission.aws_cloud_watch_logs_boto3_client import BOTO3Client
from .stix_transmission.aws_cloud_watch_logs_ping_connector import AWSCloudWatchLogsPingConnector
from .stix_transmission.aws_cloud_watch_logs_query_connector import AWSCloudWatchLogsQueryConnector
from .stix_transmission.aws_cloud_watch_logs_status_connector import AWSCloudWatchLogsStatusConnector
from .stix_transmission.aws_cloud_watch_logs_results_connector import AWSCloudWatchLogsResultsConnector
from .stix_transmission.aws_cloud_watch_logs_delete_connector import AWSCloudWatchLogsDeleteConnector

class EntryPoint(EntryPointBase):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(options)

        if connection and configuration:
            boto3_client = BOTO3Client(connection, configuration)
            ping_connector = AWSCloudWatchLogsPingConnector(boto3_client.client)
            query_connector = AWSCloudWatchLogsQueryConnector(boto3_client.client,boto3_client.log_group_names)
            status_connector = AWSCloudWatchLogsStatusConnector(boto3_client.client)
            results_connector = AWSCloudWatchLogsResultsConnector(boto3_client.client)
            delete_connector = AWSCloudWatchLogsDeleteConnector(boto3_client.client)

            self.set_ping_connector(ping_connector)
            self.set_query_connector(query_connector)
            self.set_status_connector(status_connector)
            self.set_results_connector(results_connector)
            self.set_delete_connector(delete_connector)
        else:
            self.setup_translation_simple('guardduty')
