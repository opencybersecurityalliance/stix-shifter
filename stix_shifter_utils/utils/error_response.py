from requests.exceptions import SSLError, ConnectionError
from enum import Enum
import importlib
import traceback
from stix_shifter_utils.utils.error_mapper_base import ErrorMapperBase
from stix_shifter_utils.utils import logger as utils_logger
import collections
import json


logger = utils_logger.set_logger(__name__)


class ErrorCode(Enum):
    TRANSLATION_NOTIMPLEMENTED_MODE = 'not_implemented'
    TRANSLATION_MODULE_DEFAULT_ERROR = 'invalid_parameter'
    TRANSLATION_MAPPING_ERROR = 'mapping_error'
    TRANSLATION_STIX_VALIDATION = 'invalid_parameter'
    TRANSLATION_NOTSUPPORTED = 'invalid_parameter'
    TRANSLATION_RESULT = 'mapping_error'
    TRANSLATION_UNKNOWN_DIALOG = 'invalid_parameter'
    TRANSLATION_UNKNOWN_LANGUAGE = 'invalid_parameter'

    TRANSMISSION_UNKNOWN = 'unknown'
    TRANSMISSION_CONNECT = 'service_unavailable'
    TRANSMISSION_AUTH_SSL = 'authentication_fail'
    TRANSMISSION_AUTH_CREDENTIALS = 'authentication_fail'
    TRANSMISSION_MODULE_DEFAULT_ERROR = 'unknown'
    TRANSMISSION_QUERY_PARSING_ERROR = 'invalid_query'
    TRANSMISSION_QUERY_LOGICAL_ERROR = 'invalid_query'
    TRANSMISSION_RESPONSE_EMPTY_RESULT = 'no_results'
    TRANSMISSION_SEARCH_DOES_NOT_EXISTS = 'no_results'
    TRANSMISSION_INVALID_PARAMETER = 'invalid_parameter'
    TRANSMISSION_REMOTE_SYSTEM_IS_UNAVAILABLE = 'service_unavailable'


class ErrorResponder():

    @staticmethod
    def get_struct_item(message_struct, message_path):
        # "+isFailure=True" means the current item is a list and the new item will be a list containing items with the field 'Failure' equal 'True'
        # '~result' means the current item is a list and new item will be a list containing specified field ('result') values
        # document it: '+' and '~'
        if message_struct is not None and message_path is not None:
            if (isinstance(message_struct, collections.Mapping) or type(message_struct).__name__=='list'):
                struct = message_struct.copy()
                for i in message_path:
                    if (isinstance(struct, collections.Mapping) and i in struct) or (type(struct).__name__=='list' and isinstance(i, int) and i < len(struct)):
                        struct = struct[i]
                        if struct is None:
                            break
                    elif i[:1] == '+' and isinstance(struct, list):
                        key, value = i[1:].split('=')
                        filtered_struct = list(filter(lambda item: (key in item and str(item[key])==str(value)), struct))
                        struct = filtered_struct
                    elif i[:1] == '~' and isinstance(struct, list):
                        key = i[1:]
                        filtered_struct = set()
                        for s in struct:
                            filtered_struct.add(s[key])
                        struct = list(filtered_struct)
                    else:
                        break
                return struct
            else:
                return message_struct

    @staticmethod
    def fill_error(return_object, message_struct=None, message_path=None, message=None, error=None):
        return_object['success'] = False
        error_code = ErrorCode.TRANSMISSION_UNKNOWN

        if message is None:
            message = ''

        struct_item = ErrorResponder.get_struct_item(message_struct, message_path)
        if struct_item is not None:
            if len(message) > 0:
                message += ';'
            if (isinstance(struct_item, list)):
                struct_item = json.dumps(struct_item)
            message += str(struct_item)
        error_msg = ''
        if error is not None:
            str_error = str(error)
            logger.error("error occurred: " + str_error)
            logger.debug(utils_logger.exception_to_string(error))
            if isinstance(error, SSLError):
                error_code = ErrorCode.TRANSMISSION_AUTH_SSL
                error_msg = 'Wrong certificate: ' + str_error
            elif isinstance(error, ConnectionError):
                error_code = ErrorCode.TRANSMISSION_CONNECT
                error_msg = 'Connection error: ' + str_error
            else:
                error_msg = str(error)

            if len(error_msg) > 0:
                if len(message) > 0:
                    message += '; '
                message += error_msg

        if message is not None and len(message) > 0:
            if error_code.value == ErrorCode.TRANSMISSION_UNKNOWN.value:
                if 'uthenticat' in message or 'uthoriz' in message:
                    error_code = ErrorCode.TRANSMISSION_AUTH_CREDENTIALS
                elif 'query_syntax_error' in message:
                    error_code = ErrorCode.TRANSMISSION_QUERY_PARSING_ERROR
            return_object['error'] = str(message)
        ErrorMapperBase.set_error_code(return_object, error_code.value)
        if error_code == ErrorCode.TRANSMISSION_UNKNOWN:
            ErrorResponder.call_module_error_mapper(message_struct, return_object)

    @staticmethod
    def call_module_error_mapper(json_data, return_object):
        caller_path_list = traceback.extract_stack()[-3].filename.split('/')

        if 'stix_translation.py' in caller_path_list[-1]:
            module_path = 'stix_shifter_utils.stix_translation.stix_translation_error_mapper'
        else:
            caller_module_name = caller_path_list[-3:-1]
            module_path = 'stix_shifter_modules.' + caller_module_name[0] + '.'  + caller_module_name[1] + '.error_mapper'

        # path_start_position = ErrorResponder.rindex(caller_path_list, 'stix-shifter')
        # module_path = 'stix_shifter_modules.' + caller_module_name[0] + '.'  + caller_module_name[1] + '.' + caller_module_name[0] + '_error_mapper'
        # module_path = '.'.join(caller_path_list[path_start_position: -1]) + '.' + caller_module_name + '_error_mapper'
        try:
            module = importlib.import_module(module_path)
            if json_data is not None:
                module.ErrorMapper.set_error_code(json_data, return_object)
            else:
                ErrorMapperBase.set_error_code(return_object, module.ErrorMapper.DEFAULT_ERROR)
        except ModuleNotFoundError:
            pass

    @staticmethod
    def rindex(mylist, myvalue):
        return len(mylist) - mylist[::-1].index(myvalue) - 1

    @staticmethod
    def is_plain_string(s):
        return isinstance(s, str) and not s.startswith('<?') and not s.startswith('{')

    @staticmethod
    def is_json_string(s):
        return isinstance(s, str) and s.startswith('{')
