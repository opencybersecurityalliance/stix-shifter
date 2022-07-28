import json
from stix_shifter_utils.modules.base.stix_transmission.base_results_connector\
    import BaseResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from aiohttp.client_exceptions import ClientConnectionError


class LimitOutOfRangeError(Exception):
    pass

class QueryIdNotFoundError(Exception):
    pass

class ResultsConnector(BaseResultsConnector):
    """ResultsConnector class"""
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    async def create_results_connection(self, search_id, offset, length):
        """
        Fetching the results using query, offset and length
        :param search_id: str, Data Source queryID
        :param offset: str, Offset value
        :param length: str, Length value
        :return: dict
        """
        try:
            min_range = int(offset)
            max_range = int(offset) + int(length)

            return_obj = {}
            response_dict = {}

            response = await self.api_client.get_search_results(
                search_id, min_range, max_range)
            response_code = response.code

            response_txt = response.read().decode('utf-8')
            response_dict = json.loads(response_txt)
            total_data = []

            #Construct a response object
            if response_code == 200:
                return_obj['success'] = True
                response_dict = ResultsConnector.check_empty_data(response_dict)
                for item in response_dict['data']:
                    total_data.append(item)
            elif response_code == 400:
                return_obj['success'] = False
                response_code = response_dict.get("errors")[0].get("code")
                if response_code == 4000010:
                    raise LimitOutOfRangeError
            elif response_code == 404:
                return_obj['success'] = False
                response_code = response_dict.get("errors")[0].get("code")
                if response_code == 4040010:
                    raise QueryIdNotFoundError
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['message'])

            if response_dict.get("pagination"):
                pagination_dict = response_dict.get("pagination")
                if pagination_dict.get("nextCursor"):
                    cursor = pagination_dict.get("nextCursor")
                else:
                    cursor = None

                while cursor is not None:
                    response = await self.api_client.get_search_results(
                        search_id, min_range, max_range, nextcursor=cursor)
                    response_code = response.code
                    response_txt = response.read().decode('utf-8')
                    response_dict = json.loads(response_txt)
                    response_dict = self.check_empty_data(response_dict)

                    for item in response_dict['data']:
                        total_data.append(item)

                    if response_dict.get("pagination"):
                        pagination_dict = response_dict.get("pagination")
                        if pagination_dict.get("nextCursor"):
                            cursor = pagination_dict.get("nextCursor")
                        else:
                            cursor = None

            if response_code == 200:
                return_obj['success'] = True
                return_obj['data'] = total_data[min_range:max_range] if total_data else []
            elif response_code == 400:
                return_obj['success'] = False
                response_code = response_dict.get("errors")[0].get("code")
                if response_code == 4000010:
                    raise LimitOutOfRangeError
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['message'])

        except ClientConnectionError:
            response_dict['type'] = "ConnectionError"
            response_dict['message'] = "Invalid Host"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'])
        except LimitOutOfRangeError:
            response_dict['type'] = "LimitOutOfRangeError"
            response_dict['message'] = "Limit must be greater than or equals to 1 " \
                                       "and less than equals to 1000"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'])
        except QueryIdNotFoundError:
            response_dict['type'] = "QueryIdNotFoundError"
            response_dict['message'] = "Could not find query id: " + search_id
            ErrorResponder.fill_error(return_obj, response_dict, ['message'])
        except Exception as ex:
            self.logger.error('error in query result: %s', str(ex))
            ErrorResponder.fill_error(return_obj, response_dict, ['message'])
        return return_obj

    @staticmethod
    def check_empty_data(res_dict):
        """
        Format the results in json format
        :param item: list of dictionary items
        :return: list
        """
        for item in res_dict['data']:
            if item.get("netProtocolName") is None and item.get("eventType") is not None:
                if item.get("srcPort") is not None or item.get("dstPort") is not None:
                    # Initializing default protocol value to tcp
                    item["netProtocolName"] = "tcp"
                    if item.get("eventType") in ["GET", "POST", "PUT", "DELETE", "OPTIONS", "CONNECT", "HEAD"]:
                        item["netProtocolName"] = "http"

            if item.get("registryKeyPath") is not None:
                registryKeyPath = item.get("registryKeyPath")
                registryKeyPath = registryKeyPath.replace('MACHINE\\', 'HKEY_LOCAL_MACHINE\\')
                registryKeyPath = registryKeyPath.replace('USER\\', 'HKEY_CURRENT_USER\\')
                item["registryKeyPath"] = registryKeyPath
                if item.get("registryPath") is not None:
                    registryPath = item.get("registryPath")
                    registryPath = registryPath.replace('MACHINE\\', 'HKEY_LOCAL_MACHINE\\')
                    registryPath = registryPath.replace('USER\\', 'HKEY_CURRENT_USER\\')
                    item["registryPath"] = registryPath
                if item.get("registryOldValue") is None and item.get("registryValue") is None:
                    item["registryPath"] = None
                    item["registryKeyPath"] = None
                if item.get("registryOldValue") is not None:
                    oldvalue=item.get("registryOldValue")
                    valuetype = item.get("registryOldValueType")
                    if valuetype == "BINARY":
                        valuetype = "REG_BINARY"
                        item["registryOldValueType"] = valuetype
                    registryOldValue = {"data": oldvalue, "data_type": valuetype}
                    item["registryOldValue"] = registryOldValue
                if item.get("registryValue") is not None:
                    rvalue = item.get("registryValue")
                    valuetype = item.get("registryOldValueType")
                    if valuetype == "BINARY":
                        valuetype = "REG_BINARY"
                        item["registryOldValueType"] = valuetype
                    registryValue = {"data": rvalue, "data_type": valuetype}
                    item["registryValue"] = registryValue

            if item.get("loginIsAdministratorEquivalent") is not None:
                if item.get("loginIsAdministratorEquivalent") == "True" or \
                        item.get("loginIsAdministratorEquivalent") == "TRUE":
                    item["loginIsAdministratorEquivalent"] = True
                elif item.get("loginIsAdministratorEquivalent") == "False" or \
                        item.get("loginIsAdministratorEquivalent") == "FALSE":
                    item["loginIsAdministratorEquivalent"] = False

            #removing \" character from path containing string field because of parsing error
            ResultsConnector.replace_escape_character(item)
        return res_dict

    @staticmethod
    def replace_escape_character(item):
        """
        replace escape character from results in json format
        :param item: list of dictionary items
        """
        if item is not None:
            fields = ['processCmd', 'srcProcCmdLine', 'tgtProcCmdLine',
                      'processImagePath', 'signatureSignedInvalidReason',
                      'srcProcImageSha1', 'srcProcParentActiveContentPath',
                      'srcProcParentImagePath', 'tgtFilePath', 'srcProcParentImagePath',
                      'srcProcParentImageSha1', 'fileFullName', 'srcProcActiveContentPath',
                      'storyline', 'tgtFileDescription', 'tgtFileOldPath',
                      'srcProcImageSha256', 'srcProcParentCmdLine', 'srcProcParentImageSha256']

            for fieldname in fields:
                if item.get(fieldname) is not None:
                    val = item.get(fieldname)
                    # Escaping the double quote in certain fields value like srcProcCmdLine
                    if val.find("\"") != -1:
                        val = val.replace('\"', '\\"')
                    elif val.find('"') != -1:
                        val = val.replace('"', '\\"')
                    item[fieldname] = val
