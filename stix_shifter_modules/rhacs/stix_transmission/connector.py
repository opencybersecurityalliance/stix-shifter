import json
from requests.exceptions import ConnectionError, RetryError
from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from .api_client import APIClient


class InvalidAuthenticationException(Exception):
    pass


class Connector(BaseJsonSyncConnector):
    """connector class"""

    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def create_results_connection(self, query, offset, length):
        """
        Fetching the results using query, offset and length
        :param query: str, Data Source query
        :param offset: str, Offset value
        :param length: str, Length value
        :return: dict
        """
        try:
            return_obj = {}
            response_dict = {}

            min_range = int(offset)
            max_range = int(offset) + int(length)

            if max_range > int(self.api_client.get_limit()):
                max_range = int(self.api_client.get_limit())

            """api call for searching alert based on query"""
            response_wrapper = await self.api_client.get_search_results(query)
            response_code = response_wrapper.code
            response_dict = json.loads(response_wrapper.read())

            if response_code == 200:
                return_obj['success'] = True
            elif response_code == 401:
                raise InvalidAuthenticationException(response_dict)
            total_data = []
            total_count = 0
            for firstresult in response_dict['alerts']:
                # exit if result limit crossed
                if total_count > max_range:
                    break
                if firstresult['id'] is not None:
                    """second level api call for getting details of particular alert id"""
                    inner_data = await self.api_client.get_inner_results(firstresult['id'])
                    inner_dict = json.loads(inner_data.read())
                    dt = {}
                    dt_main = {}
                    is_process_or_netflow = False
                    commondataset = {}
                    commondataset = Connector.get_common_data(inner_dict)

                    if inner_dict.get('deployment') is not None:
                        if inner_dict['deployment']['containers'] is not None:
                            dt['Container'] = Connector.flatten_container_data(
                                inner_dict['deployment']['containers'])

                    if inner_dict.get('violations') is not None and \
                            len(inner_dict.get('violations')) > 0:
                        for container in dt['Container']:
                            # exit if result limit crossed
                            if total_count > max_range:
                                break
                            for item in inner_dict.get('violations'):
                                if item.get('networkFlowInfo') is not None:
                                    is_process_or_netflow = True
                                    if item['time'] is not None:
                                        commondataset["firstObserved"] = item['time']
                                        commondataset["lastObserved"] = item['time']
                                    else:
                                        commondataset["firstObserved"] = inner_dict['firstOccurred']
                                        commondataset["lastObserved"] = inner_dict['firstOccurred']
                                    if item['message'] is not None:
                                        commondataset["violationMessage"] = item['message']. \
                                            replace("\'", '\"')
                                    """creating the result set based on network flow data"""
                                    dt_main = Connector.get_result_set(None, container,
                                                                       item, commondataset)
                                    total_data.append(dt_main)
                                    total_count = total_count + 1
                                    # exit if result limit crossed
                                    if total_count > max_range:
                                        break
                    """Check containers info available in api response"""
                    if inner_dict.get('deployment').get('containers') is not None:
                        for container in dt['Container']:
                            # exit if result limit crossed
                            if total_count > max_range:
                                break
                            if inner_dict.get('processViolation') is not None \
                                    and len(inner_dict['processViolation']['processes']) > 0:
                                is_process_or_netflow = True
                                if inner_dict.get('processViolation').get('message') is not None:
                                    commondataset["violationMessage"] = \
                                        inner_dict['processViolation']['message']. \
                                            replace("\'", '\"')

                                for proc in inner_dict['processViolation']['processes']:
                                    if proc['containerName'] == container['containerName']:
                                        if proc.get('signal').get('time') is not None:
                                            commondataset["firstObserved"] = proc['signal']['time']
                                            commondataset["lastObserved"] = proc['signal']['time']
                                        else:
                                            commondataset["firstObserved"] = \
                                                inner_dict['firstOccurred']
                                            commondataset["lastObserved"] = \
                                                inner_dict['firstOccurred']
                                        """creating the result set based on
                                         process violation data"""
                                        dt_main = Connector.get_result_set(proc, container, None,
                                                                           commondataset)
                                        total_data.append(dt_main)
                                        total_count = total_count + 1
                                        # exit if result limit crossed
                                        if total_count > max_range:
                                            break
                    """When alert api response does not have process or Netflow data"""
                    if is_process_or_netflow is False:
                        allcontainer = dt.get('Container')
                        if inner_dict.get('violations') is not None and \
                                len(inner_dict.get('violations')) > 0:
                            commondataset["findingType"] = 'alert'
                            for item in inner_dict.get('violations'):
                                # exit if result limit crossed
                                if total_count > max_range:
                                    break
                                commondataset["violationMessage"] = item['message']. \
                                    replace("\'", '\"')

                                if item.get('time') is not None and item['time'] != 'null':
                                    commondataset["firstObserved"] = item['time']
                                    commondataset["lastObserved"] = item['time']
                                else:
                                    commondataset["firstObserved"] = inner_dict.get('firstOccurred')
                                    commondataset["lastObserved"] = inner_dict.get('firstOccurred')

                                if allcontainer is None:
                                    """
                                    creating result set when no process or network flow 
                                    violation and no container
                                    """
                                    dt_main = Connector.get_result_set(None, None, None,
                                                                       commondataset)
                                    total_data.append(dt_main)
                                    total_count = total_count + 1
                                elif len(allcontainer) > 0:
                                    for itm in allcontainer:
                                        """
                                        creating result set when no process or 
                                        network flow violation but having container
                                        """
                                        dt_main = Connector.get_result_set(None, itm, None,
                                                                           commondataset)
                                        total_data.append(dt_main)
                                        total_count = total_count + 1
                                        # exit if result limit crossed
                                        if total_count > max_range:
                                            break

            return_obj['data'] = total_data[min_range:max_range] if total_data else []

        except InvalidAuthenticationException:
            response_dict['type'] = "AuthenticationError"
            response_dict['message'] = "Invalid Authentication"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'],
                                      connector=self.connector)
        except ConnectionError:
            response_dict['type'] = "ConnectionError"
            response_dict['message'] = "Invalid Host/Port"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'],
                                      connector=self.connector)
        except RetryError:
            response_dict['type'] = "RetryError"
            response_dict['message'] = "Invalid parameter or Url"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'],
                                      connector=self.connector)
        except Exception as ex:
            response_dict['type'] = ex.__class__.__name__
            response_dict['message'] = ex
            self.logger.error('error when getting search results: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'],
                                      connector=self.connector)
        return return_obj

    async def ping_connection(self):
        """
        Ping the endpoint
        :return: dict
        """
        return_obj = {}
        response_dict = {}
        try:
            response = await self.api_client.ping_data_source()
            response_code = response.code
            response_dict = json.loads(response.read())
            if response_code == 200 and response_dict['status'] == 'ok':
                return_obj['success'] = True
        except RetryError:
            response_dict['type'] = "RetryError"
            response_dict['message'] = "Invalid parameter or Url"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'],
                                      connector=self.connector)
        except ConnectionError:
            response_dict['type'] = "ConnectionError"
            response_dict['message'] = "Invalid Host/Port"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'],
                                      connector=self.connector)
        except Exception as ex:
            response_dict['type'] = ex.__class__.__name__
            response_dict['message'] = ex
            self.logger.error('error while pinging: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'],
                                      connector=self.connector)
        return return_obj

    async def delete_query_connection(self, search_id):
        """
        Delete query is not supported in rhacs
        :return: success
        """
        return {"success": True, "search_id": search_id}

    @staticmethod
    def get_common_data(commondata=None):
        dt_common = {}
        if commondata is not None:
            dt_common['findingType'] = 'violation'
            if commondata.get('id') is not None:
                dt_common['alertId'] = commondata.get('id')
            if commondata.get('policy') is not None:
                if commondata['policy'].get('name') is not None:
                    dt_common['policyName'] = commondata['policy']['name']
                if commondata['policy'].get('id') is not None:
                    dt_common['policyId'] = commondata['policy']['id']
                if commondata['policy'].get('description') is not None:
                    dt_common['description'] = commondata['policy']['description']. \
                        replace("\'", '\"')
                if commondata['policy'].get('rationale') is not None:
                    dt_common['rationale'] = commondata['policy']['rationale']. \
                        replace("\'", '\"')
                if commondata['policy'].get('remediation') is not None:
                    dt_common['remediation'] = commondata['policy']['remediation']. \
                        replace("\'", '\"')
                if commondata['policy'].get('disabled') is not None:
                    dt_common['disabled'] = commondata['policy']['disabled']
                if (commondata['policy']['categories'] is not None and len(
                        commondata['policy']['categories']) > 0):
                    dt_common['categories'] = commondata['policy']['categories']
                if (commondata['policy']['severity'] is not None and
                        commondata['policy']['severity'] != ''):
                    dt_common['severity'] = commondata['policy']['severity']
                if commondata['policy'].get('eventSource') is not None:
                    dt_common['eventSource'] = commondata['policy']['eventSource']
                if commondata['policy'].get('lastUpdated') is not None:
                    dt_common['lastUpdated'] = commondata['policy'].get('lastUpdated')
                if commondata['policy'].get('SORTName') is not None:
                    dt_common['sortName'] = commondata['policy']['SORTName']
                if commondata['policy'].get('SORTLifecycleStage') is not None:
                    dt_common['sortLifecycleStage'] = commondata['policy']['SORTLifecycleStage']

            if commondata.get('lifecycleStage') is not None:
                dt_common['lifecycleStage'] = commondata['lifecycleStage']
            if commondata.get('clusterId') is not None:
                dt_common['clusterId'] = commondata['clusterId']
            if commondata.get('clusterName') is not None:
                dt_common['cluster'] = commondata['clusterName']
            if commondata.get('namespace') is not None:
                dt_common['namespace'] = commondata['namespace']
            if commondata.get('namespaceId') is not None:
                dt_common['namespaceId'] = commondata['namespaceId']
            if commondata.get('state') is not None:
                dt_common['violationState'] = commondata['state']
            if commondata.get('deployment') is not None:
                dt_common['deployment'] = commondata['deployment']['name']
                dt_common['deploymentId'] = commondata['deployment']['id']
                dt_common['inactive'] = commondata['deployment']['inactive']
        return dt_common

    @staticmethod
    def get_result_set(proc=None, containerdata=None, netflowdata=None, commondt=None):
        """
            Get Customise api result
            :param proc: Process Violation
            :param containerdata: container detail
            :param netflowdata: netflow data
            :return:dict
        """
        dt_new = {}
        for key in commondt.keys():
            dt_new[key] = commondt[key]

        if proc is not None:
            dt_inner = {}
            dt_inner['name'] = proc['signal']['name']
            if proc['signal']['args'] is not None:
                if proc['signal']['args'].find(" ") != -1:
                    dt_inner['args'] = proc['signal']['args'].replace('"', '')\
                        .replace("'", '').strip().split(' ')
                else:
                    dt_inner['args'] = proc['signal']['args'].replace('"', '')\
                        .replace("'", '').strip()

            dt_inner['pid'] = proc['signal']['pid']
            dt_inner['execFilePath'] = proc['signal']['execFilePath']
            dt_inner['time'] = proc['signal']['time']
            dt_inner['id'] = str(proc['id'])
            if (proc['signal']['uid'] is not None) and (str(proc['signal']['uid']) != ''):
                dt_inner['uid'] = str(proc['signal']['uid'])
            if (proc['signal']['gid'] is not None) and (str(proc['signal']['gid']) != ''):
                dt_inner['gid'] = str(proc['signal']['gid'])

            dt_inner['podId'] = str(proc['podId'])
            if proc['podUid'] is not None and str(proc['podUid']) != "0":
                dt_inner['podUid'] = str(proc['podUid'])
            dt_new['process'] = dt_inner

        if containerdata is not None:
            if containerdata.get('containerName') is not None:
                dt_new['containerName'] = containerdata['containerName']
            if containerdata.get('containerImage') is not None:
                dt_container = {}
                dt_containernm = {}
                dt_container['id'] = containerdata['containerImage'].get('id')

                dt_containernm['registry'] = containerdata['containerImage'].get('name').get('registry')
                dt_containernm['remote'] = containerdata['containerImage'].get('name').get('remote')
                dt_containernm['tag'] = containerdata['containerImage'].get('name').get('tag')
                dt_containernm['fullName'] = containerdata['containerImage'].get('name') \
                    .get('fullName')

                dt_container['name'] = dt_containernm

                dt_new['containerImage'] = dt_container

        if netflowdata is not None:
            dt_netflow = {}
            dt_netflow['netflow_protocol'] = netflowdata.get('networkFlowInfo').get('protocol')
            dt_source = {}

            dt_source['name'] = netflowdata.get('networkFlowInfo').get('source').get('name')
            dt_source['entity_type'] = netflowdata.get('networkFlowInfo').get('source') \
                .get('entityType')
            dt_source['deployment_namespace'] = netflowdata.get('networkFlowInfo').get('source') \
                .get('deploymentNamespace')
            dt_source['deployment_type'] = netflowdata.get('networkFlowInfo').get('source') \
                .get('deploymentType')
            dt_source['port'] = netflowdata.get('networkFlowInfo').get('source').get('port')

            dt_netflow['netflow_source'] = dt_source

            dt_destination = {}
            dt_destination['name'] = netflowdata.get('networkFlowInfo').get('destination') \
                .get('name')
            dt_destination['entity_type'] = netflowdata.get('networkFlowInfo').get('destination') \
                .get('entityType')
            dt_destination['deployment_namespace'] = netflowdata.get('networkFlowInfo'). \
                get('destination').get('deploymentNamespace')
            dt_destination['deployment_type'] = netflowdata.get('networkFlowInfo') \
                .get('destination').get('deploymentType')
            dt_destination['port'] = netflowdata.get('networkFlowInfo').get('destination') \
                .get('port')

            dt_netflow['netflow_destination'] = dt_destination

            dt_new['networkFlow'] = dt_netflow
        return dt_new

    @staticmethod
    def flatten_container_data(inner_dict):
        """
           flatten container data
           :param inner_dict: container data
           :return:list
        """
        dtlist = []
        if inner_dict is not None:
            for item in inner_dict:
                dt_new = {}
                dt_new['containerName'] = item['name']
                if item['image'] is not None:
                    dt_new['containerImage'] = item['image']
                dtlist.append(dt_new)
        return dtlist
