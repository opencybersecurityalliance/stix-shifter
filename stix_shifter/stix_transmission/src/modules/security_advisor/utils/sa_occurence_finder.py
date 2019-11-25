from flatten_json import flatten

def find(s_key, superset):
    """
        Takes in searchKey and Set of findings and return the list satisfying that searchKey
        :param s_key: search Key
        :type s_key: str
        :param superset: Set in which need to be searched
        :type superset: dict
        :return: list of findings that has s_key
        :rtype: list
    """
    dic_flattened = [flatten(d) for d in superset]
    out = []
    for item in dic_flattened:
        for key, value in item.items():
            if(str(s_key) == str(value)):
                out.append(item)
            if(str(s_key) == "'" +str(value) + "'"):
                out.append(item)
    return out  

def and_operation(entites , set):
    """
        Helper function..
        Reduces the set on every iteration.
    """
    for elem in entites:
        r = find(elem[1] , set)
        set = r
    return set

def query_function(sentence , set):
    """
        Return all the findings with AND opeation on entities of sentence
    """
    findings = []
    for statement in sentence:
        findings.append(and_operation(statement, set))
        
    return findings

