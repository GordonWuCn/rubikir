# 

class Stat:
    pass


class Assign(Stat):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression


class IfElse(Stat):
    def __init__(self, condition, true_branch, false_branch):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch


class Match(Stat):
    def __init__(self, branch_map):
        self.branch_map = branch_map


class Var:
    def __init__(self, identifier, program):
        self.identifier = identifier
        self.program = program


class Expr:
    pass


class Rval(Expr):
    def __init__(self, variable):
        self.variable = variable


class Field(Expr):
    def __init__(self, name):
        self.name = name


class Load(Expr):
    def __init__(self, key):
        self.key = key


class GetState(Expr):
    pass


class Store(Stat):
    def __init__(self, key, value):
        self.key = key
        self.value = value


class SetState(Stat):
    def __init__(self, state):
        self.state = state


class Insert(Stat):
    def __init__(self, offset, length, payload):
        self.offset = offset
        self.length = length
        self.payload = payload


class Assemble(Stat):
    pass


class External(Stat):
    def __init__(self, dep_list, queue=False):
        self.dep_list = dep_list
        self.queue = queue


class Program:
    def __init__(self, queue_api=True):
        self.stat_list = None
        self.key_list = []
        self.queue_api = queue_api

    def variable(self, name):
        return Var(name, self)

    def key(self, name):
        self.key_list.append(name)
        return name

    def set_code(self, stat_list):
        self.stat_list = stat_list


class Op(Expr):
    def __init__(self, type, operand_list):
        self.type = type
        self.operand_list = operand_list


class NoHole(Expr):
    pass


class Perpare(Stat):
    def __init__(self, identifier, initial_map):
        self.identifier = identifier
        self.initial_map = initial_map


class Delete(Stat):
    pass


class Constant(Expr):
    def __init__(self, value):
        self.value = value
