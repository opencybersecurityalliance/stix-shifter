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


class GetDSLinksTests(unittest.TestCase):
    def test_get_ds_links_return_values(self):
        conn, config = get_conn_and_config()
        connector = Connector(conn, config)
        deviceId = '269b7894019fdbd5b8f4245f074d6d19e90b71a8'
        fileUniqueId = '32519b85c0b422e4656de6e6c41878e95fd95026267daab4215ee59c107d6c77'
        expected_device_link = 'https://%s/machines/%s/overview' % (
            connector.DEFENDER_HOST, deviceId) if deviceId else None
        expected_file_link = 'https://%s/files/%s/overview' % (
            connector.DEFENDER_HOST, fileUniqueId) if fileUniqueId else None
        expected_res = (expected_device_link, expected_file_link)
        self.assertTupleEqual(connector.get_ds_links(deviceId, fileUniqueId), expected_res, "incorrect result")

    def test_get_ds_links_return_types(self):
        conn, config = get_conn_and_config()
        connector = Connector(conn, config)
        deviceId = '269b7894019fdbd5b8f4245f074d6d19e90b71a8'
        fileUniqueId = '32519b85c0b422e4656de6e6c41878e95fd95026267daab4215ee59c107d6c77'
        self.assertIsInstance(connector.get_ds_links(deviceId, fileUniqueId), tuple, "incorrect result type")


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
        q = '(find withsource = TableName in (DeviceFileEvents) where (FileName =~ "powershell.exe"))'
        q = connector.join_query_with_alerts(q)
        if 'DeviceAlertEvents' not in q or 'DeviceNetworkInfo' not in q or 'DeviceInfo' not in q:
            raise AssertionError("incorrect result")

    def test_get_table_name_return_types(self):
        conn, config = get_conn_and_config()
        connector = Connector(conn, config)
        q=""
        self.assertIsInstance(connector.join_query_with_alerts(q), str, "incorrect result type")