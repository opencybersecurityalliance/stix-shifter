from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector

class AsyncDummyPingConnector(BasePingConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def ping_connection(self):
        try:
            response = self.api_client.ping_data_source()
            return response
        except Exception as err:
            print('error when pinging datasource {}:'.format(err))
            raise
