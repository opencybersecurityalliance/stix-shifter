import json
import re

import adal
from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from .api_client import APIClient
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import copy
from datetime import datetime, timedelta


def merge_alert_events(data):
    """
    msatp has a weird behaviour for some alerts - it returns multiple items of the same alert. all properties
    are identical except: 'FileName', 'SHA1', 'RemoteUrl','RemoteIP'
    this causes one event to be duplicated multiple times with the same alert with hardly any difference
    also - the presence of FileName and SHA1 creates a redundant confusing process object
    to eliminate this - we merge all the alerts that have the same timestamp, device, report title etc
    """
    keys = ['TableName', 'AlertId', 'Timestamp', 'DeviceId', 'DeviceName', 'Severity', 'Category', 'Title',
            'AttackTechniques', 'ReportId']
    alerts = filter(lambda x: x["TableName"] == "DeviceAlertEvents", data)
    non_alerts = filter(lambda x: x["TableName"] != "DeviceAlertEvents", data)
    seen_alerts = set()
    merged_alerts = []
    for alert in alerts:
        key = tuple(alert[k] for k in keys)
        if key not in seen_alerts:
            merged_alerts.append(alert)
            seen_alerts.add(key)
    return merged_alerts + list(non_alerts)


def remove_duplicate_fields(event_data):
    event = copy.deepcopy(event_data)
    for k in event_data.keys():
        if k[-1:].isdigit() and 'SHA' not in k and 'MD' not in k:
            event.pop(k)
    return event


def get_table_name(q):
    regex = r"find withsource = TableName in\s*\(([A-Za-z]+)\s*\)"
    return re.search(regex, q).group(1)


