from ..base.base_results_connector import BaseResultsConnector
import json
import re
import math

import pandas as pd

class CloudSQLResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def get_rows_partition(self, statement):
        # First, remove the comments (NB: there will be errors if -- is in a string in the query, but I'm not writing a full parser here...)
        statement = re.sub(r'--[^\n]*', '', statement)
        # Find the number of rows we're partitioning by
        m = re.match(r'.*PARTITIONED\s+EVERY\s+(\d+)\s+ROWS.*', statement, re.MULTILINE | re.DOTALL)
        if m is not None:
            return int(m.groups()[0])
        return None

    def records(self, query_id, start_rec, end_rec):
        job = self.api_client.get_job(query_id)
        units = None
        try:
            units = self.get_rows_partition(job['statement'])
        except Exception as e:
            print('Error fetching query statement {}. Will pull all record pages.'.format(e))
        if units is None:
            r = self.api_client.get_result(query_id)
            return r.iloc[start_rec : end_rec+1]
        first_page = math.floor(start_rec / units)
        last_page = math.floor(end_rec / units)
        cut_front = start_rec - first_page * units
        cut_back = units - end_rec % units - 1
        for pn in range(first_page, last_page+1):
                r = self.api_client.get_result(query_id, pagenumber=pn+1)
                if pn == last_page and cut_back < units:
                    r.drop(r.index[range(-cut_back,0)], inplace=True)
                if pn == first_page:
                    r.drop(r.index[range(cut_front)], inplace=True)
                if 'result_df' not in locals():
                    result_df = r
                else:
                    result_df = pd.concat([result_df, r], ignore_index=True)
        return result_df

    def create_results_connection(self, search_id, offset, length):
        min_range = offset
        max_range = offset + length
        success = False
        try:
            response = self.records(search_id, min_range, max_range)
            success = True
            response_json = response.to_dict(orient='records')
        except ValueError as e:
            # error thrown by cloud sql library if results query fail
            response_json = {}
            response_json['message'] = repr(e)
        except Exception as e:
            print('error when getting search results: {}'.format(e))
            raise

        # Construct a response object
        return_obj = dict()
        return_obj['success'] = success
        if success:
            return_obj['data'] = response_json
        else:
            return_obj['error'] = response_json['message']

        return return_obj
