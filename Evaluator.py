from infeng.scanner import tokens, Scanner
from infeng.parser import Parser
from .Value import Value

def asking(value):
    while True:
        i = input(f'What is the value of {value.name}? ').lower()
        if i[0] == 't':
            value.value = True
            return
        elif i[0] == 'f':
            value.value = False
            return
        else:
            print('Invalid entry. Try again.')

class Evaluator(object):
    def __init__(self, values_table, asking_function=None):
        self.var_stack = []
        self.op_stack = []
        self.scanner = Scanner()
        self.parser = Parser()
        self.values_table = values_table
        self.ask_for = asking_function if asking_function is not None else asking

    def __push_operator(self, op):
        self.op_stack.append(op)

    def __pop_operator(self):
        self.op_stack.pop()

    def __push_var(self, var):
        self.var_stack.append(var)

    def __pop_var(self):
        return self.var_stack.pop()

    def __resolve_value(self, value):
        """It looks for value.name on the right side of rules

        If value.name is found on right side of a rule, it evaluates
        that rule, else asks for the value
        """
        result = None
        rules = value.is_right_side_in_rules
        if len(rules) > 0:
            value.value = self.evaluate(rules[0].left)
        else:
            self.ask_for(value)

    def __is_expression_solved(self, expression):
        """Checks if expression is already solved and return it
        """
        if expression in self.values_table.keys():
            return self.values_table[expression]
        return None

    def __resolve_not_exp_value(self, var, expression):
        """This denies a var value and puts on values_table

        Here is created a new entry on values_table containing
        !var value. Ex: if var is 'A' it will be created NOT A value
        which is stored as A! in the values_table.
        """
        exp_value = Value(expression)
        self.values_table[expression] = exp_value
        var_value = self.values_table[var[0]]
        if var_value.value == Value.NULL:
            self.__resolve_value(var_value)
        exp_value.value = not var_value.value
        return exp_value

    def __solve_not(self):
        """Checks if !A is already solved else solve it.
        """
        var = self.__pop_var()
        expression = var[0] + '!'
        exp_value = self.__is_expression_solved(expression)
        if exp_value is None:
            exp_value = self.__resolve_not_exp_value(var, expression)
        self.__push_var([expression, tokens.ID])

    def __register_and_or_exp_on_table(self, var1, var2, op):
        """This method registers in values_table an expression like A and B

        A new entry will be created in the table. Ex: A and B is registered as
        ABand, also BAand
        """
        expression = var1[0] + var2[0] + op[0]
        expression2 = var2[0] + var1[0] + op[0]
        exp_value = Value(expression)
        self.values_table[expression] = exp_value
        self.values_table[expression2] = exp_value
        return exp_value

    def __do_or(self, val1, val2):
        """It executes or operation
        """
        if val1.value == Value.NULL:
            self.__resolve_value(val1)
            if val1.value == True: return True
        if val2.value == Value.NULL:
            self.__resolve_value(val2)
            if val2.value == True: return True
        return val1.value or val2.value

    def __do_and(self, val1, val2):
        """It executes and operation
        """
        if val1.value == Value.NULL:
            self.__resolve_value(val1)
            if val1.value == False: return False
        if val2.value == Value.NULL:
            self.__resolve_value(val2)
            if val2.value == False: return False
        return val1.value and val2.value

    def __do_and_or(self, val1, val2, op):
        """This determinates the operation to be executed between two values
        """
        if op[0] == 'and':
            return self.__do_and(val1, val2)
        elif op[0] == 'or':
            return self.__do_or(val1, val2)
        else:
            raise Exception(f'Invalid operator {op[0]}')

    def __resolve_and_or_exp_value(self, var1, var2, op):
        """This method gets variable values reference on values_table

        It gets the reference to var1, var2 and exp_value, also it
        calls __do_and_or to get exp_value.value
        """
        exp_value = self.__register_and_or_exp_on_table(var1, var2, op)
        v1_value = self.values_table[var1[0]]
        v2_value = self.values_table[var2[0]]
        exp_value.value = self.__do_and_or(v1_value, v2_value, op)

    def __solve_and_or(self, operator):
        var1 = self.__pop_var()
        var2 = self.__pop_var()
        expression = var1[0] + var2[0] + operator[0]
        exp_value = self.__is_expression_solved(expression)
        if exp_value is None:
            self.__resolve_and_or_exp_value(var1, var2, operator)
        self.__push_var([expression, tokens.ID])

    def __get_ansewer(self):
        var = self.__pop_var()[0]
        value = self.values_table[var]
        if value.value == Value.NULL:
            self.__resolve_value(value)
        return value.value

    def _evaluate(self, queue):
        current = queue.pop(0)
        while True:
            if current[1] == tokens.ID:
                self.__push_var(current)
            elif current[1] == tokens.NOT:
                self.__solve_not()
            else:
                self.__solve_and_or(current)
            if len(queue) == 0: break
            current = queue.pop(0)
        return self.__get_ansewer()

    def evaluate(self, expression):
        token_list = self.scanner.scan(expression)
        queue = self.parser.parse(token_list)
        return self._evaluate(queue)

