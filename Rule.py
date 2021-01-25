
class Rule(object):
    def __init__(self, content):
        self.left = ''
        self.right = ''
        self.__load_content(content)

    def __load_content(self, content):
        self.left = content[0]
        self.right = content[1]
        self.confidence = content[2]

    def __str__(self):
        r = f'if {self.left} then {self.right}'
        return r
