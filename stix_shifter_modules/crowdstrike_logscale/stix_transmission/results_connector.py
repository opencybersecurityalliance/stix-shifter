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
        Poll/create the query Job to fetch the results of the search
        :param search_id:  str
        :param offset: str
        :param length: str
        :param metadata: dict
        :return: return_obj, dict
        """
        response_dict = {}
        return_obj = {}
        try:
            offset = int(offset)
            length = int(length)

            job_id = await self.fetch_query_job_id(metadata, length, search_id)
            if isinstance(job_id,dict):
                return job_id
            return_obj, response_query_status_details = await self.fetch_query_job_response(job_id, metadata)
            if not response_query_status_details.get('done') and return_obj['success']:
                return_obj, response_query_status_details = await self.fetch_status_and_response(search_id, length)
            if return_obj.get('data'):
                return_obj, new_response_query_status_details = await (self.fetch_remaining_data_and_format_results
                                                                   (return_obj, offset,length, response_query_status_details, metadata, search_id))
                if new_response_query_status_details:
                    return_obj['metadata'] = ResultsConnector.prepare_metadata(return_obj['data'], new_response_query_status_details)
                else:
                    return_obj['metadata'] = ResultsConnector.prepare_metadata(return_obj['data'],
                                                                               response_query_status_details)
            if metadata:
                if return_obj.get('metadata'):
                    return_obj['metadata']['record_count'] += metadata.get('record_count',0)
                # deleting the internal query jobs that has been created for pagination
                delete_obj = DeleteConnector(self.api_client)
                await delete_obj.delete_query_connection(job_id)

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
        create the exception response
        :param code, int
        :param response_txt, dict
        :return: return_obj, dict
        """
        return_obj = {}
        response_dict = {'code': code, 'message': str(response_txt)} if code else {'message': str(response_txt)}
        ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    async def fetch_remaining_data_and_format_results(self, return_obj, offset,length, response_query_status_details, metadata, search_id):
        """
        Fetch the remaining records if the records are less than length and process the results
        :param return_obj: dict
        :param offset: int
        :param length: int
        :param response_query_status_details: dict
        :param metadata: dict
        :param search_id: str
        :return: dict
        """
        next_response_query_status_details = {}
        # If the records fetched is less than total records, create a new job id, and fetch the next set of results
        # using the event id of the last data which is fetched until now.

        if not metadata:
            total_records = offset + length
            if total_records > self.api_client.result_limit:
                total_records = self.api_client.result_limit
            if len(return_obj['data']) < total_records:
                new_metadata = ResultsConnector.prepare_metadata(return_obj['data'], response_query_status_details)
                job_id = await self.fetch_query_job_id(new_metadata, total_records - len(return_obj['data']), search_id)
                if isinstance(job_id, dict):
                    return job_id # return the dictionary in case of negative response
                next_return_object, next_response_query_status_details = await self.fetch_status_and_response(job_id, length)
                if next_return_object.get('success'):
                    return_obj['data'].extend(next_return_object['data'])
                else:
                    return next_return_object
                # delete the intermediate job id
                delete_obj = DeleteConnector(self.api_client)
                await delete_obj.delete_query_connection(job_id)

        if metadata:
            formatted_data = [self.unflatten_json(event) for event in return_obj['data']]
        else:
            formatted_data = [self.unflatten_json(event) for event in
                              return_obj['data'][offset: total_records]]

        return_obj['data'] = formatted_data
        return return_obj, next_response_query_status_details

    async def fetch_query_job_id(self,metadata, length, search_id):
        """
        Fetch the existing job id from search id or create a new job id using metadata
        :param metadata:
        :param length:
        :param search_id:
        :return:
        """
        if metadata:
            # Fetch the input details from metadata and create a new job id to fetch the next set of results through pagination
            if isinstance(metadata, str):
                metadata = json.loads(metadata)
            if (metadata.get('last_event_id') and metadata.get('last_event_timestamp') and
                    metadata.get('input_query_string') and metadata.get('start') and metadata.get('record_count')):
                remaining_records = abs(self.api_client.result_limit - metadata['record_count'])
                if length > remaining_records:
                    length = remaining_records
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
        else:
            if ":" not in search_id:
                raise InvalidSearchIdException
            # When metadata is None, split the input search id which is in the format job_id:source into individual fields for fetching results
            job_id = search_id.split(":")[0]
        return job_id

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
        Format the data and create/update the metadata
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
        metadata['record_count'] = len(data)
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
