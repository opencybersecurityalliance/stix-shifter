import json
import pathlib
import shlex
from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger

LOGGER = logger.set_logger(__name__)

# Implement custom transformer classes here. 
# The class name needs to be added to the module's to_stix_map.json

class ProcessTransformer(ValueTransformer):
    """A value transformer to convert <data type> to <transformed format>"""

    @staticmethod
    def transform(data): # Leave method name as is.
        try:
            dataAsAJson = json.loads(data)
            
            #print (json.dumps(dataAsAJson, indent=4))
            
            if(dataAsAJson["match"]['type'] == "process"):
                process = dict()
                process["type"] = dataAsAJson["match"]["type"]
                process["pid"] = dataAsAJson["match"]["properties"]["pid"]
                process["created"] = dataAsAJson["match"]["properties"]["start_time"]
               
                arguments_list = shlex.split(dataAsAJson["match"]["properties"]["args"])
                process["args"] = arguments_list
                
                converted_file = dataAsAJson["match"]["properties"]["name"].replace('\\', '/')
                pathObject = pathlib.Path(converted_file)
                process["name"] = pathObject.name + pathObject.suffix
                process["cwd"] = pathObject.parent.as_posix()
                
                creator_user_ref = dict()
                creator_user_ref["type"] = "user-account"
                creator_user_ref["user_id"] = dataAsAJson["finding"]["whats"][0]["artifact_activity"]["acting_artifact"]["process"]["user"]["user"]["user_id"]
                creator_user_ref["display_name"] = dataAsAJson["finding"]["whats"][0]["artifact_activity"]["acting_artifact"]["process"]["user"]["user"]["name"]
                if (dataAsAJson["finding"]["whats"][0]["artifact_activity"]["acting_artifact"]["process"]["user"]["user"]["domain"] is not None):
                    creator_user_ref["is_service_account"] = True
                else:
                    creator_user_ref["is_service_account"] = False

                binary_ref = dict()
                binary_ref["type"] = "file"
                binary_ref["hashes"] = dataAsAJson["finding"]["whats"][0]["artifact_activity"]["acting_artifact"]["process"]["file"]["file"]["hash"]
                binary_ref["name"] = pathObject.name + pathObject.suffix
                
                parent_ref = dict()
                parent_ref["type"] = "directory"
                parent_ref["path"] = pathObject.parent.as_posix()

                binary_ref["parent_directory_ref"] = parent_ref
                
                certificate = dict()
                certificate["type"] = "x509-certificate"
                certificate["issuer"] = dataAsAJson["finding"]["whats"][0]["artifact_activity"]["acting_artifact"]["process"]["file"]["file"]["signature_data"]["issuer"]
                certificate["subject"] = dataAsAJson["finding"]["whats"][0]["artifact_activity"]["acting_artifact"]["process"]["file"]["file"]["signature_data"]["subject"]
                binary_ref["content_refs"] = [certificate]

                process["creator_user_ref"] = creator_user_ref
                process["binary_ref"] = binary_ref
                return process
            else:
                raise Exception("There was no process type")
        except ValueError:
            LOGGER.error("Cannot convert data value {} to <transformed format>".format(data))
        except Exception as err:
            LOGGER.error(err)
    
    
class ProcessPidTransformer(ValueTransformer):

    @staticmethod
    def transform(data): # Leave method name as is.
        try:
            dataAsAJson = json.loads(data)
            
            if(dataAsAJson["match"]['type'] == "process"):
                return dataAsAJson["match"]["properties"]["pid"]
        except ValueError:
            LOGGER.error("Cannot convert data value {} to <transformed format>".format(data))
        except Exception as err:
            LOGGER.error(err)
            
class ProcessCreatedTransformer(ValueTransformer):

    @staticmethod
    def transform(data): # Leave method name as is.
        try:
            dataAsAJson = json.loads(data)
            
            if(dataAsAJson["match"]['type'] == "process"):
                return dataAsAJson["match"]["properties"]["start_time"]
        except ValueError:
            LOGGER.error("Cannot convert data value {} to <transformed format>".format(data))
        except Exception as err:
            LOGGER.error(err)
            
