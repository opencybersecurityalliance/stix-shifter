import json
import os

MODULES = [
    # 'alertflex',
    # 'arcsight',
    # 'async_template',
    # 'aws_athena',
    # 'aws_cloud_watch_logs',
    # 'aws_security_hub',
    # 'azure_sentinel',
    # 'bigfix',
    # 'carbonblack',
    # 'cbcloud',
    # 'cloudsql',
    # 'crowdstrike',
    # 'csa',
    # 'cybereason',
    # 'darktrace',
    # 'datadog',
    # 'elastic',
    # 'elastic_ecs',
    # 'guardium',
    # 'ibm_security_verify',
    # 'infoblox',
    # 'msatp',
    'mysql',
    # 'onelogin',
    # 'paloalto',
    # 'proofpoint',
    # 'proxy',
    # 'qradar',
    # 'reaqta',
    # 'reversinglabs',
    # 'rhacs',
    # 'secretserver',
    # 'security_advisor',
    # 'sentinelone',
    # 'splunk',
    # 'stix_bundle',
    # 'sumologic',
]

REFERERS = {
    "network-traffic": {
        "src_ref": ["value"],
        "dst_ref": ["value"]
    },
    "x-ibm-finding": {
        "src_ip_ref": ["value"],
        "dst_ip_ref": ["value"]
    },
    "x-oca-event": {
        "network_ref": ["src_ref.value", "dst_ref.value"],
        "file_ref": ["name"],
        "process_ref": ["pid"],
        "parent_process_ref": ["pid"],
        "user_ref": ["user_id"],
        "ip_refs": ["value"],
        "host_ref": ["x-oca-asset.hostname"]
    },
    "x-oca-asset": {
        "ip_refs": ["value"]
    },
    "process": {
        "binary_ref": ["name"],
        "parent_ref": ["binary_ref.name"],
        "creator_user_ref": ["user_id"]
    },
    "file": {
        "parent_directory_ref": ["path"]
    }
}

SUBSTITUTES = {}
non_existing_references = {}

class SortedListEncoder(json.JSONEncoder):
    def encode(self, obj):
        def sort_lists(item):
            if isinstance(item, list):
                return sorted(sort_lists(i) for i in item)
            elif isinstance(item, dict):
                return {k: sort_lists(v) for k, v in item.items()}
            else:
                return item
        return super(SortedListEncoder, self).encode(sort_lists(obj))


def find(element: str, dd: dict, default=None):
    try:
        keys = element.split('.')
        rv = dd
        for key in keys:
            rv = rv[key]
        return rv
    except Exception:
        return default

def find_in_substitutes(module, path, name) -> str:
    if module in SUBSTITUTES:
        for substitute in SUBSTITUTES[module]:
            if path in substitute['paths']:
                if substitute.get('remove'):
                    return None
                return substitute['name']

    return name

def insert_from_prop(module, from_stix, obj_name, obj_field, name, path):

    substitute_name = find_in_substitutes(module, path, name)
    if not substitute_name:
        return

    from_stix[obj_name] = find(obj_name, from_stix, {})
    from_stix[obj_name]['fields'] = find('fields', from_stix[obj_name], {})

    from_stix[obj_name]['fields'][obj_field] = find(obj_field, from_stix[obj_name]['fields'], [])
    from_stix[obj_name]['fields'][obj_field].append(substitute_name)
    from_stix[obj_name]['fields'][obj_field] = list(set(from_stix[obj_name]['fields'][obj_field]))


