# QRadar

### Format for calling stix-shifter from the command line

python stix_shifter.py `<translator_module>` `<query or result>` `<stix identity object>` `<data>`

(Note the identity object is only used when converting from AQL to STIX, but due to positional arguments, an empty hash will need to be passed in when converting from STIX patterns to AQL. Keyword arguments should be implemented to overcome this).