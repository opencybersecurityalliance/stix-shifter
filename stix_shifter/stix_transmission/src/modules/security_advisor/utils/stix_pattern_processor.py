from .statement_parser import StatementParser

class StixPatternProcessor:
    """
        Parse method will do the parsing of the Sentence.
        (The first parsing to break the sentence into Statements)
        RESULTS Connector will call this funcion initially and the further processing
        will be done by the statemet parser
    """
    def __init__(self):
        self.statementParser = StatementParser()

    def solved_statement(self, elem):

            splitted  = elem.split(" AND [")
            return splitted

    def helper(self, pattern):

        list_of_OR =[]
        split_and  = pattern.split(" OR [")
        for elem in split_and:
            list_of_OR.append( self.solved_statement(elem) )

        return list_of_OR

    def process(self, pattern, params):

        list_or =[]
        list_and = []

        try :
            statements = self.helper(pattern)
            for statement in statements :
                if(len(statement) ==1):
                    sa_findings  = self.statementParser.parse_and_call_api(statement[0], params)
                    list_or.append(sa_findings)

                else :
                    for sub_statement in statement:
                        sa_findings  = self.statementParser.parse_and_call_api(sub_statement, params)
                        list_and.append(sa_findings)

            combined_list = []

            for elem in list_and:
                list_occurence_ids = []
                for sub_elem in elem:
                    for e in sub_elem :
                        list_occurence_ids.append(e["id"])
                    
                combined_list.append(list_occurence_ids)

            common_elements =[]
            if( combined_list != [] ):
                common_elements = list(set.intersection(*map(set, combined_list)))

        except Exception as e:
            raise Exception("Invalid Query " + str(e))

        data = []
        for elem in list_and:
            for sub_elem in elem:
                if( len(sub_elem) == 1 ):

                    for element in common_elements:
                        if(element == sub_elem[0]["id"]):
                            sub_elem[0]["occurence_count"] =1
                            data.append(sub_elem[0])
                        
        for elem_or in list_or:

            for sub_elem in elem_or:
                for finding in sub_elem:
                    finding["occurence_count"] =1
                    data.append(finding)
                    
        return data
