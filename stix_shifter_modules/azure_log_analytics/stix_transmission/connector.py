import json
from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from .api_client import APIClient
from stix_shifter_utils.utils.error_response import ErrorResponder
import pandas as pd
from stix_shifter_utils.utils import logger
from azure.monitor.query import LogsQueryStatus
from azure.core.exceptions import ODataV4Format, HttpResponseError, ClientAuthenticationError
from datetime import datetime, timedelta
import re
import jsonref
import copy
from stix_shifter_modules.azure_log_analytics.stix_translation.query_constructor import QueryStringPatternTranslator, \
    CONFIG_MAP_PATH


class Connector(BaseJsonSyncConnector):

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]
        self.api_client = APIClient(connection, configuration)

    async def ping_connection(self):
        """Ping the endpoint."""
        return_obj = {}
        response_dict = {}
        try:
            response = await self.api_client.ping_box()
            response_code = response.code
            response_dict = json.loads(response.read())

            if 200 <= response_code < 300:
                return_obj['success'] = True
            elif response_code == 404:
                if 'PathNotFoundError' in str(response_dict) or 'WorkspaceNotFoundError' in str(response_dict):
                    response_dict['code'] = 404
                    response_dict['message'] = "Invalid Parameter: workspaceId"
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except ClientAuthenticationError as ex:
            if 'invalid_resource' in str(ex):
                response_dict['code'] = 500
                response_dict['message'] = "Invalid Host/Port"
            else:
                response_dict['code'] = 401
                response_dict['message'] = "Invalid Authentication"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except ValueError as ex:
            if "Invalid tenant" in str(ex):
                response_dict['message'] = "Invalid Parameter: tenant"
            else:
                response_dict['message'] = "Invalid Parameter"
            response_dict['code'] = 404
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except TimeoutError as ex:
            response_dict['code'] = 408
            response_dict['message'] = 'TimeoutError ' + str(ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except Exception as ex:
            response_dict['message'] = ex
            self.logger.error('error when getting search results: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    async def delete_query_connection(self, search_id):
        """"delete_query_connection response
        :param search_id: str, search_id"""
        return {"success": True, "search_id": search_id}

    async def create_results_connection(self, query, offset, length):
        """"built the response object
        :param query: str, search_id
        :param offset: int,offset value
        :param length: int,length value"""
        return_obj = {}
        response_dict = {}

        try:
            length = int(length)
            offset = int(offset)
            return_obj = dict()
            query = """{query} | serialize rn = row_number() | where rn >= {offset} | limit {len}""".format(query=query,
                                                                                            offset=offset, len=length)
            matches = re.findall(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+?Z)', query)
            if matches:
                stop_time = datetime.strptime(matches[len(matches) - 1].replace('Z', ""), "%Y-%m-%dT%H:%M:%S.%f")
                start_time = datetime.strptime(matches[len(matches) - 2].replace('Z', ""), "%Y-%m-%dT%H:%M:%S.%f")
            else:
                stop_time = datetime.utcnow()
                start_time = stop_time - timedelta(hours=24)

            response = await self.api_client.run_search(query, start_time, stop_time)

            if response["success"]:
                if response["response"].status == LogsQueryStatus.PARTIAL:
                    error = response["response"].partial_error
                    data = response["response"].partial_data
                    self.logger.warn(error.message)
                elif response["response"].status == LogsQueryStatus.SUCCESS:
                    data = response["response"].tables

                for table in data:
                    df = pd.DataFrame(data=table.rows, columns=table.columns)
                    return_obj = {"success": True, "data": df.astype(str).to_dict(orient='records')}
                    return_obj['data'] = self.format_response(return_obj['data'])

        except ClientAuthenticationError as ex:
            if 'invalid_resource' in str(ex):
                response_dict['code'] = 500
                response_dict['message'] = "Invalid Host/Port"
            else:
                response_dict['code'] = 401
                response_dict['message'] = "Invalid Authentication"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except HttpResponseError as ex:
            if isinstance(ex.error, ODataV4Format):
                if 'PathNotFoundError' in str(ex.error) or 'WorkspaceNotFoundError' in str(ex.error):
                    response_dict['code'] = 404
                    response_dict['message'] = "Invalid Parameter: workspaceId"
                else:
                    response_dict['code'] = 400
                    response_dict['message'] = "Invalid Query"
            else:
                response_dict['code'] = 500
                response_dict['message'] = "Invalid Host/Port"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except ValueError as ex:
            if "Invalid tenant" in str(ex):
                response_dict['message'] = "Invalid Parameter: tenant"
            else:
                response_dict['message'] = "Invalid Parameter"
            response_dict['code'] = 404
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except TimeoutError as ex:
            response_dict['code'] = 408
            response_dict['message'] = 'TimeoutError ' + str(ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except Exception as ex:
            response_dict['message'] = ex
            self.logger.error('error when getting search results: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    def format_response(self, data):
        """ Format the API responses
        :param data: list
        :return: list """

        for row in data:
            copied_row = copy.deepcopy(row)
            try:
                # formatting security alert response
                if row.get("Type") == "SecurityAlert":
                    row = self.format_security_alert(row)
                # formatting security incident response
                elif row.get("Type") == 'SecurityIncident':
                    row = self.format_security_incident(row)
                # formatting security event response
                elif row.get("Type") == "SecurityEvent":
                    if row.get('FileHash'):
                        row = self.find_filehash_map(row)
            except:
                row = copied_row
        return data

    def format_security_alert(self, security_alert):
        """ Format the security alert response
        :param security_alert: dict
        :return: dict """

        if security_alert.get("ExtendedProperties"):
            security_alert["ExtendedProperties"] = json.loads(security_alert["ExtendedProperties"])

        if security_alert.get("RemediationSteps"):
            if '{' not in security_alert["RemediationSteps"] and '}' not in security_alert["RemediationSteps"]:
                security_alert["RemediationSteps"] = ' '.join(json.loads(security_alert["RemediationSteps"]))

        if security_alert.get("Entities"):
            entity_list = json.loads(security_alert["Entities"].replace('$ref":"', '$ref":"#'))
            entity_dict = {}
            for _dict in entity_list:
                if _dict.get("$id"):
                    _dict = self.add_account_type(_dict)
                    entity_dict[_dict["$id"]] = _dict
            entity_dict = self.remove_unwanted_ref(entity_dict)
            security_alert['entity'] = json.loads(json.dumps(jsonref.loads(json.dumps(entity_dict)), indent=1))
            if security_alert.get('entity'):
                result = self.format_security_type(security_alert['entity'])
                if result:
                    security_alert['Entities'] = self.remove_duplicates(result)
        return security_alert

    def format_security_incident(self, security_incident):
        """ Format the security incident response
        :param security_incident: dict
        :return: dict """
        if security_incident.get("AdditionalData"):
            security_incident["AdditionalData"] = json.loads(security_incident["AdditionalData"])
            if security_incident["AdditionalData"].get('tactics'):
                security_incident["AdditionalData"]['tactics'] = \
                    ', '.join(security_incident["AdditionalData"]['tactics'])
            if security_incident["AdditionalData"].get('techniques'):
                security_incident["AdditionalData"]['techniques'] = \
                    ', '.join(security_incident["AdditionalData"]['techniques'])
            else:
                security_incident["AdditionalData"]['techniques'] = None
        if security_incident.get("Owner"):
            security_incident["Owner"] = json.loads(security_incident["Owner"])

        if security_incident.get("AlertIds"):
            security_incident["AlertIds"] = json.loads(security_incident["AlertIds"])

        if security_incident.get("ProviderName"):
            security_incident["ProviderNameIncident"] = security_incident["ProviderName"]
            security_incident["ProviderName"] = None

        return security_incident

    @staticmethod
    def format_security_type(entity):
        """ Convert the type as dict key
        :param entity: list
        :return: dict """
        result = {}
        for obj in entity:
            if entity[obj].get("Type"):
                if entity[obj].get("Type") == 'file':
                    filehash = {}
                    for row in entity[obj].get("FileHashes", []):
                        if row.get("Algorithm") and row.get("Value"):
                            filehash[row["Algorithm"]] = row["Value"]
                    if filehash:
                        entity[obj]["FileHashes"] = filehash

                if entity[obj].get("Type") == 'process' and entity[obj].get('ImageFile'):
                    filehash = {}
                    for row in entity[obj]['ImageFile'].get("FileHashes", []):
                        if row.get("Algorithm") and row.get("Value"):
                            filehash[row["Algorithm"]] = row["Value"]
                    if filehash:
                        entity[obj]['ImageFile']["FileHashes"] = filehash

                if entity[obj].get("Type") == 'process' and entity[obj].get("ParentProcess") and \
                        entity[obj]["ParentProcess"].get('ImageFile'):
                    filehash = {}
                    for row in entity[obj]["ParentProcess"]['ImageFile'].get("FileHashes", []):
                        if row.get("Algorithm") and row.get("Value"):
                            filehash[row["Algorithm"]] = row["Value"]
                    if filehash:
                        entity[obj]["ParentProcess"]['ImageFile']["FileHashes"] = filehash

                if entity[obj]["Type"] in result:
                    if isinstance(result[entity[obj]["Type"]], list):
                        result[entity[obj]["Type"]].append(entity[obj])
                    else:
                        result[entity[obj]["Type"]] = [result[entity[obj]["Type"]], entity[obj]]
                else:
                    result[entity[obj]["Type"]] = entity[obj]
        return result

    @staticmethod
    def find_filehash_map(obj):
        """ Find file hash mappings based on length
        :param obj: obj
        :return: obj """
        if re.compile("^[a-f0-9]{32}$").match(obj["FileHash"]):
            obj['MD5'] = obj["FileHash"]
        elif re.compile(r'\b[0-9a-f]{40}\b').match(obj["FileHash"]):
            obj['SHA1'] = obj["FileHash"]
        elif re.compile("[A-Fa-f0-9]{64}").match(obj["FileHash"]):
            obj['SHA256'] = obj["FileHash"]
        return obj

    @staticmethod
    def remove_duplicates(data):
        """ Remove the duplicated records
        :param data: dict
        :return: dict """
        copied_data = copy.deepcopy(data)
        for key, value in data.items():
            if isinstance(value, list):
                for index, val in enumerate(value):
                    if str(value).count("{'$id': '" + val.get('$id')) > 1:
                        copied_data[key].remove(val)
        return copied_data

    @staticmethod
    def add_account_type(_dict):
        """ Add the account type as dict key
        :param _dict: dict
        :return: dict """
        if _dict.get('IsDomainJoined') is True:
            _dict["AccountType"] = "windows-domain"
        elif _dict.get('IsDomainJoined') is False:
            _dict["AccountType"] = "windows-local"
        return _dict

    @staticmethod
    def remove_unwanted_ref(entity):
        """ Remove the unwanted references
        :param entity: dict
        :return: dict """
        keys = entity.keys()
        for key, value in entity.items():
            ref_list = re.findall(r"ref': '#([^>]*?)'", str(value))
            for ref in ref_list:
                if ref not in keys:
                    entity[key] = json.loads(json.dumps(entity[key]).replace(f'$ref": "#{ref}', f'ref": "#{ref}'))
        return entity
