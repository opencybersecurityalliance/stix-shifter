import json
import adal
from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from .api_client import APIClient
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import copy


class Connector(BaseSyncConnector):
    init_error = None
    logger = logger.set_logger(__name__)

    join_query = '| join kind=leftouter (DeviceAlertEvents | where Table =~ "{}") on ' \
                 'ReportId, $left.ReportId == $right.ReportId | join kind=leftouter (DeviceNetworkInfo | ' \
                 'distinct DeviceId, MacAddress) on DeviceId, $left.DeviceId == $right.DeviceId | join ' \
                 'kind=leftouter (DeviceInfo | distinct PublicIP, OSPlatform ,OSArchitecture, OSVersion , ' \
                 'DeviceType, DeviceId) on DeviceId, $left.DeviceId == $right.DeviceId'

    ALERT_FIELDS = ['Severity', 'FileName', 'Title', 'SHA1', 'Category', 'RemoteUrl', 'RemoteIP', 'AttackTechniques']
    ALERT_FIELDS_IGNORE = ['DeviceId', 'DeviceName', 'ReportId', 'Timestamp']
    DEFENDER_HOST = 'security.microsoft.com'

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""

        try:
            self.token = Connector.generate_token(connection, configuration)
            configuration['auth']['access_token'] = self.token
            self.api_client = APIClient(connection, configuration)

        except Exception as ex:
            self.init_error = ex

    def get_ds_links(self, deviceId=None, fileUniqueId=None):
        device_link = 'https://%s/machines/%s/overview' % (self.DEFENDER_HOST, deviceId) if deviceId else None
        file_link = 'https://%s/files/%s/overview' % (self.DEFENDER_HOST, fileUniqueId) if fileUniqueId else None
        return device_link, file_link

    @staticmethod
    def unify_alert_fields(event_data):
        if 'AttackTechniques' in event_data:
            AttackTechniques_lst = json.loads(event_data['AttackTechniques'])
            event_data['AttackTechniques'] = AttackTechniques_lst

        alert_dct = {}
        for field in Connector.ALERT_FIELDS:
            re_field = ''.join([field, '1'])
            if re_field in event_data:
                val = event_data[re_field]
                event_data.pop(re_field)
                alert_dct['alert_' + field] = val
            elif field in event_data:
                val = event_data[field]
                event_data.pop(field)
                alert_dct['alert_' + field] = val

        for field in Connector.ALERT_FIELDS_IGNORE:
            if ''.join([field, '1']) in event_data:
                event_data.pop(''.join([field, '1']))

        alert = [alert_dct]
        event_data['Alerts'] = alert

        return event_data

    @staticmethod
    def get_table_name(q):
        ind_s = q.find('(', 1)
        ind_e = q.find(')')
        return q[ind_s + 1:ind_e]

    @staticmethod
    def join_query_with_alerts(query):
        table = Connector.get_table_name(query)
        join_query = Connector.join_query.format(table)
        query += join_query
        return query

    @staticmethod
    def _handle_errors(response, return_obj):
        """Handling API error response
        :param response: response for the API
        :param return_obj: dict, response for the API call with status
        """
        response_code = response.code
        response_txt = response.read().decode('utf-8')

        if 200 <= response_code < 300:
            return_obj['success'] = True
            return_obj['data'] = response_txt
            return return_obj
        elif ErrorResponder.is_plain_string(response_txt):
            ErrorResponder.fill_error(return_obj, message=response_txt)
            raise Exception(return_obj)
        elif ErrorResponder.is_json_string(response_txt):
            response_json = json.loads(response_txt)
            ErrorResponder.fill_error(return_obj, response_json, ['reason'])
            raise Exception(return_obj)
        else:
            raise Exception(return_obj)

    def ping_connection(self):
        """Ping the endpoint."""
        return_obj = dict()
        if self.init_error:
            raise self.init_error
        response = self.api_client.ping_box()
        response_code = response.code
        if 200 <= response_code < 300:
            return_obj['success'] = True
        else:
            ErrorResponder.fill_error(return_obj, message='unexpected exception')
        return return_obj

    def delete_query_connection(self, search_id):
        """"delete_query_connection response
        :param search_id: str, search_id"""
        return {"success": True, "search_id": search_id}

    def create_results_connection(self, query, offset, length):
        """"built the response object
        :param query: str, search_id
        :param offset: int,offset value
        :param length: int,length value"""
        response_txt = None
        return_obj = dict()

        try:
            if self.init_error:
                raise self.init_error
            q_return_obj = dict()
            joined_query = Connector.join_query_with_alerts(query)
            response = self.api_client.run_search(joined_query, offset, length)
            q_return_obj = self._handle_errors(response, q_return_obj)
            response_json = json.loads(q_return_obj["data"])
            q_return_obj['data'] = response_json['Results']
            # Customizing the output json,
            # Get 'TableName' attribute from each row of event data
            # Create a dictionary with 'TableName' as key and other attributes in an event data as value
            # Filter the "None" and empty values except for RegistryValueName, which support empty string
            # Customizing of Registry values json
            table_event_data = []
            unify_events_dct = {}
            for event_data in q_return_obj['data']:
                lookup_table = event_data['TableName']
                event_data.pop('TableName')
                build_data = dict()
                build_data[lookup_table] = {k: v for k, v in event_data.items() if v or k == "RegistryValueName"}
                DeviceId = build_data[lookup_table].get('DeviceId', None)
                SHA256 = build_data[lookup_table].get('InitiatingProcessSHA256', None)
                device_link, file_link = self.get_ds_links(DeviceId, SHA256)
                build_data[lookup_table]['device_link'] = device_link
                build_data[lookup_table]['file_link'] = file_link

                # if there is an alarm ref, unify all the information about the alarm to custom fields
                if 'AlertId' in build_data[lookup_table]:
                    build_data[lookup_table] = Connector.unify_alert_fields(build_data[lookup_table])
                else:
                    build_data[lookup_table]['Alerts'] = []

                if lookup_table == "DeviceNetworkInfo":
                    for k, v in build_data[lookup_table].items():
                        if k == 'IPAddresses':
                            ip_addresses_lst = list()
                            arr = json.loads(v)
                            for obj in arr:
                                if 'IPAddress' in obj:
                                    ip_addresses_lst.append(obj['IPAddress'])
                            build_data[lookup_table]['IPAddresses'] = ip_addresses_lst

                if lookup_table == "DeviceRegistryEvents":
                    registry_build_data = copy.deepcopy(build_data)
                    registry_build_data[lookup_table]["RegistryValues"] = []
                    registry_value_dict = {}
                    for k, v in build_data[lookup_table].items():
                        if k in ["RegistryValueData", "RegistryValueName", "RegistryValueType"]:
                            registry_value_dict.update({k: v})
                            registry_build_data[lookup_table].pop(k)
                    registry_build_data[lookup_table]["RegistryValues"].append(registry_value_dict)

                    build_data[lookup_table] = registry_build_data[lookup_table]

                build_data[lookup_table]['event_count'] = '1'
                build_data[lookup_table]['original_ref'] = json.dumps(event_data)

                k_tuple = (
                    build_data[lookup_table].get('DeviceName', None),
                    build_data[lookup_table].get('ReportId', None),
                    build_data[lookup_table].get('Timestamp', None))
                # if the same event already exists on the table_event_data, just update 'Alerts' field
                if k_tuple in unify_events_dct:
                    alerts = build_data[lookup_table]['Alerts']
                    ind = unify_events_dct[k_tuple]
                    for alert in alerts:
                        if alert not in table_event_data[ind][lookup_table]['Alerts']:
                            table_event_data[ind][lookup_table]['Alerts'].append(alert)
                else:
                    lst_len = len(table_event_data)
                    table_event_data.insert(lst_len, build_data)
                    unify_events_dct[k_tuple] = lst_len

            if 'data' in return_obj.keys():
                return_obj['data'].extend(table_event_data)
            else:
                return_obj['data'] = table_event_data

            return_obj['success'] = True
            return return_obj

        except Exception as ex:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception')
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise ex

    @staticmethod
    def generate_token(connection, configuration):
        """To generate the Token
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""

        authority_url = ('https://login.windows.net/' +
                         configuration['auth']['tenant'])
        resource = "https://" + str(connection.get('host'))

        try:
            context = adal.AuthenticationContext(
                authority_url, validate_authority=configuration['auth']['tenant'] != 'adfs',
            )
            token = context.acquire_token_with_client_credentials(
                resource,
                configuration['auth']['clientId'],
                configuration['auth']['clientSecret'])

            token_value = token['accessToken']
            return token_value

        except Exception as ex:
            return_obj = dict()
            if ex.error_response:
                ErrorResponder.fill_error(return_obj, ex.error_response, ['reason'])
                Connector.logger.error("Token generation Failed: " + return_obj)
            raise ex
