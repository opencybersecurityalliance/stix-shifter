import re

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


def get_next_index(objects):
    """returns the next available index in the objects dictionary"""
    return str(len(objects.keys()))


def parse_technique(str):
    match = re.match(r'^(.+) \((T.+)\)$', str)
    return {
        "technique_name": match.group(1),
        "technique_id": match.group(2)
    }


def fix_finding_refs(observed):
    objects = observed["objects"]
    events = get_objects_by_type(objects, "x-oca-event")
    for event_ref in events:
        event = objects[event_ref]
        if "finding_refs" in event:
            event["finding_refs"] = list(set(event["finding_refs"]))


def fix_ttp_refs(observed):
    objects = observed["objects"]
    findings = get_objects_by_type(objects, "x-ibm-finding")
    for finding_ref in findings:
        finding = objects[finding_ref]
        if "ttp_tagging_refs" in finding:
            new_refs = []
            for ttp_ref in finding["ttp_tagging_refs"]:
                ttp = objects[ttp_ref]
                if ttp["type"] == "x-ibm-ttp-tagging":
                    if (
                            "kill_chain_phases" in ttp
                            and type(ttp["kill_chain_phases"]) == dict
                    ):
                        phase_name = parse_camel_case(ttp["kill_chain_phases"]["phase_name"])
                        kill_chain = "microsoft"
                        if phase_name in TACTICS:
                            kill_chain = "mitre-attack"
                        ttp["kill_chain_phases"] = [
                            {
                                "phase_name": phase_name,
                                "kill_chain_name": kill_chain
                            }
                        ]
                    if (
                            "extensions" in ttp
                            and "mitre-attack-ext" in ttp["extensions"]
                            and "technique_name" in ttp["extensions"]["mitre-attack-ext"]
                            and type(ttp["extensions"]["mitre-attack-ext"]["technique_name"]) == list
                    ):
                        first = ttp["extensions"]["mitre-attack-ext"]["technique_name"][0]
                        others = ttp["extensions"]["mitre-attack-ext"]["technique_name"][1:]
                        ttp["extensions"]["mitre-attack-ext"] = parse_technique(first)
                        for other in others:
                            t = parse_technique(other)
                            key = get_next_index(objects)
                            objects[key] = {
                                'type': 'x-ibm-ttp-tagging',
                                'extensions': {
                                    'mitre-attack-ext': t
                                }
                            }
                            new_refs.append(key)
            finding["ttp_tagging_refs"].extend(new_refs)

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

def fix_device_event_refs(observed):
    objects = observed["objects"]
    atp_refs = get_objects_by_type(objects, "x-msatp")
    if len(atp_refs) > 0:
        atp = objects[atp_refs[0]]
        if 'Table' in atp and atp['Table'] == 'DeviceEvents':
            events = get_objects_by_type(objects, "x-oca-event")
            if len(events) > 0:
                event = objects[events[0]]
                if 'process_ref' in event:
                    proc_ref = event['process_ref']
                    proc = get_reference(objects, event, 'process_ref', 'process')
                    if 'pid' not in proc and 'binary_ref' in proc:
                        ##main process has no pid - in DeviceEvents this means it is a file ref not a process ref
                        ref = proc['binary_ref']
                        del event['process_ref']
                        event['file_ref'] = ref
                        del objects[proc_ref]


class ResultsTranslator(JSONToStix):

    def translate_results(self, data_source, data):
        result = super().translate_results(data_source, data)
        for observed in result["objects"]:
            if observed["type"] == "observed-data":
                fix_ttp_refs(observed)
                fix_finding_refs(observed)
                fix_device_event_refs(observed)
        return result
