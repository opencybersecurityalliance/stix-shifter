from stix_shifter_utils.utils.error_mapper_base import ErrorMapperBase
from stix_shifter_utils.utils.utils.error_response import ErrorResponder, ErrorCode
from enum import Enum
from stix_shifter_utils.utils import logger


class ErrorCaptureType(Enum):
    ERROR_MESSAGE = 'ERROR_MESSSAGE'
    STRUCT_VALUE = 'STRUCT_VALUE'

error_mapping = (
        (ErrorCaptureType.ERROR_MESSAGE, 'XML parsing error', ErrorCode.TRANSMISSION_QUERY_PARSING_ERROR),
        (ErrorCaptureType.ERROR_MESSAGE, 'is not defined', ErrorCode.TRANSMISSION_QUERY_PARSING_ERROR),
        (ErrorCaptureType.STRUCT_VALUE, (('BESAPI', 'ClientQueryResults'), None), (ErrorCode.TRANSMISSION_RESPONSE_EMPTY_RESULT, 'result is not found'))
)

class ErrorMapper(ErrorMapperBase):
    logger = logger.set_logger(__name__)
    DEFAULT_ERROR = ErrorCode.TRANSMISSION_MODULE_DEFAULT_ERROR.value

    @staticmethod
    def set_error_code(json_data, return_obj):
        error_code = ErrorMapper.DEFAULT_ERROR

        for error_package in error_mapping:
            search_type = error_package[0]
            search_criteria = error_package[1]
            result_error = error_package[2]

            if ErrorCaptureType.ERROR_MESSAGE == search_type:
                if 'error' in return_obj and search_criteria in return_obj['error']:
                    error_code = result_error
            elif ErrorCaptureType.STRUCT_VALUE == search_type:
                search_path = search_criteria[0]
                desired_value = search_criteria[1]
                stuct_search_result = ErrorResponder.get_struct_item(json_data, search_path[:-1])
                if stuct_search_result is not None and search_path[-1] in stuct_search_result and stuct_search_result[search_path[-1]]==desired_value:
                    error_code = result_error

        if error_code == ErrorMapper.DEFAULT_ERROR:
            ErrorMapper.logger.debug('failed to map: ' + str(json_data))

        if isinstance(error_code, tuple):
            ErrorMapperBase.set_error_code(return_obj, error_code[0], error_code[1])
        else:
            ErrorMapperBase.set_error_code(return_obj, error_code)