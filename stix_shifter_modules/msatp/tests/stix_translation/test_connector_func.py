from stix_shifter_modules.msatp.stix_transmission import connector
from stix_shifter_modules.msatp.stix_transmission.connector import Connector

import unittest


def get_conn_and_config():
    _connection = {
        'host': 'blah',
        'port': 443
    }

    _configuration = {
        'auth': {
            'tenant': 'blah',
            'clientId': 'blah',
            'clientSecret': 'blah'
        }
    }
    return _connection, _configuration


raw_data = {
    "AlertId": ["alert_id_0123456789"],
    "Severity": ["low"],
    "Title": ["blah"],
    "Category": ["blah"],
    "RemoteUrl": ["blah"],
    "RemoteIP": [8080]
}

class UnifyAlertFieldsTests(unittest.TestCase):
    def test_unify_alert_fields_return_values(self):
        conn, config = get_conn_and_config()
        connector = Connector(conn, config)
        ret_data = connector.unify_alert_fields(raw_data)
        if 'Alerts' not in ret_data:
            raise AssertionError("incorrect result")


class GetTableNameTests(unittest.TestCase):
    def test_get_table_name_return_values(self):
        q = '(find withsource = TableName in (DeviceFileEvents) where (FileName =~ "powershell.exe"))'
        table_name = Connector.get_table_name(q)
        if 'Device' not in table_name:
            raise AssertionError("incorrect result")
        self.assertIsInstance(table_name, str, "incorrect result type")


class JoinQueryWithAlertsTests(unittest.TestCase):
    def test_get_table_name_return_values(self):
        conn, config = get_conn_and_config()
        connector = Connector(conn, config)
        query = '(find withsource = TableName in (DeviceFileEvents) where (FileName =~ "powershell.exe"))'
        joined_query = list(connector.join_query_with_alerts(query))
        if not any(('DeviceAlertEvents' or 'DeviceNetworkInfo' or 'DeviceInfo') in q for q in joined_query):
            raise AssertionError("incorrect result")

    def test_get_table_name_return_types(self):
        conn, config = get_conn_and_config()
        connector = Connector(conn, config)
        q=""
        self.assertIsInstance(connector.join_query_with_alerts(q), tuple, "incorrect result type")
