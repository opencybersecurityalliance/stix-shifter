from .statementParser import StatementParser

class StixPatternParser:

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