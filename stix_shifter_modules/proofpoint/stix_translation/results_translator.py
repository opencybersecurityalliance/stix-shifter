from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix
from os import path
import json
import ast

class ResultsTranslator(JSONToStix):

    def __init__(self, options, dialect):
        super().__init__(options, dialect, path.dirname(__file__))

    @staticmethod
    def process_multipart(objectsdata, body_multipart, fileobjects):
        for ele in body_multipart:
            filename = ele.get('filename')
            if filename:
                for i in fileobjects:
                    try:
                        name = objectsdata[i]['name']
                        MD5 = objectsdata[i]['hashes']['MD5']
                        SHA256 = objectsdata[i]['hashes']['SHA-256']
                        if filename==name and MD5==ele.get('md5') and SHA256==ele.get('sha256'):
                            #add body_raw_ref
                            ele["body_raw_ref"] = i
                            #del redundant data
                            del ele['filename']
                            del ele['md5']
                            del ele['sha256']
                    except:
                        continue

    @staticmethod
    def update_bodymultipart(results):
        objectsdata = results['objects'][1]['objects']
        fileobjects = [i for i, j in objectsdata.items() if j['type'] == "file"]
        body_multipartobjs = [i for i, j in objectsdata.items() if j.get('body_multipart')]

        if body_multipartobjs:
            body_multipart = objectsdata[body_multipartobjs[0]].get('body_multipart')
            ResultsTranslator.process_multipart(objectsdata, body_multipart, fileobjects)

    def translate_results(self, data_source, data):
        """
        Translates JSON data into STIX results based on a mapping file
        :param data: JSON formatted data to translate into STIX format
        :type data: str
        :param mapping: The mapping file path to use as instructions on how to translate the given JSON data to STIX.
            Defaults the path to whatever is passed into the constructor for JSONToSTIX (This should be the to_stix_map.json in the module's json directory)
        :type mapping: str (filepath)
        :return: STIX formatted results
        :rtype: str
        """
        results = super().translate_results(data_source, data)
        json_data = json.loads(data)

        if len(results['objects']) - 1 == len(json_data):
            for i in range(1, len(results['objects'])):
                results['objects'][i]['num  ber_observed'] = 1
        else:
            raise RuntimeError("Incorrect number of result objects after translation. Found: {}, expected: {}.".format(
                len(results['objects']) - 1, len(json_data)))

        return results