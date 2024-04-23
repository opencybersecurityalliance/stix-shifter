
import json
from logging import Logger
import os

class Test_Group_Similarities():
    
    #These 4 methods iterate through the file system and get a list of all of the config/json files.
    #After it gets all of the files, it iterates through all of the files and validates the groups
    def test_iterate_through_file_list_config_connection(self):
        list_of_config_files = self._get_list_of_files("config.json")
        module_group_list = dict()
        for file_index in range(len(list_of_config_files)):
            self._validate_config_connection(json.loads(list_of_config_files[file_index]), module_group_list)
    
    def test_iterate_through_file_list_config_auth(self):
        list_of_config_files = self._get_list_of_files("config.json")
        module_group_list = dict()
        for file_index in range(len(list_of_config_files)):
            self._validate_config_auth(json.loads(list_of_config_files[file_index]), module_group_list)
            
    def test_iterate_through_file_list_leng_en_config(self):
        list_of_config_files = self._get_list_of_files("config.json")
        list_of_lang_en_files = self._get_list_of_files("lang_en.json")
        module_group_list = dict()
        for file_index in range(len(list_of_config_files)):
            self._validate_lang_en_connection(json.loads(list_of_config_files[file_index]), json.loads(list_of_lang_en_files[file_index]), module_group_list)
            
    def test_iterate_through_file_list_lang_en_auth(self):
        list_of_config_files = self._get_list_of_files("config.json")
        list_of_lang_en_files = self._get_list_of_files("lang_en.json")
        module_group_list = dict()
        for file_index in range(len(list_of_config_files)):
            self._validate_lang_en_auth(json.loads(list_of_config_files[file_index]), json.loads(list_of_lang_en_files[file_index]), module_group_list)
    
    #Checks if the current file has a group field. If it doesn't, than it's ignored.
    #This gets the current group type and then checks if we have already seen it or not. If we haven't add it to the list of groups.
    #If the group was already seen, we need to validate that the values in the current config/langen file match the current group.
    def _validate_config_connection(self, config_json, module_group_list):
        if("connection" in config_json and "type" in config_json["connection"] and "group" in config_json["connection"]["type"]):
            current_group = config_json["connection"]["type"]["group"]
            if(current_group in module_group_list):
                self._check_that_config_connection_matches(config_json, module_group_list, current_group)
            else:
                module_group_list[current_group] = config_json
    
    def _validate_config_auth(self, config_json, module_group_list):
        if("connection" in config_json and "type" in config_json["connection"] and "group" in config_json["connection"]["type"]):
            current_group = config_json["connection"]["type"]["group"]
            if(current_group in module_group_list):
                self._check_that_config_auth_matches(config_json, module_group_list, current_group)
            else:
                module_group_list[current_group] = config_json
                
    def _validate_lang_en_connection(self, config_json, lang_en, module_group_list):
        if("connection" in config_json and "type" in config_json["connection"] and "group" in config_json["connection"]["type"]):
            current_group = config_json["connection"]["type"]["group"]
            if(current_group in module_group_list):
                self._check_that_lang_en_connection_matches(lang_en, module_group_list, current_group)
            else:
                module_group_list[current_group] = config_json
                module_group_list[current_group]["lang_en"] = lang_en
                
    def _validate_lang_en_auth(self, config_json, lang_en, module_group_list):
        if("connection" in config_json and "type" in config_json["connection"] and "group" in config_json["connection"]["type"]):
            current_group = config_json["connection"]["type"]["group"]
            if(current_group in module_group_list):
                self._check_that_lang_en_auth_matches(lang_en, module_group_list, current_group)
            else:
                module_group_list[current_group] = config_json
                module_group_list[current_group]["lang_en"] = lang_en    
    
    #Iterates through all of the keys in the json file.
    # If the key is type or options or the key is not in the current group, than add it to the current group.
    # If they key is in the current group, than check if the current field matches what's in the current group.
    # There are exceptions for default (which should probably be removed) and previous which doesn't change behavior (it's the previous keyname)
    def _check_that_config_connection_matches(self, config_json, module_group_list, current_group):
        for key,value in config_json["connection"].items():
            if(key in module_group_list[current_group]["connection"] and key != "type" and key != "options"):
                existing_value = module_group_list[current_group]["connection"][key]
                if("default" in existing_value):
                    existing_value.pop("default")
                if("default" in value):
                    value.pop("default")
                if("previous" in existing_value):
                    existing_value.pop("previous")
                if("previous" in value):
                    value.pop("previous")
                assert existing_value == value
            else:
                module_group_list[current_group]["connection"][key] = value
                
    def _check_that_config_auth_matches(self, config_json, module_group_list, current_group):
        for key,value in config_json["configuration"]["auth"].items():
            if(key in module_group_list[current_group]["configuration"]["auth"]):
                existing_value = module_group_list[current_group]["configuration"]["auth"][key]
                if("previous" in existing_value):
                    existing_value.pop("previous")
                if("previous" in value):
                    value.pop("previous")
                assert existing_value == value
            else:
                module_group_list[current_group]["configuration"]["auth"][key] = value
                
    def _check_that_lang_en_connection_matches(self, lang_en, module_group_list, current_group):
        for key,value in lang_en["connection"].items():
            if(key in module_group_list[current_group]["lang_en"]["connection"]):
                existing_value = module_group_list[current_group]["lang_en"]["connection"][key]
                assert existing_value == value
            else:
                module_group_list[current_group]["connection"][key] = value
                
    def _check_that_lang_en_auth_matches(self, lang_en, module_group_list, current_group):
        for key,value in lang_en["configuration"]["auth"].items():
            if(key in module_group_list[current_group]["lang_en"]["configuration"]["auth"]):
                existing_value = module_group_list[current_group]["lang_en"]["configuration"]["auth"][key]
                assert existing_value == value
            else:
                module_group_list[current_group]["configuration"]["auth"][key] = value
                
    def _get_list_of_files(self, file_name):
        #Generated by WCA for GP
        #Here's an example of how you can do this in Python using the os module:

        # Define the directory path
        directory_path = os.getcwd() + "/stix_shifter_modules"
        lang_en_file_list = list()
        
        # Iterate through all the child directories
        for dir_name, subdir_list, file_list in os.walk(directory_path):
            # Check if the file exists in the current directory
            if file_name in file_list:
                # Open the file and read its contents
                with open(os.path.join(dir_name, file_name), 'r') as file:
                    lang_en_file_list.append(file.read())
        return lang_en_file_list