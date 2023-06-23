import copy

from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from .boto3_client import BOTO3Client
from botocore.exceptions import EndpointConnectionError, ParamValidationError, ClientError, InvalidRegionError, \
    ReadTimeoutError, ConnectTimeoutError
import json


class InvalidMetadataException(Exception):
    pass


class Connector(BaseJsonSyncConnector):

    def __init__(self, connection, configuration):

        self.client = BOTO3Client(connection, configuration)
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def create_results_connection(self, query, offset, length, metadata=None):
        """
         Fetching the results using query, offset and length and metadata
        :param query: str, Data Source query
        :param offset: str, Offset value
        :param length: str, Length value
        :param metadata: dict
        :return: return_obj, dict
        """
        return_obj = {}
        response_dict = {}
        local_result_count = 0
        local_data = []
        try:
            if not isinstance(query, dict):
                query = json.loads(query)

            if metadata:
                if isinstance(metadata, dict) and metadata.get('result_count') and metadata.get('detector_ids') \
                        and metadata.get('next_page_token'):
                    result_count, detector_ids, next_page_token = metadata['result_count'], metadata['detector_ids'], \
                                metadata['next_page_token']
                    result_count = int(result_count)
                    total_records = int(length)
                    if abs(self.client.result_limit - result_count) < total_records:
                        total_records = abs(self.client.result_limit - result_count)
                else:
                    # raise exception when metadata doesn't contain result count or detector ids or next page token
                    raise InvalidMetadataException(metadata)
            else:
                detector_response = await self.get_detector()
                if detector_response.get('error') and detector_response.get('success') is False:
                    return detector_response
                else:
                    detector_ids = detector_response['data']
                result_count = 0
                next_page_token = None
                total_records = int(offset) + int(length)
                if self.client.result_limit < total_records:
                    total_records = self.client.result_limit
            track_detector_id = copy.deepcopy(detector_ids)
            max_items = total_records
            if (result_count == 0 and detector_ids and next_page_token is None) or (
                    result_count < self.client.result_limit and detector_ids):

                for detector_id in detector_ids:
                    list_findings = await self.client.get_paginated_result('guardduty', 'list_findings',
                                                                           DetectorId=detector_id,
                                                                           FindingCriteria=query['FindingCriteria'],
                                                                           PaginationConfig={'MaxItems': max_items,
                                                                                             'StartingToken':
                                                                                                 next_page_token})

                    if list_findings.get('ResponseMetadata') and list_findings['ResponseMetadata'].\
                            get('HTTPStatusCode') != 200:
                        return self.exception_response(list_findings)
                    else:
                        if list_findings['data']:
                            findings = list_findings['data']
                            next_page_token = list_findings.get('next_token')
                            result_count += len(list_findings['data'])
                            local_result_count += len(list_findings['data'])
                            if not next_page_token:
                                track_detector_id.remove(detector_id)
                            final_response = await self.get_findings(findings, detector_id)
                            if final_response.get('error') and final_response.get('success') is False:
                                return final_response
                            else:
                                local_data += final_response['data']
                            if local_result_count >= total_records:
                                break
                            else:
                                max_items = total_records - local_result_count

                if local_data:
                    return_obj['success'] = True
                    if metadata:
                        return_obj['data'] = local_data
                    else:
                        return_obj['data'] = local_data[int(offset):total_records]

                    if result_count < self.client.result_limit:
                        return_obj['metadata'] = {"result_count": result_count,
                                                  "next_page_token": next_page_token,
                                                  "detector_ids": track_detector_id}

                else:
                    return_obj['success'] = True
                    return_obj['data'] = []
            else:
                return_obj['success'] = True
                return_obj['data'] = []

        except ClientError as ex:
            if 'BadRequestException' in str(ex):
                response_dict['code'] = 400
            elif 'InternalServerErrorException' in str(ex):
                response_dict['code'] = 500
            else:
                response_dict['code'] = 403
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except EndpointConnectionError as ex:
            response_dict['code'] = 503
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except ParamValidationError as ex:
            response_dict['code'] = 400
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except InvalidRegionError as ex:
            response_dict['code'] = 400
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except ReadTimeoutError as ex:
            response_dict['code'] = 503
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except ConnectTimeoutError as ex:
            response_dict['code'] = 408
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except KeyError as ex:
            if 'InvalidClientTokenId' in str(ex) or 'SignatureDoesNotMatch' in str(ex) or 'ValidationError' in str(ex) \
                    or 'AccessDenied' in str(ex):
                response_dict['code'] = 403
            elif 'endpoint URL' in str(ex):
                response_dict['code'] = 503
            else:
                response_dict['code'] = 100
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except Exception as ex:
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    async def ping_connection(self):
        """
        Ping the endpoint
        :return: return_object, dict
        """
        return_obj = {}
        response_dict = {}
        try:
            response = await self.client.make_request('guardduty', 'list_detectors')
            if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
                return_obj['success'] = True
            else:
                return_obj = self.exception_response(response)

        except ClientError as ex:
            if 'BadRequestException' in str(ex):
                response_dict['code'] = 400
            else:
                response_dict['code'] = 403
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except EndpointConnectionError as ex:
            response_dict['code'] = 503
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except ParamValidationError as ex:
            response_dict['code'] = 400
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except InvalidRegionError as ex:
            response_dict['code'] = 400
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except ReadTimeoutError as ex:
            response_dict['code'] = 503
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except ConnectTimeoutError as ex:
            response_dict['code'] = 408
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except KeyError as ex:
            if 'InvalidClientTokenId' in str(ex) or 'SignatureDoesNotMatch' in str(ex) or 'ValidationError' in str(ex) \
                    or 'AccessDenied' in str(ex):
                response_dict['code'] = 403
            elif 'endpoint URL' in str(ex):
                response_dict['code'] = 503
            else:
                response_dict['code'] = 100
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except Exception as ex:
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    async def get_detector(self):
        """
        Fetch the detector id corresponding to the region
        :return: page token number, str
        """
        response = await self.client.get_paginated_result('guardduty', 'list_detectors')
        if response.get('ResponseMetadata', {}) and response['ResponseMetadata'].get('HTTPStatusCode') != 200:
            return self.exception_response(response)
        return response

    async def get_findings(self, findings, detector_id):
        """
        Get the finding details of the list of finding ids
        :param findings, list
        :param detector_id, int
        :return: return_obj, dict
        """
        data = []
        max_findings = 50
        return_obj = {}
        if len(findings) <= max_findings:
            final_response = await self.client.make_request('guardduty', 'get_findings',
                                                            DetectorId=detector_id,
                                                            FindingIds=findings)
            if final_response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
                data += final_response.get('Findings')
            else:
                return_obj = self.exception_response(final_response)
                data = []
        else:
            for finding in range(0, len(findings), max_findings):
                split_findings = findings[finding:finding + max_findings]
                final_response = await self.client.make_request('guardduty', 'get_findings',
                                                                DetectorId=detector_id,
                                                                FindingIds=split_findings)

                if final_response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
                    data += final_response['Findings']
                else:
                    return_obj = self.exception_response(final_response)
                    data = []
        if data:
            return_obj['data'] = Connector.format_result(data)
        return return_obj

    def exception_response(self, response):
        """
        Create the exception response
        :param response, dict
        :return: return_obj, dict
        """
        return_obj = {}
        response_dict = {'code': response.get('ResponseMetadata').get('HTTPStatusCode'),
                         'message': response.get('Error', {}).get('Message', '')}
        ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        return return_obj

    @staticmethod
    def format_result(response):
        """
        Formats the result
        param: response, list
        """
        updated_response = []
        for finding in response:
            finding = Connector.format_private_ip_address(finding)
            updated_response.append(finding)
        return updated_response

    @staticmethod
    def format_private_ip_address(finding):
        """
        remove the private ip address which matches either target or local ip address inorder to avoid
        duplicate ip address object creation
        :param finding,dict
        :return dict
        """
        local_affected_ip, target_affected_ip = '', ''
        if finding.get('Service', {}) and finding['Service'].get('ResourceRole', '') == 'TARGET':
            local_affected_ip = finding.get('Service', {}).get('Action', {}).get('NetworkConnectionAction', {}). \
                get('LocalIpDetails', {}).get('IpAddressV4', '')
        else:
            target_affected_ip = finding.get('Service', {}).get('Action', {}).get('NetworkConnectionAction', {}). \
                get('RemoteIpDetails', {}).get('IpAddressV4', '')
        if local_affected_ip or target_affected_ip:
            if finding.get('Resource', {}).get('InstanceDetails', {}).get('NetworkInterfaces', []):
                for ni in finding['Resource']['InstanceDetails']['NetworkInterfaces']:
                    if ni.get('PrivateIpAddresses', []):
                        for private_ip in ni['PrivateIpAddresses']:
                            if private_ip.get('PrivateIpAddress', '') == local_affected_ip or \
                                    private_ip.get('PrivateIpAddress', '') == target_affected_ip:
                                del private_ip['PrivateIpAddress']
                                break
        return finding