class ProcessArgsTransformer(ValueTransformer):

    @staticmethod
    def transform(data): # Leave method name as is.
        try:
            dataAsAJson = json.loads(data)
            
            arguments_list = shlex.split(dataAsAJson["match"]["properties"]["args"])
            return arguments_list
        except ValueError:
            LOGGER.error("Cannot convert data value {} to <transformed format>".format(data))
        except Exception as err:
            LOGGER.error(err)

class ProcessNameTransformer(ValueTransformer):

    @staticmethod
    def transform(data): # Leave method name as is.
        try:
            dataAsAJson = json.loads(data)
            converted_file = dataAsAJson["match"]["properties"]["name"].replace('\\', '/')
            pathObject = pathlib.Path(converted_file)
            return pathObject.name + pathObject.suffix
            
        except ValueError:
            LOGGER.error("Cannot convert data value {} to <transformed format>".format(data))
        except Exception as err:
            LOGGER.error(err)
            
class ProcessCWDPathTransformer(ValueTransformer):

    @staticmethod
    def transform(data): # Leave method name as is.
        try:
            dataAsAJson = json.loads(data)
            
            converted_file = dataAsAJson["match"]["properties"]["name"].replace('\\', '/')
            pathObject = pathlib.Path(converted_file)
            return pathObject.parent.as_posix()
        except ValueError:
            LOGGER.error("Cannot convert data value {} to <transformed format>".format(data))
        except Exception as err:
            LOGGER.error(err)
            
class ProcessUserIdTransformer(ValueTransformer):

    @staticmethod
    def transform(data): # Leave method name as is.
        try:
            dataAsAJson = json.loads(data)
            return dataAsAJson["finding"]["whats"][0]["artifact_activity"]["acting_artifact"]["process"]["user"]["user"]["user_id"]
        except ValueError:
            LOGGER.error("Cannot convert data value {} to <transformed format>".format(data))
        except Exception as err:
            LOGGER.error(err)
            
class ProcessUserDisplayNameTransformer(ValueTransformer):

    @staticmethod
    def transform(data): # Leave method name as is.
        try:
            dataAsAJson = json.loads(data)
            
            return dataAsAJson["finding"]["whats"][0]["artifact_activity"]["acting_artifact"]["process"]["user"]["user"]["name"]
        except ValueError:
            LOGGER.error("Cannot convert data value {} to <transformed format>".format(data))
        except Exception as err:
            LOGGER.error(err)
            
class ProcessUserDaemonTransformer(ValueTransformer):

    @staticmethod
    def transform(data): # Leave method name as is.
        try:
            dataAsAJson = json.loads(data)
            
            if (dataAsAJson["finding"]["whats"][0]["artifact_activity"]["acting_artifact"]["process"]["user"]["user"]["domain"] is not None):
                return True
            else:
                return False
        except ValueError:
            LOGGER.error("Cannot convert data value {} to <transformed format>".format(data))
        except Exception as err:
            LOGGER.error(err)
            
class ProcessFileCertificateIssuerTransformer(ValueTransformer):

    @staticmethod
    def transform(data): # Leave method name as is.
        try:
            dataAsAJson = json.loads(data)
            return dataAsAJson["finding"]["whats"][0]["artifact_activity"]["acting_artifact"]["process"]["file"]["file"]["signature_data"]["issuer"]
        
        except ValueError:
            LOGGER.error("Cannot convert data value {} to <transformed format>".format(data))
        except Exception as err:
            LOGGER.error(err)
            
class ProcessFileCertificateSubjectTransformer(ValueTransformer):

    @staticmethod
    def transform(data): # Leave method name as is.
        try:
            dataAsAJson = json.loads(data)
            return dataAsAJson["finding"]["whats"][0]["artifact_activity"]["acting_artifact"]["process"]["file"]["file"]["signature_data"]["subject"]
        
        except ValueError:
            LOGGER.error("Cannot convert data value {} to <transformed format>".format(data))
        except Exception as err:
            LOGGER.error(err)
            
class ProcessFileHashesTransformer(ValueTransformer):

    @staticmethod
    def transform(data): # Leave method name as is.
        try:
            dataAsAJson = json.loads(data)
            return dataAsAJson["finding"]["whats"][0]["artifact_activity"]["acting_artifact"]["process"]["file"]["file"]["hash"]
        except ValueError:
            LOGGER.error("Cannot convert data value {} to <transformed format>".format(data))
        except Exception as err:
            LOGGER.error(err)