class Connector(BaseJsonSyncConnector):
    init_error = None
    logger = logger.set_logger(__name__)
    make_alert_as_list = True

    events_and_device_info = ('(({}'
                              '| join kind=leftouter {} on DeviceId) '
                              '| where Timestamp1 < Timestamp | summarize arg_max(Timestamp1, *) '
                              'by ReportId, DeviceName, Timestamp) '
                              '| join kind=leftouter {} on DeviceId | where Timestamp2 < Timestamp '
                              '| summarize arg_max(Timestamp2, *) by ReportId, DeviceName, Timestamp')

    events_alerts_and_device_info = ('((({}'
                                     '| join kind=leftouter {} on ReportId, DeviceName, Timestamp)'
                                     '| join kind=leftouter {} on DeviceId) '
                                     '| where Timestamp2 < Timestamp | summarize arg_max(Timestamp2, *) '
                                     'by ReportId, DeviceName, Timestamp) '
                                     '| join kind=leftouter {} on DeviceId | where Timestamp3 < Timestamp '
                                     '| summarize arg_max(Timestamp3, *) by ReportId, DeviceName, Timestamp')

    events_alerts_query = '({} | join kind=leftouter {} on ReportId, DeviceName, Timestamp)'

    events_query = ('(find withsource = TableName in ({})  where (Timestamp == datetime({})) '
                    'and (DeviceName == "{}") and (ReportId == {}))')

    alerts_query = (
        '(DeviceAlertEvents | summarize AlertId=make_list(AlertId), Severity=make_list(Severity), '
        'Title=make_list(Title), Category=make_list('
        'Category), AttackTechniques=make_list('
        'AttackTechniques) by DeviceName, ReportId, Timestamp)')

    network_info_query = (
        '(DeviceNetworkInfo | where NetworkAdapterStatus == "Up" | project Timestamp, DeviceId, MacAddress, IPAddresses| summarize '
        'IPAddressesSet=make_set(IPAddresses), MacAddressSet=make_set(MacAddress) by '
        'DeviceId, Timestamp)')

    device_info_query = '(DeviceInfo | project Timestamp, DeviceId, PublicIP, OSArchitecture, OSPlatform, OSVersion)'

    EVENTS_TABLES = ['DeviceNetworkEvents', 'DeviceProcessEvents', 'DeviceFileEvents', 'DeviceRegistryEvents',
                     'DeviceEvents', 'DeviceImageLoadEvents']
    ALERT_FIELDS = ['AlertId', 'Severity', 'Title', 'Category', 'AttackTechniques']
    DEFENDER_HOST = 'security.microsoft.com'

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        self.connector = __name__.split('.')[1]
        self.alert_mode = False
        self.adal_response = Connector.generate_token(self, connection, configuration)
        if self.adal_response['success']:
            configuration['auth']['access_token'] = self.adal_response['access_token']
            self.api_client = APIClient(connection, configuration)
        else:
            self.init_error = True

    def join_query_with_alerts(self, query):
        table = get_table_name(query)
        if 'Alert' in table:
            self.alert_mode = True
            full_query = query
            partial_query = None

        else:
            alerts_query = Connector.alerts_query.format(table)
            full_query = Connector.events_alerts_and_device_info.format(query,
                                                                        alerts_query,
                                                                        Connector.network_info_query,
                                                                        Connector.device_info_query)
            partial_query = Connector.events_alerts_query.format(query,
                                                                 alerts_query)
        return full_query, partial_query

    def unify_alert_fields(self, event_data):
        techniques_lists = []
        if 'AttackTechniques' in event_data:
            for techniques_lst in event_data['AttackTechniques']:
                try:
                    attackTechniques = json.loads(techniques_lst)
                except json.decoder.JSONDecodeError:
                    attackTechniques = ''
                finally:
                    techniques_lists.append(attackTechniques)
            event_data['AttackTechniques'] = techniques_lists

        alerts = []
        alerts_count = len(event_data['AlertId']) if not self.alert_mode else 1
        for i in range(alerts_count):
            alert_dct = {k: (event_data[k][i] if len(event_data[k]) > i else '')
                         for k in Connector.ALERT_FIELDS if k in event_data}
            if alert_dct['AlertId'] not in [alert['AlertId'] for alert in alerts]:
                alerts.append(alert_dct)
        event_data['Alerts'] = alerts

        for f in Connector.ALERT_FIELDS:
            event_data.pop(f, None)

        return event_data

    def _handle_errors(self, response, return_obj):
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
            ErrorResponder.fill_error(return_obj, message=response_txt, connector=self.connector)
            raise Exception(return_obj)
        elif ErrorResponder.is_json_string(response_txt):
            response_json = json.loads(response_txt)
            ErrorResponder.fill_error(return_obj, response_json, ['reason'], connector=self.connector)
            raise Exception(return_obj)
        else:
            raise Exception(return_obj)

    async def ping_connection(self):
        """Ping the endpoint."""
        return_obj = dict()
        if self.init_error:
            return self.adal_response
        response = await self.api_client.ping_box()
        response_code = response.code
        if 200 <= response_code < 300:
            return_obj['success'] = True
        else:
            ErrorResponder.fill_error(return_obj, message='unexpected exception', connector=self.connector)
        return return_obj

    async def delete_query_connection(self, search_id):
        """"delete_query_connection response
        :param search_id: str, search_id"""
        return {"success": True, "search_id": search_id}

    async def create_results_connection(self, query, offset, length):
        """"built the response object
        :param query: str, search_id
        :param offset: int,offset value
        :param length: int,length value"""

        response_txt = None
        return_obj = dict()

        try:
            if self.init_error:
                return self.adal_response
            q_return_obj = dict()
            joined_query, partial_query = self.join_query_with_alerts(query)
            response = await self.api_client.run_search(joined_query, offset, length)
            q_return_obj = self._handle_errors(response, q_return_obj)
            response_json = json.loads(q_return_obj["data"])
            q_return_obj['data'] = response_json['Results']

            """ if one of the last 2 joins reset the results, search events and findings only
                without querying the networkInfo/DeviceInfo tables """
            if not q_return_obj['data'] and not self.alert_mode:
                partial_return_obj = dict()
                joined_query = partial_query
                response = await self.api_client.run_search(joined_query, offset, length)
                partial_return_obj = self._handle_errors(response, partial_return_obj)
                response_json = json.loads(partial_return_obj["data"])
                partial_return_obj['data'] = response_json['Results']
                q_return_obj['data'] = partial_return_obj['data']
            # Customizing the output json,
            # Get 'TableName' attribute from each row of event data
            # Create a dictionary with 'TableName' as key and other attributes in an event data as value
            # Filter the "None" and empty values except for RegistryValueName, which support empty string
            # Customizing of Registryvalues json
            table_event_data = []
            # for some reason sometimes msatp returns the same alert from DeviceAlertEvents multiple times.
            # they only differ in the RemoteIp, RemoteUrl, FileName and SHA1 properties, which are redundant anyway
            # because they appear in the event as well. They are even wrongly referenced in the alert. for example the
            # localip appears as RemoteIp. so we merge all these alerts into one.
            q_return_obj['data'] = merge_alert_events(q_return_obj['data'])
            for event_data in q_return_obj['data']:
                lookup_table = event_data['TableName']
                event_data.pop('TableName')
                build_data = dict()
                build_data[lookup_table] = {k: v for k, v in event_data.items() if v or k == "RegistryValueName"}
                # values for query
                table = build_data[lookup_table].get('Table', None)
                deviceName = build_data[lookup_table].get('DeviceName', None)
                reportId = build_data[lookup_table].get('ReportId', None)
                timestamp = build_data[lookup_table].get('Timestamp', None)

                if self.alert_mode and table not in Connector.EVENTS_TABLES:
                    Connector.make_alert_as_list = False
                    if 'AttackTechniques' in build_data[lookup_table]:
                        attackTechniques = json.loads(build_data[lookup_table]['AttackTechniques'])
                        build_data[lookup_table]['AttackTechniques'] = attackTechniques

                elif self.alert_mode and all([deviceName, reportId, timestamp]):
                    # query events table according to alert fields
                    found_events = True
                    events_query = "union {}".format(','.join(
                        [Connector.events_query.format(q, timestamp, deviceName, reportId) for q in
                         Connector.EVENTS_TABLES]))
                    joined_query = Connector.events_and_device_info.format(events_query,
                                                                           Connector.network_info_query,
                                                                           Connector.device_info_query)
                    print("joining alert with events: ", joined_query)
                    response = await self.api_client.run_search(joined_query, offset, length)
                    events_return_obj = dict()
                    events_return_obj = self._handle_errors(response, events_return_obj)
                    response_json = json.loads(events_return_obj["data"])
                    events_return_obj['data'] = response_json['Results']
                    # replace the lookup_table with 'table' alert's field, so the to_stix mapping will be
                    # according to 'table' mapping
                    if not events_return_obj['data']:
                        response = await self.api_client.run_search(events_query, offset, length)
                        events_return_obj = dict()
                        events_return_obj = self._handle_errors(response, events_return_obj)
                        response_json = json.loads(events_return_obj["data"])
                        events_return_obj['data'] = response_json['Results']

                        if not events_return_obj['data']:
                            Connector.make_alert_as_list, found_events = False, False
                            if 'AttackTechniques' in build_data[lookup_table]:
                                attackTechniques = json.loads(build_data[lookup_table]['AttackTechniques'])
                                build_data[lookup_table]['AttackTechniques'] = attackTechniques

                    if found_events:
                        val = build_data[lookup_table]
                        build_data.pop(lookup_table)
                        build_data[table] = val
                        lookup_table = table
                        event_build_data = dict()
                        event_obj = events_return_obj['data'][0]
                        event_obj = (remove_duplicate_fields(event_obj))
                        event_obj.pop('TableName')
                        merged_alert_event = copy.deepcopy(build_data[table])
                        event_obj = {k: v for k, v in event_obj.items() if v}
                        merged_alert_event.update(event_obj)
                        merged_alert_event = {k: v for k, v in merged_alert_event.items() if v and v != ['']}
                        event_build_data[table] = merged_alert_event
                        build_data = event_build_data

                build_data[lookup_table]['category'] = ''
                build_data[lookup_table]['provider'] = ''
                event_data = copy.deepcopy(build_data[lookup_table])

                # link the event to ms atp console device timeline with one second before and after the event https://security.microsoft.com/machines/<MachineId>/timeline?from=<start>&to=<end>
                try:
                    if 'DeviceId' in build_data[lookup_table]:
                        timestamp_dt = datetime.strptime(timestamp[:-9],
                                                         "%Y-%m-%dT%H:%M:%S")  # parse timestamp to date opbject striping nanoseconds
                        timeline_start = (timestamp_dt - timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%S") + ".000Z"
                        timeline_end = (timestamp_dt + timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%S") + ".000Z"
                        event_link = 'https://%s/machines/%s/timeline?from=%s&to=%s' % (
                            self.DEFENDER_HOST, build_data[lookup_table].get('DeviceId'), timeline_start, timeline_end)
                        build_data[lookup_table]['event_link'] = event_link
                except Exception as ex:
                    self.logger.error(
                        "error while parsing event_link (external ref) from event. this error does not stop translation {}".format(
                            str(ex)))

                if 'AlertId' in build_data[lookup_table] and Connector.make_alert_as_list:
                    build_data[lookup_table] = ({k: ([v] if k in Connector.ALERT_FIELDS and
                                                            self.alert_mode else v) for k, v in
                                                 build_data[lookup_table].items()})
                    build_data[lookup_table] = self.unify_alert_fields(build_data[lookup_table])

                if 'IPAddressesSet' in build_data[lookup_table]:
                    ips_comp_lst = build_data[lookup_table].pop('IPAddressesSet')
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
                # handle two different type of process events: ProcessCreate, OpenProcess
                if lookup_table == "DeviceProcessEvents":
                    process_fields = ["ProcessId", "ProcessCommandLine", "ProcessCreationTime", "AccountSid",
                                      "AccountName"]
                    event_type = build_data[lookup_table]['ActionType']
                    # prefix = 'Created' if event_type == 'ProcessCreated' else 'Opened'
                    # # rename fields in order to map differently events of different types
                    # build_data[lookup_table] = {(prefix + k if k in process_fields else k): v
                    #                             for k, v in build_data[lookup_table].items()}
                if lookup_table == "DeviceEvents":
                    if 'ProcessId' not in build_data[lookup_table] or build_data[lookup_table]['ProcessId'] is None or \
                            build_data[lookup_table]['ProcessId'] == "":
                        build_data[lookup_table]["_missingChildShouldMapInitiatingPid"] = "true"

                build_data[lookup_table]['event_count'] = '1'
                build_data[lookup_table]['original_ref'] = json.dumps(event_data)

                self.remove_duplicate_ips(build_data, lookup_table)

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
                ErrorResponder.fill_error(return_obj, message='unexpected exception', connector=self.connector)
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise ex

    def remove_duplicate_ips(self, build_data, lookup_table):
        ## remove duplicate ips between LocalIP, PublicIP and IPAddresses:
        if 'PublicIP' in build_data[lookup_table] and 'LocalIP' in build_data[lookup_table] and \
                build_data[lookup_table]['PublicIP'] == build_data[lookup_table]['LocalIP']:
            build_data[lookup_table].pop('PublicIP')
        self.remove_duplicate_ips_from(build_data, lookup_table, 'LocalIP')
        self.remove_duplicate_ips_from(build_data, lookup_table, 'PublicIP')

    def remove_duplicate_ips_from(self, build_data, lookup_table, prop_name):
        if 'IPAddresses' in build_data[lookup_table] and prop_name in build_data[lookup_table]:
            filtered = [x for x in build_data[lookup_table]['IPAddresses'] if
                        not x == build_data[lookup_table][prop_name]]
            if len(filtered) > 0:
                build_data[lookup_table]['IPAddresses'] = filtered
            else:
                build_data[lookup_table].pop('IPAddresses')

    def generate_token(self, connection, configuration):
        """To generate the Token
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        return_obj = dict()

        authority_url = ('https://login.windows.net/' +
                         configuration['auth']['tenant'])
        resource = "https://" + str(connection.get('host'))

        try:
            context = adal.AuthenticationContext(
                authority_url, validate_authority=configuration['auth']['tenant'] != 'adfs',
            )
            response_dict = context.acquire_token_with_client_credentials(
                resource,
                configuration['auth']['clientId'],
                configuration['auth']['clientSecret'])

            return_obj['success'] = True
            return_obj['access_token'] = response_dict['accessToken']
        except Exception as ex:
            if ex.__class__.__name__ == 'AdalError':
                response_dict = ex.error_response
                ErrorResponder.fill_error(return_obj, response_dict, ['error_description'], connector=self.connector)
            else:
                ErrorResponder.fill_error(return_obj, message=str(ex), connector=self.connector)
            Connector.logger.error("Token generation Failed: " + str(ex.error_response))

        return return_obj
