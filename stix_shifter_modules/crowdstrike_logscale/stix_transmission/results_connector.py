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
class InvalidMetadataException(Exception):
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
        Fetch the results of the search by creating and polling the query job
        :param search_id:  str
        :param offset: str
        :param length: str
        :param metadata: dict
        :return: return_obj, dict
        """
        response_dict = {}
        return_obj = {}
        response_query_status_details = {}
        try:
            offset = int(offset)
            length = int(length)
            data = []
            total_records = self.fetch_total_records(metadata, offset, length)
            first_iteration = False
            if not metadata:
                first_iteration = True   # setting the variable to apply offset and length on data when metadata is not passed as input
                return_obj, data, metadata, response_query_status_details = await self.process_first_query_job(search_id, data, total_records)
            if metadata:
                while len(data) < total_records:
                    job_id = await self.fetch_query_job_id(metadata, self.api_client.api_page_size)
                    if isinstance(job_id,dict):
                        return job_id
                    return_obj, response_query_status_details = await self.fetch_status_and_response(job_id, length)
                    if not return_obj.get('success'):
                        break
                    if return_obj.get('data'):
                        data.extend(return_obj['data'])
                        #prepare metadata for next iteration
                        metadata = ResultsConnector.prepare_metadata(return_obj['data'], response_query_status_details)
                    else:
                        break
                    # deleting the internal query jobs that has been created for pagination
                    delete_obj = DeleteConnector(self.api_client)
                    await delete_obj.delete_query_connection(job_id)

            if data:
                return_obj = await self.format_results(data, offset,total_records, first_iteration)
                if (offset + len(return_obj['data'])) < self.api_client.result_limit:
                    return_obj['metadata'] = ResultsConnector.prepare_metadata(return_obj['data'], response_query_status_details)

        except InvalidSearchIdException:
            return_obj = self.handle_api_exception(404,"Invalid Search Id")

        except InvalidMetadataException:
            return_obj = self.handle_api_exception(101, "Invalid Metadata")

        except Exception as ex:
            if "timeout_error" in str(ex):
                response_dict['code'] = 408
            response_dict['message'] = str(ex)
            self.logger.error('error while getting results in Crowdstrike Falcon Logscale: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        return return_obj

    def handle_api_exception(self, code, response_txt):
        """
        Create the exception response
        :param code, int
        :param response_txt, dict
        :return: return_obj, dict
        """
        return_obj = {}
        response_dict = {'code': code, 'message': str(response_txt)} if code else {'message': str(response_txt)}
        ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    async def process_first_query_job(self, search_id, data, total_records):
        """
        Fetch the response of the First Query Job Id
        :param search_id: str
        :param data: list
        :param total_records: int
        :return: dict
        """
        metadata = {}
        if ":" not in search_id:
            raise InvalidSearchIdException
        # split the input search id which is in the format job_id:source into individual fields for fetching results
        job_id = search_id.split(":")[0]
        return_obj, response_query_status_details = await self.fetch_query_job_response(job_id)
        if return_obj['success']:
            if return_obj.get('data'):
                data.extend(return_obj['data'])
                if len(return_obj['data']) < total_records:
                    metadata = ResultsConnector.prepare_metadata(return_obj['data'], response_query_status_details)
        else:
            return return_obj, data, metadata, response_query_status_details
        return {}, data, metadata, response_query_status_details
    async def format_results(self, data, offset, total_records, first_iteration):
        """
        Slice the records and format the results
        :param data: dict
        :param offset: int
        :param total_records: int
        :param first_iteration: bool
        :return: dict
        """
        if first_iteration:
            formatted_data = [self.unflatten_json(event) for event in data[offset: total_records]]
        else:
            formatted_data = [self.unflatten_json(event) for event in data[:total_records]]

        return_obj = {'success': True, 'data': formatted_data}
        return return_obj

    def fetch_total_records(self,metadata, offset, length):
        """
        Calculate the value of total records to be fetched based on metadata
        :param metadata: dict
        :param offset: int
        :param length: int
        :return: int
        """
        if not metadata:
            total_records = offset + length
            if self.api_client.result_limit < total_records:
                total_records = self.api_client.result_limit
        else:
            records_fetched = offset
            total_records = length
            if abs(self.api_client.result_limit - records_fetched) < total_records:
                total_records = abs(self.api_client.result_limit - records_fetched)
        return total_records
    async def fetch_query_job_id(self,metadata, length):
        """
        Create a new job id using metadata
        :param metadata: dict
        :param length: int
        :return: dict/str
        """
        # Fetch the input details from metadata and create a new job id to fetch the next set of results through pagination
        if isinstance(metadata, str):
            metadata = json.loads(metadata)
        if (metadata.get('last_event_id') and metadata.get('last_event_timestamp') and
                metadata.get('input_query_string') and metadata.get('start')):
            search_query = {
                'queryString': metadata['input_query_string'],
                'around': {"eventId" : metadata['last_event_id'],
                           "numberOfEventsAfter" : 0,
                           "numberOfEventsBefore" : length,
                           "timestamp" : metadata['last_event_timestamp']},
                'start': metadata['start'],
                'end': metadata['last_event_timestamp']
            }
            query_response = await self.api_client.create_search(search_query)
            query_response_content = query_response.read().decode('utf-8')
            if query_response.code == 200:
                query_response_text = json.loads(query_response_content)
                job_id = query_response_text['id']
            else:
                return self.handle_api_exception(query_response.code, query_response_content)
        else:
            raise InvalidMetadataException
        return job_id

    async def fetch_status_and_response(self, search_id, length):
        """
        Fetch the status and results of the intermediate query job
        :param search_id: str
        :param length: int
        :return: dict,dict
        """
        return_obj = {}
        status_obj = StatusConnector(self.api_client)
        status = await status_obj.create_status_connection(search_id)
        if status['success']:
            # check if the intermediate queryjob's status is still running
            while status.get('progress') < 100 and status.get('status') == 'RUNNING':
                status = await status_obj.create_status_connection(search_id,{'length':length})
                if status['success'] is False:
                    return status, {}
            if status.get('status') == 'CANCELED':
                return_obj['success'] = True
                return_obj['data'] = []
                return return_obj, {}
            # Fetch the response if the intermediate queryjob's status is completed
            return await self.fetch_query_job_response(search_id)
        return status, {}

    async def fetch_query_job_response(self, search_id, metadata=None):
        """
        Fetch the results for the Query Job ID
        :param search_id: str
        :param metadata: dict
        :return: dict, dict
        """
        return_obj = {}
        response_query_status_details = {}
        result_response = await self.api_client.poll_query_job(search_id)
        result_response_text = result_response.read().decode('utf-8')
        if result_response.code == 200:
            return_obj['success'] = True
            result_response_json = json.loads(result_response_text)
            if not metadata or (metadata and result_response_json.get('done')):
                return_obj['data'] = result_response_json['events']
            # store the filter query details in order to prepare the metadata
            response_query_status_details = {'filterQuery': result_response_json['metaData']['filterQuery'],
                                            'done': result_response_json['done']
                                             }
        else:
            return_obj = self.handle_api_exception(result_response.code, result_response_text)

        return return_obj, response_query_status_details
    @staticmethod
    def prepare_metadata(data, response_query_status_details):
        """
        Create the metadata
        :param data: list
        :param response_query_status_details: dict
        :return: return_obj, dict
        """
        metadata = {}

        querystring = response_query_status_details.get('filterQuery').get('queryString')
        tail_index = querystring.find("| tail")
        formatted_query = querystring[:tail_index] if tail_index != -1 else querystring
        metadata['last_event_id'] = data[-1]['@id']   # -1 index represents the last record in the list
        metadata['last_event_timestamp'] = data[-1]['@timestamp']
        metadata['input_query_string'] = formatted_query
        metadata['start'] = response_query_status_details['filterQuery']['start']
        return metadata

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
