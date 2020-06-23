from stix_shifter_utils.utils.error_mapper_base import ErrorMapperBase
from stix_shifter_utils.utils.error_response import ErrorCode
from stix_shifter_utils.utils import logger

error_mapping = {
        'service_not_availiable' :  ErrorCode.TRANSMISSION_CONNECT,
        'Authorizaion Failed' : ErrorCode.TRANSMISSION_AUTH_CREDENTIALS,
        'query_failed': ErrorCode.TRANSMISSION_QUERY_LOGICAL_ERROR
    }

class ErrorMapper():
    logger = logger.set_logger(__name__)
    DEFAULT_ERROR = ErrorCode.TRANSMISSION_MODULE_DEFAULT_ERROR

    @staticmethod
    def set_error_code(json_data, return_obj):
        code = None
        try:
            code = json_data['code']
        except Exception:
            pass

        error_code = ErrorMapper.DEFAULT_ERROR
        if code in error_mapping:
            error_code = error_mapping[code]

        if error_code == ErrorMapper.DEFAULT_ERROR:
            ErrorMapper.logger.error("failed to map: "+ str(json_data))

        ErrorMapperBase.set_error_code(return_obj, error_code)
