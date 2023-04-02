import json
import re

import adal
from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from .api_client import APIClient
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import copy
from datetime import datetime, timedelta


def merge_alerts(data):
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


def remove_duplicate_and_empty_fields(event_data):
    unique_values = set()
    # remove timestamps from joins of device network info and device info
    event_data.pop("DNI_TS", None)
    event_data.pop("DI_TS", None)
    copied = copy.deepcopy(event_data)
    # remove None's empty strings and duplicates from joins such as DeviceId2, DeviceId3 etc
    for key, value in copied.items():
        if key in unique_values or value is None or value == '' \
                or (key[-1:].isdigit() and 'SHA' not in key and 'MD' not in key):
            event_data.pop(key)
        else:
            unique_values.add(key)


def get_table_name(q):
    regex = r"find withsource = TableName in\s*\(([A-Za-z]+)\s*\)"
    return re.search(regex, q).group(1)


def organize_registry_data(device_registry_events_data):
    registry_value_dict = {}
    for k in ["RegistryValueData", "RegistryValueName", "RegistryValueType"]:
        if k in device_registry_events_data:
            registry_value_dict[k] = device_registry_events_data[k]
            device_registry_events_data.pop(k)
        else:
            registry_value_dict[k] = ''
    device_registry_events_data["RegistryValues"] = [registry_value_dict]


def organize_ips(data):
    ips_comp_lst = data.pop('IPAddressesSet')
    flat_lst = [ip_obj['IPAddress'] for ips in ips_comp_lst for ip_obj in json.loads(ips) if 'IPAddress' in ip_obj]
    data['IPAddresses'] = flat_lst


