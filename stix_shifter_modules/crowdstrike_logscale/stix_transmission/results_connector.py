from stix_shifter_utils.modules.base.stix_transmission.base_json_results_connector import BaseJsonResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from .status_connector import StatusConnector
from .delete_connector import DeleteConnector
import regex
import json
from flatten_json import unflatten

class InvalidSearchIdException(Exception):
    pass

# LogScale event fields starts with @timestamp and @error_msg will be overwritten while un-flattening.
# These fields are excluded while un flattening
DS_FLATTEN_KEY_EXCLUDE = ["@timestamp", "@error_msg"]


class ResultsConnector(BaseJsonResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def create_results_connection(self, search_id, offset, length, metadata=None):
        """
        Poll the query Job to fetch the results of the search
        :param search_id:  str
        :param offset: str
        :param length: str
        :param metadata: dict
        :return: return_obj, dict
        """

        return_obj = {}
        response_dict = {}
        result_response_json = {}
        source = ""
        try:
            offset = int(offset)
            length = int(length)

            if metadata:
                # Fetch the query from metadata and create a new job id to fetch the next set of results through pagination
                if isinstance(metadata, str):
                    metadata = json.loads(metadata)
                if metadata.get('query') and metadata.get('source'):
                    source = metadata['source']
                    query = metadata['query']
                    query['around']['numberOfEventsBefore'] = length
                    query_response = await self.api_client.create_search(query)
                    query_response_content = query_response.read().decode('utf-8')
                    if query_response.code == 200:
                        query_response_text = json.loads(query_response_content)
                        search_id = query_response_text['id']
                    else:
                        return self.handle_api_exception(query_response.code, query_response_content)
            else:
                if ":" not in search_id:
                    raise InvalidSearchIdException
                source = search_id.split(":")[-1]
                search_id = search_id.split(":")[0]
            result_response = await self.api_client.get_search_results(search_id)
            result_response_text = result_response.read().decode('utf-8')
            if result_response.code == 200:
                return_obj['success'] = True
                result_response_json = json.loads(result_response_text)
                if not metadata or (metadata and result_response_json.get('done')):
                    data = result_response_json['events']
                else:
                    return_obj, data = await self.fetch_status_and_response(search_id, length)
            else:
                return_obj = self.handle_api_exception(result_response.code, result_response_text)
                data = []
            if data:
                if metadata:
                    data = [{source: self.unflatten_json(event)} for event in data]
                    # update the around parameter with last event details to fetch the next set of records in pagination
                    metadata['query']['around'] = {"eventId": data[-1][source]['@id'], "numberOfEventsAfter": 0,
                                                   "numberOfEventsBefore": 0,
                                                   "timestamp": data[-1][source]['@timestamp']}
                    metadata['query']['end'] = data[-1][source]['@timestamp']
                    return_obj['metadata'] = metadata
                    return_obj['data'] = data

                else:
                    data = [{source: self.unflatten_json(event)} for event in data[offset: (offset + length)]]
                    # Remove the tail function from the QueryString, since around parameter will be used for pagination
                    # in further iterations as tail function and around parameter cannot be used in same query
                    querystring = result_response_json.get('metaData').get('filterQuery').get('queryString')
                    tail_index = querystring.find("| tail")
                    formatted_query = querystring[:tail_index] if tail_index != -1 else querystring
                    # Create the input query string, around parameter to fetch the next set of records using the last event from the response
                    input_query = {
                        "queryString": formatted_query,
                        "start": result_response_json['metaData']['filterQuery']['start'],
                        "end": data[-1][source]['@timestamp'],
                        "around": {"eventId": data[-1][source]['@id'], "numberOfEventsAfter": 0,
                                   "numberOfEventsBefore": 0, "timestamp": data[-1][source]['@timestamp']}
                    }
                    return_obj['metadata'] = {"query": input_query, "source": source}
                    return_obj['data'] = data

            else:
                if not return_obj.get('error') and return_obj.get('success') is not False:
                    return_obj['success'] = True
                    return_obj['data'] = []
            if metadata:
                # deleting the internal query jobs that has been created for pagination
                delete_obj = DeleteConnector(self.api_client)
                await delete_obj.delete_query_connection(search_id)

        except InvalidSearchIdException:
            return_obj = self.handle_api_exception(404,"Invalid Search Id")

        except Exception as ex:
            if "timeout_error" in str(ex):
                response_dict['code'] = 408
            response_dict['message'] = str(ex)
            self.logger.error('error while getting results in Crowdstrike Falcon Logscale: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        return return_obj

    def handle_api_exception(self, code, response_txt):
        """
        create the exception response
        :param code, int
        :param response_txt, dict
        :return: return_obj, dict
        """
        return_obj = {}
        response_dict = {'code': code, 'message': str(response_txt)} if code else {'message': str(response_txt)}
        ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    async def fetch_status_and_response(self, search_id, length):
        """
        Fetch the status and results of the intermediate query job
        :param search_id: str
        :param length: int
        :return: return_obj, dict: data, list
        """
        return_obj = {}
        status_obj = StatusConnector(self.api_client)
        status = await status_obj.create_status_connection(search_id)
        if status['success']:
            # check if the intermediate queryjob's status is still running
            while status.get('progress') < 100 and status.get('status') == 'RUNNING':
                status = await status_obj.create_status_connection(search_id,{'length':length})
                if status['success'] is False:
                    return status, []
            if status.get('status') == 'CANCELED':
                return_obj['success'] = True
                return return_obj, []
            # Fetch the response if the intermediate queryjob's status is completed
            next_response = await self.api_client.get_search_results(search_id)
            next_response_text = next_response.read().decode('utf-8')
            if next_response.code == 200:
                return_obj['success'] = True
                response_json = json.loads(next_response_text)
                data = response_json['events']
            else:
                return_obj = self.handle_api_exception(next_response.code, next_response_text)
                data = []
        else:
            return status, []
        return return_obj, data

    def unflatten_json(self, flatten_json):
        """
        Unflatten the flattened JSON event
        :param flatten_json: dict
        :return res,dict
        """
        res = {}
        # Excluded flatten keys
        excluded_keys = [key for key in flatten_json if key.startswith(tuple(DS_FLATTEN_KEY_EXCLUDE))]

        # copy excluded items to res and remove from flatten_json
        for key in excluded_keys:
            res[key] = flatten_json.pop(key)

        unflatten_json = unflatten(flatten_json, separator='.')
        # Format array indexed keys to proper json format
        unflatten_json = self.format_indexed_keys(unflatten_json)
        res.update(unflatten_json)
        res['finding_type'] = 'alert'
        return res

    def format_indexed_keys(self, event):
        """
        Format array indexed string keys to single key
        :param event: dict
        :return res,dict
        """
        res = {}
        for key, value in event.items():
            match = regex.search(r'(.*)\[(\d+)\]$', key)
            if match:
                indexed_key, _ = match.groups()
                val = res.get(indexed_key, {}) or []
                if isinstance(value, dict):
                    response = self.format_indexed_keys(value)
                    val.append(response)
                else:
                    if value != {} and value != '' and value != [] and value is not None:
                        val.append(value)
                res[indexed_key] = val
            else:
                if isinstance(value, dict):
                    value = self.format_indexed_keys(value)
                if value != {} and value != '' and value != [] and value is not None:
                    res[key] = value
        return res
