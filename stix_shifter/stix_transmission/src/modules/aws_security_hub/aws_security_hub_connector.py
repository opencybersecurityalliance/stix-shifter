from ..base.base_connector import BaseConnector

import boto3
from json import loads


class Connector(BaseConnector):
    def __init__(self, connection, configuration):

        self.is_async = False

        self.connection = connection
        self.configuration = configuration

        self.results_connector = self
        self.query_connector = self
        self.ping_connector = self

    def ping(self):
        client = boto3.client('securityhub',
                              aws_access_key_id=self.configuration['aws_access_key_id'],
                              aws_secret_access_key=self.configuration['aws_secret_access_key']
                              )

        return { "success": client.can_paginate('get_findings') }

    def create_query_connection(self, query):
        return { "success": True, "search_id": query }

    def create_results_connection(self, query_id, offset, length):

        client = boto3.client('securityhub',
                              aws_access_key_id=self.configuration['aws_access_key_id'],
                              aws_secret_access_key=self.configuration['aws_secret_access_key']
                              )

        filters = None
        if query_id != '':
            filters = loads(query_id)

        findings = client.get_findings(Filters=filters)
        self.results = findings['Findings']

        return { "success": True, "data": self.results }
