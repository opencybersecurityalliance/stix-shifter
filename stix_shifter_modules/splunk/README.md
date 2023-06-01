# Splunk

## Supported STIX Mappings

See the [table of mappings](splunk_supported_stix.md) for the STIX objects and operators supported by this connector.

### Format for calling stix-shifter from the command line

python stix_shifter.py `<translator_module>` `<query or result>` `<stix identity object>` `<data>`

(Note the identity object is only used when converting from AQL to STIX, but due to positional arguments, an empty hash will need to be passed in when converting from STIX patterns to AQL. Keyword arguments should be implemented to overcome this).

## Converting from Splunk CIM to STIX Cyber Observable Object

Splunk data to Stix mapping is defined in `to_stix_map.json` which is located in the Splunk module.

As Splunk uses common field names across multiple Splunk CIM objects, the unique CIM compliant event `tag` field located in the `<data>` object clarifies which objects can potentially be created.

This example Splunk data (based on the `Change Analysis` CIM):

`python main.py translate "splunk" "results" '{"type": "identity", "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3", "name": "Splunk", "identity_class": "events"}' '[{"tag": "change", "_time": "2018-08-21T15:11:55.000+00:00", "event_count": 1, "bytes": "300", "user": "ibm_user", "object_path": "hkey_local_machine\\system\\bar\\foo", "file_path": "C:\\Users\\someuser\\sample.dll", "file_create_time": "2018-08-15T15:11:55.676+00:00", "file_modify_time": "2018-08-15T18:10:30.456+00:00", "file_hash": "aec070645fe53ee3b3763059376134f058cc337247c978add178b6ccdfb0019f", "file_name": "sample.dll", "file_size": 25536}]'`

Will return the following valid STIX Cyber Observable Object:
```json
{                                                                                                       
    "type": "bundle",                                                                                   
    "id": "bundle--26a18dba-427e-44b3-82cf-ed6a666ddccd",                                               
    "objects": [                                                                                        
        {                                                                                               
            "type": "identity",                                                                         
            "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",                                     
            "name": "Splunk",                                                                           
            "identity_class": "events"                                                                  
        },                                                                                              
        {                                                                                               
            "id": "observed-data--00693dee-0690-4211-bf6a-364fae53df18",                                
            "type": "observed-data",                                                                    
            "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",                         
            "objects": {                                                                                
                "0": {                                                                                  
                    "type": "user-account",                                                             
                    "account_login": "ibm_user",                                                        
                    "user_id": "ibm_user"                                                               
                },                                                                                      
                "1": {                                                                                  
                    "type": "windows-registry-key",                                                     
                    "creator_user_ref": "0",                                                            
                    "key": "hkey_local_machine\\system\\bar\\foo"                                       
                },                                                                                      
                "2": {                                                                                  
                    "type": "directory",                                                                
                    "path": "C:\\Users\\someuser\\sample.dll",                                          
                    "created": "2018-08-15T15:11:55.676Z",                                              
                    "modified": "2018-08-15T18:10:30.456Z"                                              
                },                                                                                      
                "3": {                                                                                  
                    "type": "file",                                                                     
                    "parent_directory_ref": "2",                                                        
                    "created": "2018-08-15T15:11:55.676Z",                                              
                    "modified": "2018-08-15T18:10:30.456Z",                                             
                    "hashes": {                                                                         
                        "SHA-256": "aec070645fe53ee3b3763059376134f058cc337247c978add178b6ccdfb0019f"   
                    },                                                                                  
                    "name": "sample.dll",                                                               
                    "size": 25536                                                                       
                }                                                                                       
            },                                                                                          
            "created": "2018-08-21T15:11:55.000Z",                                                      
            "modified": "2018-08-21T15:11:55.000Z",                                                     
            "first_observed": "2018-08-21T15:11:55.000Z",                                               
            "last_observed": "2018-08-21T15:11:55.000Z",                                                
            "number_observed": 1,                                                                       
            "x_splunk_spl": {                                                                       
                "bytes": "300",                                                                         
                "user": "ibm_user"                                                                      
            }                                                                                           
        }                                                                                               
    ]                                                                                                   
}                                                                                                       
```
