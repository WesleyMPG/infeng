import json
from .Rule import Rule
from .Value import Value
from infeng.scanner import Scanner
from infeng.parser import Parser
from .Evaluator import Evaluator


class Engine(object):
    def __init__(self, knowledge_file_path, asking_function=None):
        self.knowledge_base = []
        self.values_table = {}
        self.evaluator = Evaluator(self.values_table, asking_function)
        self.load_knowledge(knowledge_file_path)

    def __load_file_content(self, file):
        file = json.load(file)
        desc = file['description']
        rules = file['rules']
        return desc, rules

    def __get_description_info(self, item):
        #return value, description
        if type(item) == bool:
            return item, ''
        elif type(item) == str:
            return '', item
        elif type(item) == list:
            if type(item[0]) == bool and type(item[1]) == str:
                return item[0], item[1]
            else:
                raise Exception(f'{item} should be [bool, str].')
        else:
            raise Exception(f'Invalid description {item}.\
Acepted formats: bool, str, [bool, str].')

    def load_descriptions(self, desc):
        print('Loading descriptions...')
        for key in desc.keys():
            v, d = self.__get_description_info(desc[key])
            self.values_table[key] = Value(key, value=v, description=d)

    def load_rules(self, rules):
        print('Loading rules...')
        for i in rules:
            rule = Rule(i)
            self.knowledge_base.append(rule)
            # associa uma um valor (A) às regras nas quais ele
            # aparece no lado direito de uma regra
            self.values_table[rule.right].add_rule(rule)

    def load_knowledge(self, file_path):
        with open(file_path, 'r') as file:
            desc, rules = self.__load_file_content(file)
            self.load_descriptions(desc)
            self.load_rules(rules)

    def evaluate(self, expression):
        return self.evaluator.evaluate(expression)
