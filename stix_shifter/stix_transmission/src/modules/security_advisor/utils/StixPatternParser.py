from .statementParser import StatementParser

class StixPatternParser:
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

    def parse(self, pattern, params):

        list_or =[]
        list_and = []

        try :
            arr = self.helper(pattern)
            for elem in arr :
                if( len(elem) ==1):
                    solved  = self.statementParser.parser(elem[0], params)
                    list_or.append(solved)

                else :
                    for finding in elem:
                        solved  = self.statementParser.parser(finding , params)
                        list_and.append(solved)

            combined_list = []

            for elem in list_and:
                list_occ_ids = []

                for sub_elem in elem:

                    if( len(sub_elem) == 1 ):
                        list_occ_ids.append(sub_elem[0]["id"])
                    
                combined_list.append(list_occ_ids)

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
