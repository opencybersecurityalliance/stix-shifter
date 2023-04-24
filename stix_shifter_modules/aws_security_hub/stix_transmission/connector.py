from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector

import aioboto3
from json import loads


class Connector(BaseJsonSyncConnector):
    def __init__(self, connection, configuration):
        self.connection = connection
        self.configuration = configuration
        self.session = aioboto3.Session()

    async def ping_connection(self):
        client = await self.session.client('securityhub',
                              aws_access_key_id=self.configuration['aws_access_key_id'],
                              aws_secret_access_key=self.configuration['aws_secret_access_key']
                              )

        return { "success": client.can_paginate('get_findings') }

    async def create_results_connection(self, query_id, offset, length):

        client = await self.session.client('securityhub',
                              aws_access_key_id=self.configuration['aws_access_key_id'],
                              aws_secret_access_key=self.configuration['aws_secret_access_key']
                              )

        filters = None
        if query_id != '':
            filters = loads(query_id)

        findings = client.get_findings(Filters=filters)
        self.results = findings['Findings']

        return { "success": True, "data": self.results }
