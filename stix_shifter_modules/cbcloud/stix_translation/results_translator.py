import json
import re

from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix


class ResultsTranslator(JSONToStix):

    @staticmethod
    def parse_hash(hashlist):
        """Extract hash values from list."""
        md5 = ''
        sha256 = ''

        for hash_value in hashlist:
            if re.match('^[a-fA-F0-9]{32}$', hash_value):
                md5 = hash_value
            elif re.match('^[a-fA-F0-9]{64}$', hash_value):
                sha256 = hash_value

        return md5, sha256

    def translate_results(self, data_source, data):
        """Convert and translate the JSON data to STIX."""
        json_data = json.loads(data)

        for json_entry in json_data:
            # Split process hash lists into separate md5 and sha256 entries
            if json_entry.get('process_hash', False):
                md5, sha256 = self.parse_hash(json_entry.pop('process_hash'))
                json_entry['process_md5'] = md5
                json_entry['process_sha256'] = sha256

            if json_entry.get('parent_hash', False):
                md5, sha256 = self.parse_hash(json_entry.pop('parent_hash'))
                json_entry['parent_md5'] = md5
                json_entry['parent_sha256'] = sha256

            # Split lists across separate JSON fields
            count = 1
            for key in json_entry:
                if isinstance(json_entry.get(key, False), list) and self.map_data.get(key, False):
                    # If only 1 value in the list, replace the list with the value and keep the mapping definition
                    if len(json_entry[key]) == 1:
                        json_entry[key] = json_entry[key][0]
                    # If more than 1 value in the list, remove the item and add separate entries and mapping definitions
                    elif len(json_entry[key]) > 1:
                        # Get the mapping definition for the field
                        map_value = self.map_data.pop(key)
                        # Add new fields for each value with a copy of the original mapping definition
                        for json_value in json_entry.pop(key):
                            json_entry[key + str(count)] = json_value
                            self.map_data[key + str(count)] = map_value
                            count += 1

        data = json.dumps(json_data)
        # Throw the updated JSON data to JSONToStix for translation to STIX
        return super().translate_results(data_source, data)
