from ibmcloudsql import SQLQuery

class APIClient(SQLQuery):
    def __init__(self, connection, configuration):
        auth = configuration.get('auth')
        client_info = configuration.get('client_info')
        instance_crn = connection.get('instance_crn')
        target_cos = connection.get('target_cos')

        super().__init__(auth["bxapikey"], instance_crn, target_cos,
                                client_info=client_info)
        super().logon()