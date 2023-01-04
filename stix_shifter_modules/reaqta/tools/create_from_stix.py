from _ctypes import PyObj_FromPtr # pip install ctypes-callable
import json
import re
import json

from dictionaries import REFERERS, SUBSTITUTES

class NoIndent(object):
    """ Value wrapper. """
    def __init__(self, value):
        self.value = value

class MyEncoder(json.JSONEncoder):
    FORMAT_SPEC = '@@{}@@'
    regex = re.compile(FORMAT_SPEC.format(r'(\d+)'))

    def __init__(self, **kwargs):
        self.__sort_keys = kwargs.get('sort_keys', None)
        super(MyEncoder, self).__init__(**kwargs)

    def default(self, obj):
        return (self.FORMAT_SPEC.format(id(obj)) if isinstance(obj, NoIndent)
                else super(MyEncoder, self).default(obj))

    def encode(self, obj):
        format_spec = self.FORMAT_SPEC
        json_repr = super(MyEncoder, self).encode(obj) 
        for match in self.regex.finditer(json_repr):
            id = int(match.group(1))
            no_indent = PyObj_FromPtr(id)
            json_obj_repr = json.dumps(no_indent.value, sort_keys=self.__sort_keys)
            json_repr = json_repr.replace(
                            '"{}"'.format(format_spec.format(id)), json_obj_repr)

        return json_repr

def find(element, dd, default=None):
    try:
        keys = element.split('.')
        rv = dd
        for key in keys:
            rv = rv[key]
        return rv
    except Exception:
        return default


def find_in_substitutes(path, name) -> str:
    for substitute in SUBSTITUTES:
        if path in substitute['paths']:
            return substitute['name']

    return name

def insert_from_prop(from_stix, obj_name, obj_field, path, name):
    from_stix[obj_name]['fields'][obj_field] = find(obj_field, from_stix[obj_name]['fields'], [])
    substitute_name = find_in_substitutes(path, name)
    if '.startsWith' in substitute_name:
        return
        
    substitute_name = substitute_name.replace('.gte', '').replace('.lte', '')
    from_stix[obj_name]['fields'][obj_field].append(substitute_name)
    from_stix[obj_name]['fields'][obj_field] = list(set(from_stix[obj_name]['fields'][obj_field]))
    from_stix[obj_name]['fields'][obj_field].sort()

def add_from_prop(from_stix, name, value, path):
    if isinstance(value, dict):
        value = [value]

    for val in value:
        key = find('key', val)
        ref_check = True
        if key:
            key_spl = key.split('.', 1)
            if len(key_spl) > 1:
                obj_name = key_spl[0]
                obj_field = key_spl[1]

                #  Some rules
                obj_field = obj_field.replace('.MD5', ".'MD5'")
                obj_field = obj_field.replace('.SHA-1', ".'SHA-1'")
                obj_field = obj_field.replace('.SHA-256', ".'SHA-256'")

                if 'extensions.' in obj_field:
                    if 'x-process-ext' in obj_field:
                        print(obj_field)
                        
                    obj_field = obj_field.replace('extensions.', '')
                    
                    add_from_prop(from_stix, name, {'key': obj_field}, path)
                    ref_check = False
                    obj_field_key_spl = obj_field.split('.', 1)
                    # obj_field_key_spl[0] = obj_field_key_spl[0].replace('-', '_') + "_ref"
                    obj_field_key_spl[0] = "extensions.'{}'".format(obj_field_key_spl[0])
                    obj_field = '.'.join(obj_field_key_spl)


                from_stix[obj_name] = find(obj_name, from_stix, {})
                from_stix[obj_name]['fields'] = find('fields', from_stix[obj_name], {})

                if '_ref' in obj_field and ref_check:
                    obj_field_ref = find(obj_field, find(obj_name, REFERERS, None))
                    if obj_field_ref:
                        for ref in obj_field_ref:
                            if '_refs' in obj_field:
                                field = obj_field + "[*]." + ref
                            else:
                                field = obj_field + "." + ref
                            insert_from_prop(from_stix, obj_name, field, path, name)
                    else:
                        raise Exception('Reference not found for stix property ' + obj_name + ':' + obj_field)
                else:
                    insert_from_prop(from_stix, obj_name, obj_field, path, name)

                    
                # if '_ref' in obj_field:
                #     if obj_name not in REFERERS:
                #         REFERERS[obj_name] = {}
                        
                #         REFERERS[obj_name][obj_field] = None


def parse_from_stix():
    reacta_search_result_key_map = None
    to_stix = None
    from_stix = {}
    num_reaqta_props = 0
    num_found_stix_props = 0

    with open('reacta_search_result_key_map.json', 'r') as f:
        reacta_search_result_key_map = json.load(f)

        # Additions
        reacta_search_result_key_map.append({
            "name": "ip",
            "paths": ["payload.data.localAddrV4"]
        })
        reacta_search_result_key_map.append({
            "name": "ip",
            "paths": ["payload.data.localAddrV6"]
        })
        reacta_search_result_key_map.append({
            "name": "ip",
            "paths": ["payload.data.remoteAddrV4"]
        })
        reacta_search_result_key_map.append({
            "name": "ip",
            "paths": ["payload.data.remoteAddrV6"]
        })

    with open('../stix_translation/json/to_stix_map.json', 'r') as f:
        to_stix = json.load(f)

    for obj in reacta_search_result_key_map:
        num_reaqta_props += 1
        name = obj['name']

        for path in obj['paths']:
            val = find(path, to_stix)
            if val:
                num_found_stix_props += 1
                add_from_prop(from_stix, name, val, path)

    with open('../stix_translation/json/from_stix_map.json', 'w') as f:
        for stix_obj in from_stix:
            for stix_field in from_stix[stix_obj]['fields']:
                # set(['a', 'b']).issubset(['a', 'b', 'c'])
                from_stix[stix_obj]['fields'][stix_field] = NoIndent(from_stix[stix_obj]['fields'][stix_field])

        f.write(json.dumps(from_stix, cls=MyEncoder, sort_keys=True, indent=2))

    print('num_reaqta_props', num_reaqta_props)
    print('num_found_stix_props', num_found_stix_props)
    # print('REFERERS', json.dumps(REFERERS))

parse_from_stix()
