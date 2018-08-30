from ..base.base_result_translator import BaseResultTranslator

import uuid
import json

class SplunkResultTranslator(BaseResultTranslator):

    def translate_results(self, data_source, data, options, mapping=None):
        """
        Takes in passed in results string and returns it
        :param data_source: STIX identity object representing a data source
        :type data_source: str
        :param data: results string that gets returned
        :type data: str
        :param mapping: This is unused
        :type mapping: str
        :return: the passed in data
        :rtype: str
        """
        # translate results...


        #json_data = json.loads(data)
        data_source = json.loads(data_source)

        bundle = {
            "type": "bundle",
            "id": "bundle--" + str(uuid.uuid4()),
            "objects": []
        }

        self.break_splunk_query(data)

        return bundle

    def break_splunk_query(self, data):

        print(data)
