import json
import adal
from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from .api_client import APIClient
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import copy


class Connector(BaseSyncConnector):
    make_alert_as_list = True
    init_error = None
    logger = logger.set_logger(__name__)

    alerts_join_query = ('| join kind=leftouter (DeviceAlertEvents | project ReportId, Timestamp, DeviceName, AlertId, '
                         'Severity, Title, Category, RemoteUrl, RemoteIP, AttackTechniques, Table | where '
                         'Table =~ "{}" | summarize AlertId=make_set(AlertId), Severity=make_set(Severity), '
                         'Title=make_set(Title), Category=make_set('
                         'Category), RemoteUrl=make_set(RemoteUrl), RemoteIP=make_set(RemoteIP),  AttackTechniques=make_set('
                         'AttackTechniques) by DeviceName, ReportId, Timestamp, '
                         'Table) on ReportId, DeviceName, Timestamp')

    device_join_query = ('| join kind=leftouter (DeviceNetworkInfo| project DeviceName, '
                         'MacAddress, IPAddresses, ReportId, Timestamp | summarize MacAddresses=make_set(MacAddress), '
                         'IPAddresses=make_set(IPAddresses) by DeviceName, ReportId, Timestamp) on '
                         'ReportId, DeviceName, Timestamp | join kind=leftouter (DeviceInfo| project DeviceName, '
                         'ReportId, Timestamp, PublicIP, OSPlatform ,OSArchitecture, OSVersion, DeviceType, DeviceId | '
                         'summarize by DeviceName, ReportId, Timestamp, PublicIP, OSPlatform ,OSArchitecture, OSVersion, '
                         'DeviceType, DeviceId) on '
                         'ReportId, DeviceName, Timestamp')

    events_query = ('(find withsource = TableName in ({})  where (DeviceName =~ "{}") and '
                    '(tostring(ReportId) == "{}") and (Timestamp == todatetime("{}")))')

    ALERT_FIELDS = ['AlertId', 'Severity', 'Title', 'Category', 'RemoteUrl', 'RemoteIP', 'AttackTechniques']
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

        finally:
            self.alert_mode = False

    def get_ds_links(self, deviceId=None, fileUniqueId=None):
        device_link = 'https://%s/machines/%s/overview' % (self.DEFENDER_HOST, deviceId) if deviceId else None
        file_link = 'https://%s/files/%s/overview' % (self.DEFENDER_HOST, fileUniqueId) if fileUniqueId else None
        return device_link, file_link

    def join_query_with_alerts(self, query):
        table = Connector.get_table_name(query)
        if 'Alert' in table:
            self.alert_mode = True
        else:
            query += Connector.alerts_join_query.format(table)
            query += Connector.device_join_query
        return query

    @staticmethod
    def remove_duplicate_fields(event_data):
        event = copy.deepcopy(event_data)
        for k in event_data.keys():
            if any(char.isdigit() for char in k) and 'SHA' not in k and 'MD' not in k:
                event.pop(k)
        return event

    def unify_alert_fields(self, event_data):
        techniques_lists = []
        if 'AttackTechniques' in event_data:
            for techniques_lst in event_data['AttackTechniques']:
                attackTechniques = json.loads(techniques_lst)
                techniques_lists.append(attackTechniques)
            event_data['AttackTechniques'] = techniques_lists

        alerts = []
        alerts_count = len(event_data['AlertId']) if not self.alert_mode else 1
        for i in range(alerts_count):
            alert_dct = {k: (event_data[k][i] if len(event_data[k]) > i else '')
                         for k in Connector.ALERT_FIELDS if k in event_data}
            alerts.append(alert_dct)
        event_data['Alerts'] = alerts

        for f in Connector.ALERT_FIELDS:
            event_data.pop(f, None)

        return event_data

    @staticmethod
    def get_table_name(q):
        ind_s = q.find('(', 1)
        ind_e = q.find(')')
        return q[ind_s + 1:ind_e]

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
            joined_query = self.join_query_with_alerts(query)
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
            for event_data in q_return_obj['data']:
                Connector.make_alert_as_list = True
                event_data = Connector.remove_duplicate_fields(event_data)
                lookup_table = event_data['TableName']
                event_data.pop('TableName')
                build_data = dict()
                build_data[lookup_table] = {k: v for k, v in event_data.items() if ((v and v != ['']) or k == "RegistryValueName")}

                # values for query
                table = build_data[lookup_table].get('Table', None)
                deviceName = build_data[lookup_table].get('DeviceName', None)
                reportId = build_data[lookup_table].get('ReportId', None)
                timestamp = build_data[lookup_table].get('Timestamp', None)
                if self.alert_mode and all([table, deviceName, reportId, timestamp]):
                    # query events table according to alert fields
                    joined_query = Connector.events_query.format(table, deviceName, reportId, timestamp)
                    joined_query += Connector.device_join_query
                    response = self.api_client.run_search(joined_query, offset, length)
                    events_return_obj = dict()
                    events_return_obj = self._handle_errors(response, events_return_obj)
                    response_json = json.loads(events_return_obj["data"])
                    events_return_obj['data'] = response_json['Results']
                    # replace the lookup_table with 'table' alert's field, so the to_stix mapping will be
                    # according to 'table' mapping
                    if not events_return_obj['data']:
                        Connector.make_alert_as_list = False
                        if 'AttackTechniques' in build_data[lookup_table]:
                            AttackTechniques_lst = json.loads(build_data[lookup_table]['AttackTechniques'])
                            build_data[lookup_table]['AttackTechniques'] = AttackTechniques_lst
                    else:
                        val = build_data[lookup_table]
                        build_data.pop(lookup_table)
                        build_data[table] = val
                        lookup_table = table
                        event_build_data = dict()
                        event_obj = events_return_obj['data'][0]
                        event_obj = (Connector.remove_duplicate_fields
                                                        (event_obj))
                        event_obj.pop('TableName')
                        merged_alert_event = copy.deepcopy(build_data[table])
                        event_obj = {k:v for k, v in event_obj.items() if v}
                        merged_alert_event.update(event_obj)
                        merged_alert_event = {k: v for k, v in merged_alert_event.items() if v}
                        event_build_data[table] = merged_alert_event
                        build_data = event_build_data

                build_data[lookup_table]['category'] = ''
                build_data[lookup_table]['provider'] = ''
                event_data = copy.deepcopy(build_data[lookup_table])
                device_link, file_link = self.get_ds_links(build_data[lookup_table].get
                                                           ('DeviceId', None),
                                                           build_data[lookup_table].get('InitiatingProcessSHA256',
                                                                                        None))
                if device_link:
                    build_data[lookup_table]['device_link'] = device_link

                if file_link:
                    build_data[lookup_table]['file_link'] = file_link

                if 'AlertId' in build_data[lookup_table] and Connector.make_alert_as_list:
                    build_data[lookup_table] = ({k: ([v] if k in Connector.ALERT_FIELDS and
                                                            self.alert_mode else v) for k, v in
                                                 build_data[lookup_table].items()})
                    build_data[lookup_table] = self.unify_alert_fields(build_data[lookup_table])

                if 'IPAddresses' in build_data[lookup_table]:
                    ips_comp_lst = build_data[lookup_table]['IPAddresses']
                    flat_lst = [ip_obj['IPAddress'] for ip_lst in ips_comp_lst for ip_obj in json.loads(ip_lst) if
                                'IPAddress' in ip_obj]
                    build_data[lookup_table]['IPAddresses'] = flat_lst

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

                lst_len = len(table_event_data)
                table_event_data.insert(lst_len, build_data)

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
