import json

from . import json_to_stix_translator
from ..modules.base.base_result_translator import BaseResultTranslator
from . import transformers

# Concrete BaseResultTranslator


class JSONToStix(BaseResultTranslator):

    def translate_results(self, data, mapping=None):
        # if translating QRadar events to STIX...
        json_data = json.loads(data)

        if(mapping is None):
            map_file = open('src/modules/qradar/json/to_stix_map.json').read()
            map_data = json.loads(map_file)
        else:
            map_data = json.loads(map)

        # todo: make datasource id/name dynamic
        datasource = {
            'id': '7c0de425-33bf-46be-9e38-e42319e36d95', 'name': 'events'}

        results = json_to_stix_translator.convert_to_stix(
            datasource, map_data, json_data, transformers.get_all_transformers())

        return json.dumps(results)
