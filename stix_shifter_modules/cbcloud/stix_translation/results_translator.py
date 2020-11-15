import json
import ntpath
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

            # Convert the process_name and parent_name to split path and name fields
            if json_entry.get('process_name', False):
                tmp = json_entry['process_name']
                json_entry['process_name'] = ntpath.basename(tmp)
                json_entry['process_path'] = ntpath.dirname(tmp)

            if json_entry.get('parent_name', False):
                tmp = json_entry['parent_name']
                json_entry['parent_name'] = ntpath.basename(tmp)
                json_entry['parent_path'] = ntpath.dirname(tmp)

            # Convert list values
            for key in json_entry:
                if isinstance(json_entry.get(key, False), list):
                    # If only 1 value, replace the list with the value
                    if len(json_entry[key]) == 1:
                        json_entry[key] = json_entry[key][0]
                    # If more than 1 value, convert the list items to a string
                    elif len(json_entry[key]) > 1:
                        json_entry[key] = f"[{', '.join(str(x) for x in json_entry[key])}]"

        data = json.dumps(json_data)
        # Throw the updated JSON data to JSONToStix for translation to STIX
        return super().translate_results(data_source, data)
