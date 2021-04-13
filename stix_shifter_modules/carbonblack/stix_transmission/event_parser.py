from datetime import datetime
from stix_shifter_utils.stix_translation.src.utils.transformers import ToIPv4
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


def format_timestamp(_timestamp):
    """
     to TZ format
    :param _timestamp: 2021-03-14 13:17:07.716
    :return: 2021-03-14T13:17:07.716000Z
    """
    if not _timestamp:
        return _timestamp
    try:
        dt = datetime.strptime(_timestamp, '%Y-%m-%d %H:%M:%S.%f')
        return dt.isoformat() + 'Z'
    except Exception:
        pass
    return _timestamp


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
    event_dict['event_timestamp'] = format_timestamp(cbr_event.get('event_time'))
    event_dict['regmod_name'] = cbr_event.get('registry_key_path')
    event_dict['regmod_action'] = regmod_operation_dict[val] if val is not None else None
    return event_dict


def create_crossproc_obj(event_dict, event_type, cbr_event):
    event_dict['event_type'] = event_type
    event_dict['event_timestamp'] = format_timestamp(cbr_event.get('event_time'))
    event_dict['crossproc_name'] = cbr_event.get('target_path')
    event_dict['crossproc_action'] = cbr_event.get('crossproc_type')
    event_dict['crossproc_md5'] = cbr_event.get('target_md5')
    return event_dict


def create_modload_obj(event_dict, event_type, cbr_event):
    event_dict['event_type'] = event_type
    event_dict['event_timestamp'] = format_timestamp(cbr_event.get('event_time'))
    event_dict['modload_name'] = cbr_event.get('path')
    event_dict['modload_md5'] = cbr_event.get('md5')
    return event_dict


def create_filemod_obj(event_dict, event_type, cbr_event):
    val = cbr_event.get('operation_type')

    event_dict['event_type'] = event_type
    event_dict['event_timestamp'] = format_timestamp(cbr_event.get('event_time'))
    event_dict['filemod_name'] = cbr_event.get('file_path')
    event_dict['filemod_action'] = filemod_operation_dict[val] if val is not None else None
    event_dict['filemod_md5'] = cbr_event.get('md5')
    return event_dict


def create_childproc_obj(event_dict, event_type, cbr_event):
    event_dict['event_type'] = event_type
    event_dict['event_timestamp'] = format_timestamp(cbr_event.get('event_time'))
    event_dict['childproc_name'] = cbr_event.get('path')
    event_dict['childproc_md5'] = cbr_event.get('md5')
    event_dict['childproc_sha256'] = cbr_event.get('sha256')
    event_dict['childproc_cmdline'] = cbr_event.get('commandLine')
    event_dict['childproc_username'] = cbr_event.get('userName')
    event_dict['childproc_pid'] = cbr_event.get('pid')
    return event_dict


def create_netconn_obj(event_dict, event_type, cbr_event):
    event_dict['event_type'] = event_type
    event_dict['event_timestamp'] = format_timestamp(cbr_event.get('timestamp'))
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
