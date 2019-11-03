
from .sa_findings_api import get_all_occurences
from flatten_json import flatten

from .StixPatternParser import StixPatternParser


def find(s_key , superset):
    
    dic_flattened = [flatten(d) for d in superset]
    out = []
    for item in dic_flattened:
        for key, value in item.items():

            if( str(s_key) == str(value) ):
                out.append(item)

    return out  

def and_operation(entites , set):
    for elem in entites:
        r = find(elem[1] , set)
        set = r

    return set

def query_func(sentence , set ):

    findings = []

    for statement in sentence:
        findings.append(and_operation(statement, set))
        
    return findings

