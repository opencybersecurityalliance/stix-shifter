from abc import ABCMeta, abstractmethod
from cmath import inf
from stix_shifter_utils.utils import logger
from stix_shifter_utils.utils.file_helper import read_json as helper_read_json
from datetime import datetime
from stix2validator import validate_instance, print_results, ValidationOptions
import uuid


"""  
    This BaseNormalization class normalize third party threat feed raw report to various STIX objects
    such as indicator, extension-definition, malware, infrastructure, identity
    This base class normalize malware type and infra type and also creates relationship object implicit.
"""
class BaseNormalization(object,metaclass=ABCMeta):

    def __init__(self, options):
        self.logger = logger.set_logger(__name__)
        self.stix_validator = options.get('stix_validator')


    def create_stix_bundle(self, version="2.1"):
        DEFAULT_SPEC_VERSION = version
        if (DEFAULT_SPEC_VERSION == "2.1"):
            bundle = {
                "type": "bundle",
                "id": "bundle--" + str(uuid.uuid4()),
                "spec_version": DEFAULT_SPEC_VERSION,
                "objects": []
            }
        else:
            bundle = {}
        return bundle


    '''
    create Identity STIX Domain Object
    param  data_source : JSON formatted data to translate into STIX format, passed as an input param in results_translator.py
    param  namespace : UUID value used to create a deterministic (unique) id for the identity
    '''
    def create_identity_sdo(self, data_source, namespace):
        try:
            DETERMINISTIC_IDENTITY_ID = uuid.uuid5(uuid.UUID(namespace), data_source['name'])      
            DEFAULT_SPEC_VERSION = '2.1'
            stix_type = 'identity'
            now = "{}Z".format(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])
            stix_identity_sdo = {
                'type': stix_type,
                'name': data_source['name'],
                'spec_version': DEFAULT_SPEC_VERSION,
                'id': stix_type + '--' + str(DETERMINISTIC_IDENTITY_ID),            
                'created': now,
                'modified': now,
            }

            if data_source.get('description'): stix_identity_sdo['description'] = data_source['description']
            if data_source.get('roles'): stix_identity_sdo['roles'] = data_source['roles']
            if data_source.get('identity_class'): stix_identity_sdo['identity_class'] = data_source['identity_class']
            if data_source.get('sectors'): stix_identity_sdo['sectors'] = data_source['sectors']
            if data_source.get('sectors'): stix_identity_sdo['sectors'] = data_source['sectors']
            if data_source.get('contact_information'): stix_identity_sdo['contact_information'] = data_source['contact_information']

            if self.stix_validator:
                options = ValidationOptions(version="2.1")
                results = validate_instance(stix_identity_sdo, options)          
                if results.is_valid is False:            
                    print_results(results)
                    raise Exception(f'Invalid parameter set in identity SDO. Please follow STIX 2.1 spec for properties') 

            return [stix_identity_sdo]
        
        except Exception as err:
            raise Exception(f'Exception occurred in create_identity_sdo in BaseNormalization : {err}')  


    ''' 
        create Extension-Definition STIX object
        param  identity_object : Dictionary object that contains STIX 2.1 specification key/value pairs for Identity SDO
        param  namespace : Valid UUID Namespace
        param  nested_properties : list of dict values, see property-extension custom properties in STIX 2.1 documentation, optional argument if you plan on adding custom properties
        param  top_properties : list of dict values, see top-level-extension custom properties, optional argument if you plan on adding custom properties
        param  schema : URL value - The normative definition of the extension, either as a URL or as plain text explaining the definition
    '''
    def create_extension_sdo(self, identity_object, namespace, nested_properties=[], toplevel_properties=[], schema='https://www.ibm.com/cp4s'):
        try:
            # Create an extension-definition object to be used in conjunction with STIX Indicator object
            stix_type = 'extension-definition'
            DEFAULT_SPEC_VERSION = "2.1"
            EXTENSION_VERSION = '1.2.1'
            extension_object = {
                'id': stix_type + '--' + str(uuid.uuid5(uuid.UUID(namespace), 'extension-definition')),
                'type': stix_type,
                'spec_version': DEFAULT_SPEC_VERSION,
                'name': (identity_object.get('name') + ' extension') if identity_object.get('name') is not None else "extension definition object",
                'created': "{}Z".format(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]),
                'modified': "{}Z".format(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]),
                'created_by_ref': identity_object['id'],
                'schema': schema,
                'version': EXTENSION_VERSION,
            }

            if identity_object.get('description'): extension_object['description'] = 'Extension object for ' + identity_object.get('description')

            if (len(nested_properties) > 0 or len(toplevel_properties) > 0):
                extension_object['extension_types'] = []
                extension_object['extension_properties'] = []
                if (len(toplevel_properties) > 0):
                    extension_object['extension_types'].append('toplevel-property-extension') 
                    for prop in toplevel_properties:
                        extension_object['extension_properties'].append(prop)
                if (len(nested_properties) > 0):
                    extension_object['extension_types'].append('property-extension') 
                    if (not len(extension_object['extension_properties']) > 0):
                        del extension_object['extension_properties']

            if self.stix_validator:
                options = ValidationOptions(version="2.1")
                results = validate_instance(extension_object, options)            
                if results.is_valid is False:              
                    print_results(results)
                    raise Exception(f'Invalid parameter set in extension_object SDO. Please follow STIX 2.1 spec for properties') 

            stix_extension_sdo = [extension_object]
            return stix_extension_sdo

        except Exception as err:
            raise Exception(f'Exception occurred in create_extension_sdo in BaseNormalization : {err}')  


    def read_json(self, filepath, options):
        return helper_read_json(filepath, options)

    
    def normalize_infra_type_mapping(self, infra_type):
        infra_type_mapping = {
            'data-theft' : 'exfiltration',
            'banking' : 'exfiltration'
        }
        """ convert few infra type values to standard values"""
        if infra_type.lower() in infra_type_mapping:
            return infra_type_mapping[infra_type.lower()]
        return None


    def normalize_malware_type_mapping(self,malware_type):
        malware_type_mapping = {
        'miner': 'resource-exploitation',
        'pua': 'spyware',
        'exfiltration': 'spyware',
        'rat': 'remote-access-trojan',
        'spreading': 'worm',
        'dropper': 'Dropper',
        'exploit': 'exploit-kit'        
        }
        """Convert category values to standard values."""        
        if malware_type.lower() in malware_type_mapping:
            return malware_type_mapping[malware_type.lower()]
        return None


    def matchKeyWord(self,keyword,dataArray):        
        for  item in dataArray:
            if item in keyword.lower():
                return item

    """
        it normalize malware type string to malware type ov list.
        below list can be extended. In future nltk or any other tool to leveraged.
    """
    def normalized_malware_type(self,sourceListOrStr):
        malware_type_ov_list= ['adware','backdoor','bot','bootkit', 'ddos','downloader','dropper' ,'exploit-kit', 
        'keylogger', 'ransomware', 'remote-access-trojan','resource-exploitation',
        'rogue-security-software','rootkit','screen-capture','spyware','trojan','unknown','virus','webshell','wiper','worm','stealware']       

        matched_words_in_target_list =[];
        if isinstance(sourceListOrStr,list):
            if ( len(sourceListOrStr) > 0 ):
                for sourceWord in sourceListOrStr:
                    if sourceWord is not None:
                        matchedMapping = self.normalize_malware_type_mapping(sourceWord)
                        if(matchedMapping is None):
                            matchKeyword = self.matchKeyWord(sourceWord,malware_type_ov_list)                        
                            if(matchKeyword is not None and matchKeyword not in matched_words_in_target_list):
                                matched_words_in_target_list.append(matchKeyword);
                        else:  
                            if(matchedMapping is not None and matchedMapping not in matched_words_in_target_list):
                                matched_words_in_target_list.append(matchedMapping)

                if len(matched_words_in_target_list) == 0:
                    matched_words_in_target_list.append('unknown');    
            return matched_words_in_target_list
        elif isinstance(sourceListOrStr,str):
            if sourceListOrStr is not None:
                matchKeyword = self.matchKeyWord(sourceListOrStr,malware_type_ov_list)
                if(matchKeyword is not None):
                    matched_words_in_target_list.append(matchKeyword)
                else:
                    matchedMapping = self.normalize_malware_type_mapping(sourceListOrStr)
                    if(matchedMapping is not None and matchedMapping not in matched_words_in_target_list):
                        matched_words_in_target_list.append(matchedMapping)

                if len(matched_words_in_target_list) == 0:
                    matched_words_in_target_list.append('unknown') 
            return matched_words_in_target_list


    # it normalize infra type string to infra type ov list.    
    def normalized_infra_type(self,sourceList):
        # target list                                                                      
        infrastructure_type_ov_list= ['amplification','anonymization','botnet','command-and-control', 'exfiltration',
        'hosting-malware','hosting-target-lists' ,'phishing', 'reconnaissance', 'staging', 'unknown']

        matched_words_in_target_list =[];
        if ( len(sourceList) > 0 ):
            for sourceWord in sourceList:
                if sourceWord == 'CnC':
                    sourceWord = 'command-and-control'
                matchKeyword = self.matchKeyWord(sourceWord,infrastructure_type_ov_list)            
                if(matchKeyword is not None and matchKeyword not in matched_words_in_target_list):
                    matched_words_in_target_list.append(matchKeyword)
                else:                    
                    matchedMapping = self.normalize_infra_type_mapping(sourceWord)
                    if (matchedMapping is not None and matchedMapping not in matched_words_in_target_list):
                        matched_words_in_target_list.append(matchedMapping)
            
            if len(matched_words_in_target_list) == 0:
                matched_words_in_target_list.append('unknown') 
        return matched_words_in_target_list 


    """ 
        It creates sighting SDO as per STIX 2.1 specs
        sighting_object: dict object to create sighting STIX object
        indicatorId: str 
    """
    def create_sighting_sdo(self, sighting_object, indicator_id):
        try:
            stix_type = 'sighting'
            DEFAULT_SPEC_VERSION = "2.1"
            now = "{}Z".format(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])
            
            sighting = {                      
                    'type': stix_type,
                    'spec_version' : DEFAULT_SPEC_VERSION,
                    'id': stix_type + '--' + str(uuid.uuid4()),
                    'sighting_of_ref': indicator_id,            
                    'count': sighting_object['count'],
                    'created': now,
                    'modified': now
                }        

            if self.stix_validator:
                options = ValidationOptions(version="2.1")
                results = validate_instance(sighting, options)            
                if results.is_valid is False:
                    print_results(results)
                    raise Exception(f'Invalid parameter set in sighting SDO. Please follow STIX 2.1 spec for properties') 

            return [sighting]
        except Exception as err:
            raise Exception(f'Exception occurred in create_sighting_sdo in BaseNormalization : {err}')  


    """ 
        create infrastructure STIX object
        param : infrastructure_object : dict type of infrastructure value object dict value object to be followed the stix 2.1 infrastructure attributes)    
        enriched_ioc string type 
    """
    def create_infrastructure_object_sdo(self, infrastructure_object, enriched_ioc, indicator_id):
        try:       
            stix_type = 'infrastructure'
            DEFAULT_SPEC_VERSION = "2.1"
            now = "{}Z".format(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])
            infrastructure = {                      
                    'type': stix_type,
                    'spec_version' : DEFAULT_SPEC_VERSION,
                    'id': stix_type + '--' + str(uuid.uuid4()),            
                    'created': now,
                    'modified': now,            
                    'name': 'Infrastructure related to ' + enriched_ioc,
                    'infrastructure_types': infrastructure_object['infrastructure_types'],                   
                    'description' : infrastructure_object['description'] if infrastructure_object.get('description') is not None else ','.join(infrastructure_object.get('infrastructure_types'))
                }
            infrastructure_types = self.normalized_infra_type(infrastructure['infrastructure_types'])
            infrastructure['infrastructure_types'] = infrastructure_types

            if self.stix_validator:
                options = ValidationOptions(version="2.1")
                results = validate_instance(infrastructure, options)            
                if results.is_valid is False:
                    print_results(results)
                    raise Exception(f'Invalid parameter set in infrastructure SDO. Please follow STIX 2.1 spec for properties') 

            infrastructure_array = [infrastructure]
            relationship = self.createRelationship(infrastructure_array, indicator_id)
            infrastructure_array += relationship
            return infrastructure_array
        except Exception as err:
            raise Exception(f'Exception occurred in create_infrastructure_object_sdo : {err}')


    # STIX 2.1 relationship object : relationship between indicatorId and malware SDO.    
    def createRelationship(self,objArray,indicatorId):
        DEFAULT_SPEC_VERSION = "2.1"
        stix_type = 'relationship'
        now = "{}Z".format(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]) 
        relationsihpArray =  []           
        for data in objArray:               
            relationship = {
                "type": stix_type,
                "spec_version": DEFAULT_SPEC_VERSION,
                "id": stix_type + '--' + str(uuid.uuid4()),
                "created": now,
                "modified": now,
                "relationship_type": "indicates",
                "source_ref": indicatorId,
                "target_ref": data['id']
                }
            relationsihpArray.append(relationship)
        return relationsihpArray

    # create malware STIX object
    # param : malware : list (type) of malware values objects (each dict in list to be followed the stix 2.1 )
    # param: indicatorId string type
    # dataToEnrichPattern string type
    def create_malware_sdo(self,malware_object, indicator_id, enriched_ioc):        
        try:        
            malware_array=[]  
            if isinstance(malware_object, list):                
                for data in malware_object:
                    #print(data)            
                    stix_type = 'malware'
                    DEFAULT_SPEC_VERSION = "2.1"
                    now = "{}Z".format(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])            
                    malware = {                      
                            'type': stix_type,
                            'name': data.get('name') if data.get('name') is not None else 'Malware related to ' + enriched_ioc,                         
                            'spec_version': DEFAULT_SPEC_VERSION,
                            'id': stix_type + '--' + str(uuid.uuid4()),            
                            'created': now,
                            'modified': now,                                                                
                            'malware_types': data.get('malware_types') if data.get('malware_types') is not None else ['unknown'],
                            'is_family' : data.get('is_family') if data.get('is_family') is not None else False
                        }
                    # right now its iterates additional attributes of malware SDO and no null, empty list is not checked. Developer has to ensure not to send such data
                    for key,value in data.items():                       
                        if key is not malware:
                            malware[key] = value
                    # set the description same as malware type returns from threat feed if description property is not provided. 
                    if data.get('description'):
                        malware['description'] = data.get('description')
                    elif data.get('malware_types') and 'unknown' not in data.get('malware_types'):                    
                        malware['description'] =  ','.join(data.get('malware_types')) if isinstance(data.get('malware_types'),list) else data.get('malware_types')

                    malware_types = self.normalized_malware_type(malware['malware_types'])     
                    malware['malware_types'] = malware_types                    

                    # malware SDO properties validation        
                    if self.stix_validator:
                        options = ValidationOptions(version="2.1")
                        results = validate_instance(malware, options)                    
                        if results.is_valid is False:                        
                            print_results(results)
                            raise Exception(f'Invalid parameter set in malware SDO. Please follow STIX 2.1 spec for properties') 

                    # if name is not present then compare only malware_types to remove duplicate else check malware types and name.                    
                    if (len([i for i in malware_array if (i['malware_types'] == malware ['malware_types'] and i['name'] == malware ['name'])]) == 0):                        
                        malware_array.append(malware)                   

                relationship = self.createRelationship(malware_array, indicator_id)
                malware_array += relationship
                return malware_array
        except Exception as err:
            raise Exception(f'Exception occurred in create_malware_sdo in BaseNormalization : {err}')

    ''' 
    create Indicator STIX object
    param  indicator_object : Dictionary object that contains STIX 2.1 specification key/value pairs for Indicator SDO
    param  identity_id : UUID id value of Identity SDO
    param  extension_id : UUID id value of Extension-definition object, optional argument if you plan on adding custom properties
    param  nested_properties : list of dict values, see property-extension custom properties in STIX 2.1 documentation, optional argument if you plan on adding custom properties
    param  top_properties : list of dict values, see top-level-extension custom properties, optional argument if you plan on adding custom properties
    '''
    def create_indicator_sdo(self, indicator_object: dict, identity_id: str, extension_id:str=None, nested_properties:list=None, top_properties:list=None):
        try:

            # Param: Dictionary
            stix_type = 'indicator'
            pattern_type = 'stix'
            DEFAULT_SPEC_VERSION = "2.1"
            now = "{}Z".format(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])

            # Exception handle required property
            if 'pattern' not in indicator_object:
                raise ValueError(f'Missing required indicator property: pattern')

            indicator = {
                'type': stix_type,
                'spec_version': DEFAULT_SPEC_VERSION,
                'id': stix_type + '--' + str(uuid.uuid4()),
                'pattern': indicator_object['pattern'],
                'pattern_type': pattern_type,
                'created_by_ref': identity_id,
                'created': now,
                'modified': now,
                'valid_from': now,
            }

            if indicator_object.get('name'): indicator['name'] = indicator_object['name']
            if indicator_object.get('description'): indicator['description'] = indicator_object['description']
            if indicator_object.get('pattern_version'): indicator['pattern_version'] = indicator_object['pattern_version']
            if indicator_object.get('valid_until'): indicator['valid_until'] = indicator_object['valid_until']
            if indicator_object.get('kill_chain_phases'): indicator['kill_chain_phases'] = indicator_object['kill_chain_phases']
            if indicator_object.get('indicator_types'): indicator['indicator_types'] = indicator_object['indicator_types']
            if indicator_object.get('external_references'): indicator['external_references'] = indicator_object['external_references']

            if (extension_id):
                indicator = self.add_extension(indicator, extension_id, nested_properties, top_properties)

            # indicator SDO properties validation        
            if self.stix_validator:
                options = ValidationOptions(version="2.1")
                results = validate_instance(indicator, options)                    
                if results.is_valid is False:
                    print_results(results)                
                    raise Exception(f'Invalid parameter set in indicator SDO. Please follow STIX 2.1 spec for properties')

            return [indicator]

        except ValueError as err:
            raise ValueError(err)


    '''
        Method that lets you add custom property to any STIX SDO
        param:  stix_object         The SDO to add extension-definition
        param:  extension_id        The extensionId from extension-definition SDO that defines the custom objects
        param:  nested_properties   nested extension-definition properties of type list
        param:  top_properties      top-level-custom-properties of type list
    '''
    def add_extension(self, stix_object, extension_id:str=None, nested_properties:list=None, top_properties:list=None):
        if top_properties:
            for prop in top_properties:
                for key, value in prop.items():
                    stix_object[key] = value
        # Add nested properties
        if (nested_properties):
            stix_object['extensions'] = {extension_id: {}}
            stix_object['extensions'][extension_id]['extension_type'] = 'property-extension'
            for prop in nested_properties:
                for key, value in prop.items():
                    stix_object['extensions'][extension_id][key] = value
        return stix_object