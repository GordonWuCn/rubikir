# 

class Stat:
    pass


class Assign(Stat):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression

    def __str__(self):
        return 'ASSIGN ' + self.variable.identifier + ' <- ' + str(self.expression)


class IfElse(Stat):
    def __init__(self, condition, true_branch, false_branch):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch
    
    def __str__(self):
        ifelse = 'IF ' + str(self.condition) + '\n'
        for stat in self.true_branch:
            ifelse += indent(str(stat)) + '\n'
        ifelse += 'ELSE\n'
        for stat in self.false_branch:
            ifelse += indent(str(stat)) + '\n'
        ifelse += 'IF END'
        return ifelse


class Var:
    def __init__(self, identifier, program):
        self.identifier = identifier
        self.program = program

    def __str__(self):
        return self.identifier


class Expr:
    pass


class Rval(Expr):
    def __init__(self, variable):
        self.variable = variable

    def __str__(self):
        return 'RVAL ' + str(self.variable)


class Field(Expr):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'FIELD ' + self.name


class SeqSeen(Expr):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'SEQSEEN ' + self.name


class Load(Expr):
    def __init__(self, key):
        self.key = key

    def __str__(self):
        return 'LOAD ' + str(self.key)


class Store(Stat):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return 'STORE ' + str(self.key) + ' <- ' + str(self.value)


class InsertMeta(Stat):
    def __init__(self, offset, length):
        self.offset = offset
        self.length = length

    def __str__(self):
        return 'INSERT @' + str(self.offset) + ', len: ' + str(self.length)


class InsertData(Stat):
    def __init__(self, offset, length, payload):
        self.offset = offset
        self.length = length
        self.payload = payload

    def __str__(self):
        return (
            'INSERTDATA @ ' + str(self.offset) + ', len: ' + str(self.length) +
            ', payload: ' + str(self.payload)
        )


class Assemble(Stat):
    def __str__(self):
        return 'ASSEMBLE'


class External(Stat):
    def __init__(self, dep_list, queue=False):
        self.dep_list = dep_list
        self.queue = queue

    def __str__(self):
        ext = 'EXTERNAL ' + str_list(self.dep_list)
        if self.queue:
            ext += ' AND QUEUE'
        return ext


class Program:
    def __init__(self, queue_api=True):
        self.stat_list = None
        self.key_list = []
        self.var_list = []
        self.queue_api = queue_api

    def variable(self, name):
        var = Var(name, self)
        self.var_list.append(var)
        return var

    def key(self, name):
        key = Key(name, self)
        self.key_list.append(key)
        return key

    def set_code(self, stat_list):
        self.stat_list = stat_list

    def __str__(self):
        prog = 'Program\n'
        prog += 'TEMP ' + str_list(self.var_list) + '\n'
        prog += 'PERM ' + str_list(self.key_list) + '\n'
        if self.stat_list is not None:
            prog += '\n'
            for stat in self.stat_list:
                prog += str(stat) + '\n'
        return prog


class Key:
    def __init__(self, identifier, program):
        self.identifier = identifier
        self.program = program

    def __str__(self):
        return self.identifier


class Op(Expr):
    def __init__(self, type, operand_list):
        self.type = type
        self.operand_list = operand_list

    def __str__(self):
        return (
            'OP:' + self.type + '(' + 
            str_list([str(operand) for operand in self.operand_list]) +
            ')'
        )

class Create(Stat):
    def __init__(self, identifier, initial_map):
        self.identifier = identifier
        self.initial_map = initial_map
    
    def __str__(self):
        return (
            'Create @ ' + str(self.identifier) + ': ' + 
            str_dict(self.initial_map)
        )


class Contain(Expr):
    def __init__(self, identifier):
        self.identifier = identifier

    def __str__(self):
        return 'CONTAIN ' + str(self.identifier)


class Delete(Stat):
    def __str__(self):
        return 'DELETE'


class Constant(Expr):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'CONST ' + str(self.value)


def str_list(list):
    return ', '.join([str(item) for item in list])

def str_dict(dict):
    return ', '.join([str(key) + ' => ' + str(value) for key, value in dict.items()])

def indent(str):
    result = []
    for line in str.split('\n'):
        result.append('  ' + line)
    return '\n'.join(result)