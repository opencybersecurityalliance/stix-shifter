from .statementParser import StatementParser

class StixPatternParser:
    """
        Parse method will do the parsing of the Sentence.
        (The first parsing to break the sentence into Statements)
        RESULTS Connector will call this funcion initially and the further processing
        will be done by the statemet parser
    """
    def __init__(self):
        self.statement_parser =  StatementParser()
    
    def solved_statement(self, elem):

        splitted  = elem.split("] AND [")
        return splitted

    def parse(self, pattern):

        list_of_OR =[]
        split_and  = pattern.split("] OR [")

        for elem in split_and:
            list_of_OR.append( self.solved_statement(elem) )

        return list_of_OR