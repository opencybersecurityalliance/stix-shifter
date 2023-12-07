import pathlib
import shlex
from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger

LOGGER = logger.set_logger(__name__)

class ProcessArgsTransformer(ValueTransformer):
    @staticmethod
    def transform(data):
        #The argument is passed in as if it was run in the command line.
        #This method uses shlex to convert it to a list.
        try:
            arguments_list = shlex.split(data)
            return arguments_list
        except ValueError:
            LOGGER.error("Cannot convert data value {} to <transformed format>".format(data))
        except Exception as err:
            LOGGER.error(err)

class ProcessNameTransformer(ValueTransformer):
    @staticmethod
    def transform(data):
        #The path is given in the form of path/file.extension.
        #This method uses pathlib to only return the file name.
        try:
            converted_file = data.replace('\\', '/')
            pathObject = pathlib.Path(converted_file)
            return pathObject.name
            
        except ValueError:
            LOGGER.error("Cannot convert data value {} to <transformed format>".format(data))
        except Exception as err:
            LOGGER.error(err)
            
class ProcessCWDPathTransformer(ValueTransformer):
    @staticmethod
    def transform(data):
        #The path is given in the form of path/file.extension.
        #This method uses pathlib to only return the directory path.
        try:            
            converted_file = data.replace('\\', '/')
            pathObject = pathlib.Path(converted_file)
            return pathObject.parent.as_posix()
        except ValueError:
            LOGGER.error("Cannot convert data value {} to <transformed format>".format(data))
        except Exception as err:
            LOGGER.error(err)
            
class ProcessUserDaemonTransformer(ValueTransformer):
    @staticmethod
    def transform(data):    
        #This method just checks if a domain was provided for the user. If it does, than it's true. Otherwise it's false.
        if (data is not None and data is not ""):
            return True
        else:
            return False
        
class ReturnAlertTransformer(ValueTransformer):
    @staticmethod
    def transform(data): 
        #The type of the alert isn't returned as an object in the data.
        #Thus I had to set it to always return it as an alert.
        return "alert"
                
class ConvertTextSeverityToNumberValue(ValueTransformer):
    @staticmethod
    def transform(data):
        #This method converts the text value of a severity (info,low,high) to a hardcoded number.
        #One assumption is that the fields are "info", "low", and "high". I could not find any reference to all of the possible values.
        #I do know that info and high exist.
        #The second assumption is their relative values. I don't actually know how severe an 80 is for example or if their is a higher value.
        #Finally, if it comes across a new value, it returns 50 as default. This is mostly in case something critical exist, in which case it should show up.
        if("info" in data):
            return 0
        elif("low" in data):
            return 40
        elif("high" in data):
            return 80
        else:
            return 50
        
class ReturnEmpty(ValueTransformer):
    @staticmethod
    def transform(data):
        #This is used because the mitre extension requires an empty tactic value if an actual value doesn't exist.
        return ""
