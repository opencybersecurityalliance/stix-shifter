import json
import re

from stix_shifter_modules.msatp.stix_translation.transformers import SeverityToNumericVal
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix

TACTICS = [
    "Reconnaissance",
    "Resource Development",
    "Initial Access",
    "Execution",
    "Persistence",
    "Privilege Escalation",
    "Defense Evasion",
    "Credential Access",
    "Discovery",
    "Lateral Movement",
    "Collection",
    "Command and Control",
    "Exfiltration",
    "Impact"
]


def parse_camel_case(name):
    return "".join([" " + char if char.isupper() and i > 0 else char for i, char in enumerate(name)])


def get_objects_by_type(objects, type_name):
    """receives a stix objects dictionary and returns indexes of all objets of the given type"""
    return [key for (key, obj) in objects.items() if obj["type"] == type_name]


def get_first_object_by_type(objects, type_name):
    """receives a stix objects dictionary and returns the first index and value of the object of the given type"""
    for k, v in objects.items():
        if v.get("type") == type_name:
            return k, v
    return None, None


def delete_object(objects, remove_ref):
    """removes an object with all its references from objects"""
    index_to_remove = int(remove_ref)
    objects.pop(remove_ref)
    renames = []
    for ref, sco in objects.items():
        if int(ref) > index_to_remove:
            renames.append(ref)
        remove = []
        for key, value in sco.items():
            if key.endswith("_ref"):
                if int(value) == index_to_remove:
                    remove.append(key)
                elif int(value) > index_to_remove:
                    sco[key] = str(int(value) - 1)
            elif key.endswith("_refs"):
                sco[key] = [str(int(item) - 1) if int(item) > index_to_remove else item for item in value if
                            int(item) != index_to_remove]
                if len(sco[key]) == 0:
                    remove.append(key)
        for i in remove:
            sco.pop(i)
    for ref in renames:
        objects[str(int(ref) - 1)] = objects.pop(ref)


def get_next_index(objects):
    """returns the next available index in the objects dictionary"""
    i = 0
    while str(i) in objects:
        i += 1
    next_ref = str(i)
    for ref, sco in objects.items():
        remove = []
        for key, value in sco.items():
            if key.endswith("_ref"):
                if value == next_ref:
                    remove.append(key)
            elif key.endswith("_refs"):
                for r in value:
                    if r == next_ref:
                        sco[key] = [item for item in value if item != next_ref]
                        if len(sco[key]) == 0:
                            remove.append(key)
        for i in remove:
            sco.pop(i)
    return next_ref


def add_to_objects(observed, obj_to_add):
    objects = observed['objects']
    index = get_next_index(objects)
    objects[index] = obj_to_add
    if int(index) < len(objects) - 1:
        observed['objects'] = sort_objects(objects)
    return index


def parse_technique(technique):
    match = re.match(r'^(.+) \((T.+)\)$', technique)
    return {
        "technique_name": match.group(1),
        "technique_id": match.group(2)
    }


def create_ttp_from_category(category):
    phase_name = parse_camel_case(category)
    kill_chain = "microsoft"
    if phase_name in TACTICS:
        kill_chain = "mitre-attack"
    return {
        'type': 'x-ibm-ttp-tagging',
        'kill_chain_phases': [
            {
                "phase_name": phase_name,
                "kill_chain_name": kill_chain
            }
        ]
    }


def create_ttps_from_technique(technique):
    t = parse_technique(technique)
    return {
        'type': 'x-ibm-ttp-tagging',
        'extensions': {
            'mitre-attack-ext': t
        }
    }


def fix_alerts(observed):
    objects = observed["objects"]
    json_alert_ref, json_alert = get_first_object_by_type(objects, "x-json-alert")
    if json_alert_ref is not None:
        objects.pop(json_alert_ref)
        event_ref, event = get_first_object_by_type(objects, "x-oca-event")
        alerts = json.loads(json_alert.get('data'))
        ttps = {}
        for alert in alerts:
            finding = {
                'type': 'x-ibm-finding',
                'name': alert.get("Title"),
                'alert_id': alert.get("AlertId"),
                'severity': SeverityToNumericVal.transform(alert.get("Severity")),
                'ttp_tagging_refs': []
            }
            finding_ref = add_to_objects(observed, finding)
            if 'finding_refs' not in event:
                event['finding_refs'] = []
            event['finding_refs'].append(finding_ref)
            if 'Category' in alert:
                cat = alert['Category']
                if cat not in ttps:
                    cat_ttp = create_ttp_from_category(cat)
                    cat_ref = add_to_objects(observed, cat_ttp)
                    ttps[cat] = cat_ref
                finding['ttp_tagging_refs'].append(ttps[cat])
            if 'AttackTechniques' in alert:
                for technique in alert['AttackTechniques']:
                    if technique not in ttps:
                        ttp = create_ttps_from_technique(technique)
                        ttp_ref = add_to_objects(observed, ttp)
                        ttps[technique] = ttp_ref
                    finding['ttp_tagging_refs'].append(ttps[technique])
            if len(finding['ttp_tagging_refs']) == 0:
                finding.pop('ttp_tagging_refs')


def get_reference(objects, source, ref_prop, ref_type):
    if ref_prop not in source:
        return None
    ref_index = source[ref_prop]
    if ref_index not in objects:
        return None
    ref = objects[ref_index]
    if not 'type' in ref or ref['type'] != ref_type:
        return None
    return ref


def extract_pipe_name(x_msatp, event):
    if 'AdditionalFields' in x_msatp:
        pattern = r'PipeName:\s*(.+?),'
        match = re.search(pattern, x_msatp['AdditionalFields'])
        if match:
            event['pipe_name'] = match.group(1)


def fix_device_event_refs(observed):
    objects = observed["objects"]
    x_msatp_refs = get_objects_by_type(objects, "x-msatp")
    if len(x_msatp_refs) > 0:
        x_msatp = objects[x_msatp_refs[0]]
        events = get_objects_by_type(objects, "x-oca-event")
        if len(events) > 0:
            event = objects[events[0]]
            if event['action'] == "NamedPipeEvent":
                ## if named pipe event add the pip_name to event:
                extract_pipe_name(x_msatp, event)
            if 'Table' in x_msatp and x_msatp['Table'] == 'DeviceEvents':
                ## if event from DeviceEvent and there is only file name without process pid should be a file_ref not process_ref:
                validate_process_ref_in_event(event, objects)


def validate_process_ref_in_event(event, objects):
    if 'missingChildShouldMapInitiatingPid' in event:
        pid = event['missingChildShouldMapInitiatingPid']
        if 'process_ref' in event:
            proc_ref = event['process_ref']
            proc = get_reference(objects, event, 'process_ref', 'process')
            ref = proc['binary_ref']
            event['file_ref'] = ref
            delete_object(objects, proc_ref)
        if pid is not None and pid != "-1":
            init_proc = [key for key, value in objects.items()
                         if value.get("type") == "process"
                         and value.get("pid") == event['missingChildShouldMapInitiatingPid']]
            if len(init_proc) == 1:
                event['process_ref'] = init_proc[0]
        del event['missingChildShouldMapInitiatingPid']


def sort_objects(objects):
    return {k: objects[k] for k in sorted(objects, key=lambda x: int(x))}


class ResultsTranslator(JSONToStix):

    def translate_results(self, data_source, data):
        result = super().translate_results(data_source, data)
        for observed in result["objects"]:
            if observed["type"] == "observed-data" and "objects" in observed:
                fix_alerts(observed)
                fix_device_event_refs(observed)
                observed['objects'] = sort_objects(observed['objects'])
        return result
