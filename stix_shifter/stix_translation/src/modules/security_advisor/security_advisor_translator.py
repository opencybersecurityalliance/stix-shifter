from .security_advisor_query_translator import SecurityAdvisorQueryTranslator
from ..base.base_translator import BaseTranslator
from ...json_to_stix.json_to_stix import JSONToStix
from ...json_to_stix import observable

from flatten_json import flatten
from os import path
import json
import re 



class Translator(BaseTranslator):

    def __init__(self):
        basepath = path.dirname(__file__)
        filepath = path.abspath(
            path.join(basepath, "json", "to_stix_map.json"))
        self.mapping_filepath = filepath
        # Pass in callback function to handle hashes with unknown type
        # Use a decorator which has standard JSONToStix translation capability and ability to decorate with observables.
        self.result_translator = JSONToStixObservablesDecorator(filepath)
        self.query_translator = SecurityAdvisorQueryTranslator()

    

class JSONToStixObservablesDecorator:
    def __init__(self, filepath):
        self.result_translator = JSONToStix(filepath)
        self.filepath = filepath
        
    def translate_results(self, data_source, data, options, mapping=None):
        json_data = json.loads(data)
        map_file = open(self.filepath).read()
        mapping_overriden = json.loads(map_file)
        # Decorate the findings with std observables at this step
        self.decorateFindingsWithObjects(json_data,mapping_overriden)
        data = json.dumps(json_data)
        # Override the mapping with dynamically identified definitions
        options["mapping"] = mapping_overriden
        return self.result_translator.translate_results( data_source, data, options, mapping_overriden)
    
    # Decorate the finding with dynamically identified cyber observables
    def decorateFindingsWithObjects(self,data, mapping_overriden): 
        for finding in data:
            flattened_finding = flatten(finding)
            self.regexAndDecorateWithStdObjects(flattened_finding,finding,r'((?:[\da-fA-F]{2}[:\-]){5}[\da-fA-F]{2})',"mac-addr", mapping_overriden)
            self.regexAndDecorateWithStdObjects(flattened_finding,finding,r'[0-9]+(?:\.[0-9]+){3}',"ipv4address", mapping_overriden)
            self.regexAndDecorateWithStdObjects(flattened_finding,finding,r'(?<![:.\w])(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}(?![:.\w])',"ipv6address", mapping_overriden)
            self.regexAndDecorateWithStdObjects(flattened_finding,finding,r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)","email",mapping_overriden)
            self.regexAndDecorateWithStdObjects(flattened_finding,finding,r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]","domain-name",mapping_overriden)
            self.regexAndDecorateWithStdObjects(flattened_finding,finding,r'(https?://\S+)',"url",mapping_overriden)
            self.regexAndDecorateWithStdObjects(flattened_finding,finding,r'([~!@#$%^&*()\-_+={}\[\]|\\:;\"`\'<>.\?\w]+\.[a-z,A-Z][\w]+|[\w]+\.[a-z,A-Z][\W]+|\.[a-z,A-Z][\w]+)',"file",mapping_overriden)
            self.customFunctionAndDecorateWithStdObjects(flattened_finding,finding,"directory",mapping_overriden)

    # This method decorates finding with cyber observables and overrides mapping to support these observables
    def regexAndDecorateWithStdObjects(self,flattened_finding, finding, regex,type, mapping_overriden):
        definition = mapping_overriden[type]
        objects = []
        for key, value in flattened_finding.items():
            try:
                objectList = re.findall(regex, value)
                exceptionList = []
                if len(objectList) > 0:
                    if type == 'domain-name' :
                       for value in objectList:
                           if "securityadvisor." in value:
                               exceptionList.append(value)
                           elif ".pdf" in value or ".sh" in value or ".txt" in value or ".html" in value:
                               exceptionList.append(value)
                    if type == 'file':
                       for value in objectList:
                           if ".com" in value or ".in" in value or ".org" in value or ".co.in" in value or ".net" in value:
                               exceptionList.append(value)
                    # Removing specific exceptions here.
                    objectList =  list(set(objectList) - set(exceptionList))
                    objects.extend(objectList)
            except:
                pass
        
        count = 1
        for entry in set(objects):
            try:
                finding[type+ str(count)] = entry
                # Dynamically add mapping, for eg: 5 email definitions if there are 5 emails identified from a finding
                mapping_overriden[type+ str(count)] = definition
                count += 1
            except:
                pass
    
    # This method provides a way to call custom functions when function name is provided as string
    def customFunctionAndDecorateWithStdObjects(self, flattened_finding, finding, type, mapping_overriden):
        m = globals()['ObjectParserMethods']()
        function_name = "parse"+type.capitalize() 
        getattr(m, function_name)(flattened_finding, finding, type, mapping_overriden)


""" This class contains all custom  parsing functions to parse standard stix objects from findings.
    Each of these methods should start with ‘parse’  and end with type.
    For example  parseDirectory parses directory type objects """


class ObjectParserMethods:

    def parseDirectory(self,flattened_finding, finding, type, mapping_overriden):
        regex = "[/~!@#$%^&*()\-_+={}\[\]|\\:;\"`\'<>.\?\w]+"
        definition = mapping_overriden[type]
        objects = []
        for key, value in flattened_finding.items():
            try:
                objectList = re.findall(regex, value)
                exceptionList = []
                dirList = []
                for value in objectList:
                    path = value
                    if '.' in value and '/' in value and 'providers' not in value:
                        path = re.search("[/[\w]*/+", value).group()
                        dirList.append(path)
                    if '.' not in value and '/' in value and 'providers' not in value:
                        dirList.append(path)
                objects.extend(dirList)
            except:
                pass
        
        count = 1
        for entry in set(objects):
            try:
                finding[type+ str(count)] = entry
                # Dynamically add mapping, for eg: 5 email definitions if there are 5 emails identified from a finding
                mapping_overriden[type+ str(count)] = definition
                count += 1
            except:
                pass
