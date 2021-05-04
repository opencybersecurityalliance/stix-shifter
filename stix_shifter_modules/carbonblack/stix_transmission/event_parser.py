from datetime import datetime, timedelta, timezone
import re
from stix_shifter_utils.utils import logger

logger = logger.set_logger(__name__)

supported_event_types = [
    'filemod',
    'modload',
    'regmod',
    'netconn',
    'childproc',
    'crossproc'
]
regmod_fields = ['operation_type', 'event_time', 'registry_key_path', 'tamper']
filemod_fields = ['operation_type', 'event_time', 'file_path', 'md5', 'file_type', 'tamper']
modload_fields = ['event_time', 'md5', 'path']
crossproc_fields = ['crossproc_type', 'event_time', 'target_unique_id', 'target_md5', 'target_path', 'sub_type',
                    'requested_access', 'tamper']
str_event_fields = {
    'regmod': regmod_fields,
    'filemod': filemod_fields,
    'modload': modload_fields,
    'crossproc': crossproc_fields
}

# Textual values adopted from API documentation for file modification event type
# https://developer.carbonblack.com/reference/enterprise-response/6.3/rest-api/#filemod_complete
filemod_operation_dict = {'1': 'Created the file', '2': 'First wrote to the file', '4': 'Deleted the file', '8': 'Last wrote to the file'}

# Textual values adopted from API documentation for registry modification event type
# https://developer.carbonblack.com/reference/enterprise-response/6.3/rest-api/#regmod_complete
regmod_operation_dict = {'1': 'Created the registry key', '2': 'First wrote to the registry key', '4': 'Deleted the key', '8': 'Deleted the value'}
CB_PROVIDER = 'Carbon Black Response'


def parse_raw_event_to_obj(event_type, raw_event_data):
    if raw_event_data:
        if isinstance(raw_event_data, dict):
            return raw_event_data
        if isinstance(raw_event_data, str):
            return _raw_event_str_to_obj(event_type, raw_event_data)
    return None


def _raw_event_str_to_obj(event_type, raw_event_data):
    event_values = raw_event_data.split('|')
    if event_type in str_event_fields:
        event_obj = {}
        for index, event_field in enumerate(str_event_fields[event_type]):
            event_obj[event_field] = event_values[index]
        return event_obj
    return None


def format_timestamp(timestamp):
    """
    to TZ format
    :param timestamp: datetime object
    :return: 2021-03-14T13:17:07.716000Z
    """
    if not timestamp:
        return timestamp
    try:
        return timestamp.isoformat() + 'Z'
    except Exception:
        pass
    return timestamp


def extract_time_window(query):
    if re.search(r'last_update:\[(.*?)]', query):
        # Case: 'last_update:[2021-04-22T11:09:00 TO 2021-04-22T11:10:00]'
        last_update_arr = re.findall(r'last_update:\[(.*?)]', query)
        if len(last_update_arr) > 0:
            time_window = last_update_arr[0].split(' TO ')
            if len(time_window) == 2:
                return [datetime.strptime(time_window[0], '%Y-%m-%dT%H:%M:%S'),
                        datetime.strptime(time_window[1], '%Y-%m-%dT%H:%M:%S')]
    elif re.search(r'last_update:-(\d*)m', query):
        # Case: '((process_name:erl.exe) and last_update:-5m)'
        last_update_arr = re.findall(r'last_update:-(\d*)m', query)
        if len(last_update_arr) > 0:
            last_minutes = float(last_update_arr[0])
            end_time = datetime.now(timezone.utc)
            start_time = end_time - timedelta(minutes=last_minutes)
            return [start_time.replace(tzinfo=None), end_time.replace(tzinfo=None)]
    return None


def get_timestamp_by_event_type(event_obj, event_type):
    try:
        if event_type in str_event_fields.keys():
            # format: 2014-01-23 09:19:08.331
            timestamp = event_obj.get('event_time')
            return datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        elif event_type == 'netconn':
            # format: 2017-01-11T16:20:04.892Z
            timestamp = event_obj.get('timestamp')
            return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
        elif event_type == 'childproc':
            # format: 2017-01-11T19:57:44.066000Z / 2017-01-11T19:57:44Z
            action_type = event_obj.get('type')
            if action_type:
                timestamp = event_obj.get(action_type)
                try:
                    return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
                except ValueError:
                    pass
                try:
                    return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
                except ValueError:
                    pass
    except Exception as ex:
        logger.warning('Failed to parse timestamp for {} event, skipping, {}'.format(event_type, str(ex)))
    return None


