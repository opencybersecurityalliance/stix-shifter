from .sa_findings_api import get_all_occurences
from .sa_occurence_finder import query_function

class StatementParser:
    """
        Utility Function for parsing STIX PATTERN (based on the priorites)
        1. Spliiting on basis of OR
        2. Spitting the sub elements of OR in AND
        3. Cleaning the entites
        4. Creating a list of AND and OR that will be evaluated further in Results Connector
    """
    def cleaner(self, entity):

        if entity.find("[") == 0  and  entity.find("]") == len(entity)-1:
            return entity[1:len(entity)-1].strip()

        if entity.find("[") == 0 :
            return entity[1:].strip()

        if entity.find("]") == len(entity) -1 :
            return entity[:len(entity)-1].strip()
        else:
            return entity.strip()

    def evaluate_or(self, splitted, list):

        for elem in splitted:
            sub = elem.strip()
            sub = elem.split("=")
            key = sub[0].strip()
            value = sub[1].strip()
            list.append( (key, value) )

        return list

    def slpit_and_eval_or(self, splitted):
        
        splitted  = splitted.split("AND")
        list_OR  = []
        for i in range(0, len(splitted)):       
            cleaned_entity  =  self.cleaner(splitted[i])
            split_OR = cleaned_entity.split("AND")
            self.evaluate_or(split_OR, list_OR )

        return list_OR

    def parse_and_call_api(self, statement, params):

        search_id = statement
        time_filter = None
        if( statement.find("START") != -1 ):
            index = statement.find("START")
            search_id = statement[ 0 : index ]
            time_filter = statement[ index : len(statement) ].strip()
            if( time_filter.find("STOP") != -1):
                time_filter = time_filter.replace("t", "")
                time_filter = time_filter.replace("START", "fromTime:")
                time_filter = time_filter.replace("STOP", "toTime:")
                time_filter = time_filter.replace("'", '"')

            else:
                time_filter = time_filter.replace("t", "")
                time_filter = time_filter.replace("START", "fromTime:")
                time_filter = time_filter.replace("'", '"')

        if( statement.find("STOP") != -1 and  statement.find("START") == -1 ):
            raise Exception("STOP time not specified")

        list_AND = []
        split_AND = search_id.strip().split("OR")

        for i in split_AND:
            list_AND.append(self.slpit_and_eval_or(i))

        set = get_all_occurences( params, time_filter)
        findings = query_function(list_AND, set)

        return findings

        