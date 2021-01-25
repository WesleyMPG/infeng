
class Value(object):
    """This class keeps the values and the associated rules of a variable
    """
    NULL = ''

    def __init__(self, name, description='None',
                 value='', confidence=100):
        self.name = name
        self.value = value
        self.confidence = confidence
        self.is_right_side_in_rules = []
        self.description = description

    def was_defined(self):
        return self.value != 0

    def add_rule(self, rule):
        self.is_right_side_in_rules.append(rule)

    def __str__(self):
        return f'{self.name}: {self.value} - {self.description}'
