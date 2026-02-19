import copy
from datetime import datetime, timedelta
import json
import re

from stix_shifter_utils.utils import logger


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
    # attack techniques is a string due to the make_list function in the kql
    # need to convert it back to dict
    if 'AttackTechniques' in event_data:
        for techniques_lst in event_data['AttackTechniques']:
            try:
                if techniques_lst == '':
                    attack_techniques = ''
                else:
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
                     for k in ConnectorPostProcessing.ALERT_FIELDS if k in event_data}
        if alert_dct['AlertId'] not in [alert['AlertId'] for alert in alerts]:
            alerts.append(alert_dct)
    event_data['Alerts'] = json.dumps(alerts)
    for f in ConnectorPostProcessing.ALERT_FIELDS:
        event_data.pop(f, None)


class ConnectorPostProcessing:
    logger = logger.set_logger(__name__)
    ALERT_FIELDS = ['AlertId', 'Severity', 'Title', 'Category', 'AttackTechniques']
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

    def __init__(self, options, alert_mode):
        """Initialization.
        :param options: dict,config dict"""
        self.alert_mode = alert_mode
        self.should_include_alerts = options.get("includeAlerts")
        self.should_include_network_info = options.get("includeNetworkInfo")
        self.should_include_host_os = options.get("includeHostOs")
        self.should_retain_original = options.get("retainOriginal")

    def join_alert_with_events(self, timestamp, device_name, report_id):
        events_query = "union {}".format(','.join(
            [ConnectorPostProcessing.EVENTS_QUERY.format(q, timestamp, device_name, report_id) for q in
             ConnectorPostProcessing.EVENTS_TABLES]))
        return self.join_query_with_other_tables(events_query, include_alerts=False)

    def join_query_with_other_tables(self, query, include_alerts=True):
        table = get_table_name(query)
        query = f"({query})"
        if 'Alert' in table:
            self.alert_mode = True
        if self.should_include_alerts and not self.alert_mode and include_alerts:
            query = ConnectorPostProcessing.ALERTS_QUERY.format(query)
        if self.should_include_host_os:
            query = ConnectorPostProcessing.DEVICE_INFO_QUERY.format(query)
        if self.should_include_network_info:
            query = ConnectorPostProcessing.DEVICE_NETWORK_QUERY.format(query)
        return query

    def post_process(self, response_data, return_obj, api_client_run_search):
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
                events_data = api_client_run_search(joined_query)
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
                    event_data["missingChildShouldMapInitiatingPid"] = -1 if event_data.get("InitiatingProcessId") is None else event_data.get("InitiatingProcessId")
            event_data['event_count'] = '1'
            remove_duplicate_ips(event_data)
            remove_duplicate_and_empty_fields(event_data)
            if self.should_retain_original:
                event_data['original_ref'] = json.dumps(event_data)
        return return_obj
