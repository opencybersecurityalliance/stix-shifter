from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class InvalidAuthenticationException(Exception):
    pass


class InternalServerErrorException(Exception):
    pass


class InvalidLicenseException(Exception):
    pass


class APIPermissionException(Exception):
    pass


class InvalidJsonException(Exception):
    pass


class InvalidQueryException(Exception):
    pass


class ResponseMapper:
    logger = logger.set_logger(__name__)
    connector = __name__.split('.')[1]

    @staticmethod
    def status_code_mapping(response_code, response_text):
        """
        raise exceptions for the error response code
        :return dict
        """
        return_obj = {}
        response_dict = {}

        try:
            if response_code == 500:
                return_obj = ResponseMapper.handle_response_500(response_text, return_obj, response_dict)
            else:
                response_codes_match = {
                    400: InvalidJsonException(response_text['reply']['err_msg']),
                    401: InvalidAuthenticationException,
                    402: InvalidLicenseException,
                    403: APIPermissionException
                }
                raise response_codes_match[response_code]
        except InvalidAuthenticationException:
            response_dict['type'] = "AuthenticationError"
            response_dict['message'] = "Invalid api_key"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=ResponseMapper.connector)
        except InvalidLicenseException:
            response_dict['type'] = "InvalidLicense"
            response_dict['message'] = "User does not have the required license type to run this API"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=ResponseMapper.connector)
        except APIPermissionException:
            response_dict['type'] = "APIPermissionException"
            response_dict['message'] = "The provided API Key does not have the required RBAC permissions to run " \
                                       "this API"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=ResponseMapper.connector)
        except InvalidJsonException as ex:
            response_dict['type'] = "InvalidJsonException"
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=ResponseMapper.connector)
        except Exception as ex:
            response_dict['type'] = ex.__class__.__name__
            response_dict['message'] = ex
            ResponseMapper.logger.error('error when getting search results: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=ResponseMapper.connector)
        return return_obj

    @staticmethod
    def handle_response_500(response_text, return_obj, response_dict):
        """
        Handle 500 error code response
        :param response_text: dict
        :param response_dict: dict
        :param return_obj: dict
        """
        try:
            if isinstance(response_text['reply']['err_extra'], dict) and \
                    'parse_err' in response_text['reply']['err_extra'].keys():
                raise InvalidQueryException
            raise InternalServerErrorException(response_text['reply']['err_msg'])

        except InvalidQueryException:
            response_dict['type'] = "SyntaxError"
            response_dict['message'] = 'Bad query Syntax'
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=ResponseMapper.connector)
        except InternalServerErrorException as ex:
            response_dict['type'] = "AttributeError"
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=ResponseMapper.connector)
        except Exception as exp:
            response_dict['type'] = exp.__class__.__name__
            response_dict['message'] = exp
            ResponseMapper.logger.error('error when getting search results: %s', exp)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=ResponseMapper.connector)
        return return_obj
