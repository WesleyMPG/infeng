import sys

if 'infeng' in sys.modules:
    from infeng.scanner import tokens
else:
    from scanner import tokens

class Parser(object):
    pritority = {
        '!': 20, 'and': 15, 'or': 10, '(': 5,
    }

    def __init__(self):
        self.stack = []
        self.queue = []

    def clean(self):
        self.stack = []
        self.queue = []

    def push_stack(self, item):
        self.stack.append(item)

    def stack_top(self):
        if len(self.stack) > 0:
            return self.stack[len(self.stack)-1]
        else:
            return None

    def pop_stack(self):
        return self.stack.pop()

    def push_queue(self, item):
        self.queue.append(item)

    def pop_queue(self):
        return self.queue.pop(0)

    def __handle_parentesis(self, token):
        if token[0] == '(':
            self.push_stack(token)
            return True
        elif token[0] == ')':
            top = self.pop_stack()
            while top[0] != '(':
                self.push_queue(top)
                top = self.pop_stack()
            return True
        return False

    def __handle_operator(self, token):
        if len(self.stack) == 0:
            self.push_stack(token)
            return
        pri = self.pritority[token[0]]
        top_pri = self.pritority[self.stack_top()[0]]
        while pri <= top_pri:
            self.push_queue(self.pop_stack())
            if len(self.stack) == 0: break
            top_pri = self.pritority[self.stack_top()[0]]
        self.push_stack(token)

    def parse(self, tokens_list):
        for token in tokens_list:
            if token[1] == tokens.ID:
                self.push_queue(token)
            elif self.__handle_parentesis(token):
                pass
            else:
                self.__handle_operator(token)
        while len(self.stack) != 0:
            self.push_queue(self.pop_stack())
        queue = self.queue
        self.clean()
        return queue


