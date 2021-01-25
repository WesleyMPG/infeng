import json, sys

if 'infeng' in sys.modules:
    from .Evaluator import Evaluator
    from .Rule import Rule
    from .Value import Value

    from infeng.scanner import Scanner
    from infeng.parser import Parser
else:
    from Evaluator import Evaluator
    from Rule import Rule
    from Value import Value

    from scanner import Scanner
    from parser import Parser


class Engine(object):
    def __init__(self, knowledge_file_path, asking_function=None,
                 debug=False):
        self.knowledge_base = []
        self.values_table = {}
        self.evaluator = Evaluator(self.values_table, asking_function,
                                   debug)
        self.load_knowledge(knowledge_file_path)

    def __load_file_content(self, file):
        file = json.load(file)
        desc = file['description']
        rules = file['rules']
        return desc, rules

    @staticmethod
    def __check_types_order(types : list, var : list):
        if len(types) != len(var): return False
        for i in range(len(types)):
            if not isinstance(var[i], types[i]):
                return False
        return True

    def __get_description_info(self, item):
        #return value, description
        if type(item) == bool:
            return item, 100, ''
        elif type(item) == str:
            return '', 100, item
        elif type(item) == list:
            item[1] = float(item[1])
            if self.__check_types_order([bool, float, str], item):
                return item[0], item[1], item[2]
            elif self.__check_types_order([bool, float], item):
                return item[0], item[1]
            else:
                raise Exception(f'{item} should be [bool, str].')
        else:
            raise Exception(f'Invalid description {item}.\
Acepted formats: bool, str, [bool, str].')

    def load_descriptions(self, desc):
        print('Loading descriptions...')
        for key in desc.keys():
            try:
                v, c, d = self.__get_description_info(desc[key])
            except ValueError:
                v, c = self.__get_description_info(desc[key])
                d = ''
            self.values_table[key] = Value(key, value=v,
                                           description=d,
                                           confidence=c)

    def load_rules(self, rules):
        print('Loading rules...')
        for i in rules:
            rule = Rule(i)
            self.knowledge_base.append(rule)
            value= self.values_table[rule.right]
            # associa uma um valor (A) às regras nas quais ele
            # aparece no lado direito de uma regra
            value.add_rule(rule)

    def load_knowledge(self, file_path):
        with open(file_path, 'r') as file:
            desc, rules = self.__load_file_content(file)
            self.load_descriptions(desc)
            self.load_rules(rules)

    def evaluate(self, expression):
        return self.evaluator.evaluate(expression)