def is_timestamp_in_window(timestamp, time_window):
    try:
        return time_window[0] <= timestamp <= time_window[1]
    except Exception as ex:
        logger.warning('Failed to check if timestamp in time_window, {}'.format(str(ex)))
        return False


def get_common_fields_as_dict(cbr_process):
    common_fields = {'device_os': cbr_process.get('os_type'),
                     'device_name': cbr_process.get('hostname'),
                     'host_type': cbr_process.get('host_type'),
                     'process_pid': cbr_process.get('process_pid'),
                     'process_name': cbr_process.get('process_name'),
                     'parent_pid': cbr_process.get('parent_pid'),
                     'parent_name': cbr_process.get('parent_name'),
                     'process_cmdline': cbr_process.get('cmdline'),
                     'interface_ip': cbr_process.get('interface_ip'),
                     'device_external_ip': cbr_process.get('comms_ip'),
                     'provider': CB_PROVIDER
                     }
    return common_fields


def create_regmod_obj(event_dict, event_type, cbr_event):
    val = cbr_event.get('operation_type')
    event_dict['event_type'] = event_type
    event_dict['event_timestamp'] = cbr_event.get('parsed_timestamp')
    event_dict['regmod_name'] = cbr_event.get('registry_key_path')
    event_dict['regmod_action'] = regmod_operation_dict[val] if val is not None else None
    return event_dict


def create_crossproc_obj(event_dict, event_type, cbr_event):
    event_dict['event_type'] = event_type
    event_dict['event_timestamp'] = cbr_event.get('parsed_timestamp')
    event_dict['crossproc_name'] = cbr_event.get('target_path')
    event_dict['crossproc_action'] = cbr_event.get('crossproc_type')
    event_dict['crossproc_md5'] = cbr_event.get('target_md5')
    return event_dict


def create_modload_obj(event_dict, event_type, cbr_event):
    event_dict['event_type'] = event_type
    event_dict['event_timestamp'] = cbr_event.get('parsed_timestamp')
    event_dict['modload_name'] = cbr_event.get('path')
    event_dict['modload_md5'] = cbr_event.get('md5')
    return event_dict


def create_filemod_obj(event_dict, event_type, cbr_event):
    val = cbr_event.get('operation_type')
    event_dict['event_type'] = event_type
    event_dict['event_timestamp'] = cbr_event.get('parsed_timestamp')
    event_dict['filemod_name'] = cbr_event.get('file_path')
    event_dict['filemod_action'] = filemod_operation_dict[val] if val is not None else None
    event_dict['filemod_md5'] = cbr_event.get('md5')
    return event_dict


def create_childproc_obj(event_dict, event_type, cbr_event):
    event_dict['event_type'] = event_type
    event_dict['event_timestamp'] = cbr_event.get('parsed_timestamp')
    event_dict['childproc_name'] = cbr_event.get('path')
    event_dict['childproc_md5'] = cbr_event.get('md5')
    event_dict['childproc_sha256'] = cbr_event.get('sha256')
    event_dict['childproc_cmdline'] = cbr_event.get('commandLine')
    event_dict['childproc_username'] = cbr_event.get('userName')
    event_dict['childproc_pid'] = cbr_event.get('pid')
    event_dict['childproc_action'] = cbr_event.get('type')
    return event_dict


def create_netconn_obj(event_dict, event_type, cbr_event):
    event_dict['event_type'] = event_type
    event_dict['event_timestamp'] = cbr_event.get('parsed_timestamp')
    event_dict['domain'] = cbr_event['domain']
    event_dict['netconn_remote_port'] = cbr_event.get('remote_port')
    event_dict['netconn_remote_ipv4'] = cbr_event.get('remote_ip')
    event_dict['netconn_local_port'] = cbr_event.get('local_port')
    event_dict['netconn_local_ipv4'] = cbr_event.get('local_ip')
    return event_dict


create_event_obj_by_type = {'regmod': create_regmod_obj, 'modload': create_modload_obj, 'netconn': create_netconn_obj,
             'childproc': create_childproc_obj, 'crossproc': create_crossproc_obj, 'filemod': create_filemod_obj}


def create_event_obj(process, event):
    try:
        event_type = event['event_type']
    except KeyError:
        logger.warning('Event type key is unknown')
        return None

    try:
        common_fields = get_common_fields_as_dict(process)
        # Fields in event object are mapped as close as possible to Carbon Black Cloud event's fields,
        # in order to re-use "to_stix.json" mapping file.
        event_obj = create_event_obj_by_type[event_type](common_fields, event_type, event['parsed_event_data'])
    except Exception as ex:
        logger.warning('Unsupported event {}, {}'.format(event_type, str(ex)))
        return None
    return event_obj