def create_event_link(data, timestamp):
    try:
        if 'DeviceId' in data:
            # parse timestamp to date object striping nanoseconds
            timestamp_dt = datetime.strptime(timestamp[:-9], "%Y-%m-%dT%H:%M:%S")
            timeline_start = (timestamp_dt - timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%S") + ".000Z"
            timeline_end = (timestamp_dt + timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%S") + ".000Z"
            event_link = 'https://%s/machines/%s/timeline?from=%s&to=%s' % (
                'security.microsoft.com', data.get('DeviceId'), timeline_start, timeline_end)
            data['event_link'] = event_link
    except Exception as ex:
        data['event_link'] = ''


def remove_duplicate_ips(event_data):
    ## remove duplicate ips between LocalIP, PublicIP and IPAddresses:
    if 'PublicIP' in event_data and 'LocalIP' in event_data and \
            event_data['PublicIP'] == event_data['LocalIP']:
        event_data.pop('PublicIP')
    remove_duplicate_ips_from(event_data, 'LocalIP')
    remove_duplicate_ips_from(event_data, 'PublicIP')


def remove_duplicate_ips_from(event_data, prop_name):
    if 'IPAddresses' in event_data and prop_name in event_data:
        filtered = [x for x in event_data['IPAddresses'] if
                    not x == event_data[prop_name]]
        if len(filtered) > 0:
            event_data['IPAddresses'] = filtered
        else:
            event_data.pop('IPAddresses')


def unify_alert_fields(event_data):
    techniques_lists = []
    # attack techinques is a string due to the make_list function in the kql
    # need to convert it back to dict
    if 'AttackTechniques' in event_data:
        for techniques_lst in event_data['AttackTechniques']:
            try:
                attack_techniques = json.loads(techniques_lst)
            except json.decoder.JSONDecodeError:
                attack_techniques = ''
            finally:
                techniques_lists.append(attack_techniques)
        event_data['AttackTechniques'] = techniques_lists

    alerts = []
    alerts_count = len(event_data['AlertId'])
    for i in range(alerts_count):
        alert_dct = {k: (event_data[k][i] if len(event_data[k]) > i else '')
                     for k in Connector.ALERT_FIELDS if k in event_data}
        if alert_dct['AlertId'] not in [alert['AlertId'] for alert in alerts]:
            alerts.append(alert_dct)
    event_data['Alerts'] = json.dumps(alerts)
    for f in Connector.ALERT_FIELDS:
        event_data.pop(f, None)


class Connector(BaseJsonSyncConnector):
    init_error = None
    logger = logger.set_logger(__name__)
    make_alert_as_list = True

    ALERTS_QUERY = ('{} | join kind=leftouter '
                    '(DeviceAlertEvents | summarize AlertId=make_list(AlertId), Severity=make_list(Severity), '
                    'Title=make_list(Title), Category=make_list(Category), '
                    'AttackTechniques=make_list(AttackTechniques) by DeviceName, ReportId, Timestamp)'
                    ' on ReportId, DeviceName, Timestamp ')
    DEVICE_INFO_QUERY = ('{} | join kind=leftouter '
                         '(DeviceInfo | project DI_TS = Timestamp, DeviceId, PublicIP, OSArchitecture, OSPlatform, OSVersion) '
                         'on DeviceId | where DI_TS < Timestamp '
                         '| summarize arg_max(DI_TS, *) by ReportId, DeviceName, Timestamp ')
    DEVICE_NETWORK_QUERY = ('{} | join kind=leftouter '
                            '(DeviceNetworkInfo | where NetworkAdapterStatus == "Up" '
                            '| project DNI_TS = Timestamp, DeviceId, MacAddress, IPAddresses '
                            '| summarize IPAddressesSet=make_set(IPAddresses), MacAddressSet=make_set(MacAddress) '
                            'by DeviceId, DNI_TS) on DeviceId '
                            '| where DNI_TS < Timestamp | summarize arg_max(DNI_TS, *) '
                            'by ReportId, DeviceName, Timestamp '
                            )

    EVENTS_QUERY = ('(find withsource = TableName in ({})  where (Timestamp == datetime({})) '
                    'and (DeviceName == "{}") and (ReportId == {}))')

    EVENTS_TABLES = ['DeviceNetworkEvents', 'DeviceProcessEvents', 'DeviceFileEvents', 'DeviceRegistryEvents',
                     'DeviceEvents', 'DeviceImageLoadEvents']
    ALERT_FIELDS = ['AlertId', 'Severity', 'Title', 'Category', 'AttackTechniques']

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        self.connector = __name__.split('.')[1]
        self.alert_mode = False
        self.should_include_alerts = configuration.get("includeAlerts")
        self.should_include_network_info = configuration.get("includeNetworkInfo")
        self.should_include_host_os = configuration.get("includeHostOs")
        self.adal_response = Connector.generate_token(self, connection, configuration)
        if self.adal_response['success']:
            configuration['auth']['access_token'] = self.adal_response['access_token']
            self.api_client = APIClient(connection, configuration)
        else:
            self.init_error = True

    def join_alert_with_events(self, timestamp, device_name, report_id):
        events_query = "union {}".format(','.join(
            [Connector.EVENTS_QUERY.format(q, timestamp, device_name, report_id) for q in
             Connector.EVENTS_TABLES]))
        return self.join_query_with_other_tables(events_query, include_alerts=False)

    def join_query_with_other_tables(self, query, include_alerts=True):
        table = get_table_name(query)
        query = f"({query})"
        if 'Alert' in table:
            self.alert_mode = True
        if self.should_include_alerts and not self.alert_mode and include_alerts:
            query = Connector.ALERTS_QUERY.format(query)
        if self.should_include_host_os:
            query = Connector.DEVICE_INFO_QUERY.format(query)
        if self.should_include_network_info:
            query = Connector.DEVICE_NETWORK_QUERY.format(query)
        return query

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
        return_obj = {
            'success': True,
            'data': []
        }

        try:
            if self.init_error:
                return self.adal_response
            joined_query = self.join_query_with_other_tables(query)
            response_data = await self.api_client_run_search(joined_query, length, offset)
            response_data = merge_alerts(response_data)
            for event_data in response_data:
                table = event_data.get('TableName')
                # values for query
                device_name = event_data.get('DeviceName')
                report_id = event_data.get('ReportId')
                timestamp = event_data.get('Timestamp')
                if self.alert_mode and all([device_name, report_id, timestamp]):
                    # query events table according to alert fields
                    joined_query = self.join_alert_with_events(timestamp, device_name, report_id)
                    print("joining alert with events: ", joined_query)
                    events_data = await self.api_client_run_search(joined_query, length, offset)
                    if len(events_data) == 0:
                        # if only alert - assign the alert title to x-oca-event
                        event_data['ActionType'] = event_data.get("Title")
                        return_obj['data'].append({
                            table: event_data
                        })
                    else:
                        # correlated events where found to the alert
                        self.alert_mode = False
                        alert_data = copy.deepcopy(event_data)
                        if 'AttackTechniques' in alert_data:
                            if alert_data['AttackTechniques'] == '':
                                alert_data['AttackTechniques'] = '[]'
                        alert_data = {k: ([v] if k in self.ALERT_FIELDS else v) for (k, v) in alert_data.items()}
                        for event_data in events_data:
                            table = event_data.get("TableName")
                            event_data = {**alert_data, **event_data}
                            return_obj['data'].append({
                                table: event_data
                            })
                else:
                    return_obj['data'].append({
                        table: event_data
                    })
            for event in return_obj['data']:
                table = next(iter(event))
                event_data = event[table]
                timestamp = event_data.get('Timestamp')
                event_data['category'] = '1'
                event_data['provider'] = '1'
                # link the event to ms atp console device timeline with one second before and after the event https://security.microsoft.com/machines/<MachineId>/timeline?from=<start>&to=<end>
                create_event_link(event_data, timestamp)
                if event_data.get('AlertId') is not None and not self.alert_mode:
                    unify_alert_fields(event_data)
                if 'IPAddressesSet' in event_data:
                    organize_ips(event_data)
                if table == "DeviceRegistryEvents":
                    organize_registry_data(event_data)
                if table == "DeviceEvents":
                    if 'ProcessId' not in event_data or event_data['ProcessId'] is None or \
                            event_data['ProcessId'] == "":
                        event_data["missingChildShouldMapInitiatingPid"] = event_data.get("InitiatingProcessId")
                event_data['event_count'] = '1'
                remove_duplicate_ips(event_data)
                remove_duplicate_and_empty_fields(event_data)
                event_data['original_ref'] = json.dumps(event_data)
            return return_obj

        except Exception as ex:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception', connector=self.connector)
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise ex

    async def api_client_run_search(self, joined_query, length, offset):
        temp_return_obj = dict()
        response = await self.api_client.run_search(joined_query, offset, length)
        temp_return_obj = self._handle_errors(response, temp_return_obj)
        response_data = json.loads(temp_return_obj["data"]).get("Results")
        return response_data

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