def add_from_prop(module, from_stix, to_stix, name=None, path=None):
    if isinstance(to_stix, list):
        for t_s in to_stix:
            add_from_prop(module, from_stix, t_s, name, path)

    elif isinstance(to_stix, dict):
        key = find('key', to_stix)
        ref_check = True
        if key:
            key_spl = key.split('.', 1)
            if len(key_spl) > 1:
                obj_name = key_spl[0]
                obj_field = key_spl[1]

                #  Some rules
                obj_field = obj_field.replace('.SHA-1', ".'SHA-1'")
                obj_field = obj_field.replace('.SHA-256', ".'SHA-256'")

                if 'extensions.' in obj_field:
                    obj_field = obj_field.replace('extensions.', '')
                    
                    add_from_prop(module, from_stix, {'key': obj_field}, name, path)
                    ref_check = False
                    obj_field_key_spl = obj_field.split('.', 1)
                    # obj_field_key_spl[0] = obj_field_key_spl[0].replace('-', '_') + "_ref"
                    obj_field_key_spl[0] = "extensions.'{}'".format(obj_field_key_spl[0])
                    obj_field = '.'.join(obj_field_key_spl)

                if  str(obj_field).endswith(('_ref', '_refs')) and ref_check:
                    obj_field_ref = find(obj_field, find(obj_name, REFERERS, None))
                    if obj_field_ref:
                        for ref in obj_field_ref:
                            if str(obj_field).endswith('_refs'):
                                ref_field = obj_field + "[*]." + ref
                            else:
                                ref_field = obj_field + "." + ref
                            insert_from_prop(module, from_stix, obj_name, ref_field, name, path)
                    else:
                        # raise Exception('Reference not found for stix property ' + obj_name + ':' + obj_field)
                        if obj_name not in non_existing_references:
                            non_existing_references[obj_name] = {}
                        
                        # find_key = '%s.fields.%s' % (obj_name, obj_field)
                        # non_existing_references[obj_name][obj_field] = find(find_key, current_from_stix, [])
                else:
                    insert_from_prop(module, from_stix, obj_name, obj_field, name, path)

                # if from_stix[obj_name]['fields'] == {}:
                #     del from_stix[obj_name]

        else:
            for k, v in to_stix.items():
                if path:
                    k_path = '.'.join([path, k])
                else:
                    k_path = str(k)
                add_from_prop(module, from_stix, v, k, k_path)


def parse_from_stix():
    to_stix = {}
    from_stix = {}


    for module in MODULES:
        path_var_module = './var/from_stix/%s' % module
        path_to_skip = 'stix_shifter_modules/%s/SKIP.ME' % module
        path_to_stix = 'stix_shifter_modules/%s/stix_translation/json/to_stix_map.json' % module
        path_from_stix = 'stix_shifter_modules/%s/stix_translation/json/from_stix_map.json' % module
        path_from_stix_sorted = 'var/from_stix/%s/from_stix_map_sorted.json' % module
        path_from_stix_generated = 'var/from_stix/%s/from_stix_map_generated.json' % module
        path_to_to_from = 'stix_shifter_modules/%s/stix_translation/json/to_to_from_map.json' % module

        if os.path.exists(path_to_skip):
            print('SKIPPING %s' % module)
            continue

        os.makedirs(path_var_module, exist_ok=True)

        # get SUBSTITUTES for module
        if os.path.exists(path_to_to_from):
            with open(path_to_to_from, 'r') as f:
                SUBSTITUTES[module] = json.load(f)

        # generate sorted existing from_stix
        try:
            with open(path_from_stix, 'r') as f:
                from_stix = json.load(f)

            with open(path_from_stix_sorted, 'w') as f:
                f.write(json.dumps(from_stix, sort_keys=True, indent=2, cls=SortedListEncoder))
        except Exception:
            print('File from_stix_map.json does not exist for %s. Continueing...' % module)
            pass

        # Get exisitng to_stix 
        from_stix = {}
        try:
            with open(path_to_stix, 'r') as f:
                to_stix = json.load(f)

            add_from_prop(module, from_stix, to_stix, None,  None)

            # Generate new from_stix
            with open(path_from_stix_generated, 'w') as f:
                f.write(json.dumps(from_stix, sort_keys=True, indent=2, cls=SortedListEncoder))

            # print('COMPARE CMD: diff -u %s %s | ydiff -s' % (path_from_stix_sorted, path_from_stix_generated))
        
        except Exception as e:
            # print('ERROR in %s: %s' % (module, e))
            pass

    print('Done')


if __name__ == "__main__":
    parse_from_stix()
