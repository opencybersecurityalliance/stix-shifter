#!/usr/bin/python

from onelogin.api.util.constants import Constants

from .base import Base
from .statement import Statement


class Privilege(Base):
    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            self.from_data(args[0])
        else:
            self.from_values(*args)

    def from_data(self, data):
        self.id = str(data.get('id', ''))
        self.name = data.get('name', '')
        self.description = data.get('description', '')
        self.statements = []
        if data.get('privilege'):
            self.version = data.get('privilege').get('Version', '')
            statements_data = data.get('privilege').get('Statement', [])
            for statement_data in statements_data:
                self.statements.append(Statement(statement_data))

    def from_values(self, id, name, version, statements, description=None):
        self.id = str(id)
        self.name = name
        self.description = description
        self.version = version
        self.statements = []
        for statement in statements:
            if isinstance(statement, Statement):
                self.statements.append(statement)
            elif isinstance(statement, dict) and 'Effect' in statement and 'Action' in statement and 'Scope' in statement:
                self.statements.append(Statement(statement['Effect'], statement['Action'], statement['Scope']))

    @staticmethod
    def get_valid_actions():
        return Constants.VALID_ACTIONS
