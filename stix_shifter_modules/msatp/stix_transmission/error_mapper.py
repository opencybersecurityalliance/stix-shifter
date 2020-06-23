""""MSATP connector specified error handling"""
from stix_shifter_utils.utils.error_mapper_base import ErrorMapperBase
from stix_shifter_utils.utils.error_response import ErrorCode
from stix_shifter_utils.utils import logger

ERROR_MAPPING = {
    "json_parse_exception": ErrorCode.TRANSMISSION_QUERY_PARSING_ERROR,
    "HTTPSConnectionError": ErrorCode.TRANSMISSION_CONNECT,
    "illegal_argument_exception": ErrorCode.TRANSMISSION_INVALID_PARAMETER,
    "invalid_client": ErrorCode.TRANSMISSION_AUTH_CREDENTIALS,
    "invalid_resource": ErrorCode.TRANSMISSION_REMOTE_SYSTEM_IS_UNAVAILABLE,
    "unauthorized_client": ErrorCode.TRANSMISSION_AUTH_CREDENTIALS,
    "invalid_request": ErrorCode.TRANSMISSION_AUTH_CREDENTIALS,
    "NotFound": ErrorCode.TRANSMISSION_SEARCH_DOES_NOT_EXISTS,
    "ConnectionError": ErrorCode.TRANSMISSION_CONNECT
}


class ErrorMapper:
    """"ErrorMapper class"""
    logger = logger.set_logger(__name__)
    DEFAULT_ERROR = ErrorCode.TRANSMISSION_MODULE_DEFAULT_ERROR

    @staticmethod
    def set_error_code(json_data, return_obj):
        """ms_atp transmit specified error
         :param json_data: dict, error response of api_call
         :param return_obj: dict, returns error and error code"""
        error_type = ''
        
        if isinstance(json_data, tuple):
            error_type = 'HTTPSConnectionError'
        else:
            try:
                error_type = json_data['error']['code']
            except Exception:
                error_type = json_data['error']

        error_code = ErrorMapper.DEFAULT_ERROR

        if error_type in ERROR_MAPPING:
            error_code = ERROR_MAPPING[error_type]

        if error_code == ErrorMapper.DEFAULT_ERROR:
            ErrorMapper.logger.error("failed to map: " + str(json_data))

        ErrorMapperBase.set_error_code(return_obj, error_code)
