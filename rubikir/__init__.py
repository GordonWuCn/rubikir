from .OP import * 
from .buffer import *
from .code_gen import *

class Stat:
    pass


class Assign(Stat):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression

    def literal(proto_name):
        return self.variable.literal(proto_name) + ' = ' + \
            self.expression.literal(proto_name) + ';\n'

    def __str__(self):
        return 'ASSIGN ' + self.variable.identifier + ' <- ' + str(self.expression)


class IfElse(Stat):
    def __init__(self, condition, true_branch, false_branch):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch
    
    def literal(proto_name):
        code = ''
        code += f'if({self.condition.literal()}) {{\n'
        for stat in self.true_branch:
            code += stat.literal(proto_name)
        code += '}\nelse{\n'
        for stat in self.false_branch:
            code += stat.literal(proto_name)


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

    def literal(proto_name):
        return self.program.name +  "_temp->" + self.identifier

    def __str__(self):
        return self.identifier


class Expr:
    pass

class Field(Expr):
    def __init__(self, name):
        self.name = name

    def literal(proto_name, option):
        return {'eval': proto_name + "_header->" + self.name,
                'literal': self.name}[option]
    

    def __str__(self):
        return 'FIELD ' + self.name


class SeqSeen(Expr):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'SEQSEEN ' + self.name



class Program:
    def __init__(self, name, queue_api=True):
        self.stat_list = None
        self.name = name
        self.key_list = []
        self.var_list = []
        self.queue_api = queue_api
        self.type = 0 #connection_oriented or connectionless 
        self.hcode = ''
        self.dcode = ''

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

    def literal(proto_name):
        return self.program.name +  "_data->" + self.identifier

    def __str__(self):
        return self.identifier




class Create(Stat):
    #Create() can only be called once in a protocol.
    def __init__(self, identifier, initial_map):
        self.identifier = identifier
        self.initial_map = initial_map
    
    def literal(proto_name):
        code = f'{proto_name}_instance = (struct {proto_name}_instance_t*)\
            malloc(sizeof(struct {proto_name}_instance_t));\n'
        code += f'memset({proto_name}_instance, 0, sizeof(struct \
            {proto_name}_select_t));\n'
        for key, value in self.initial_map.items():
            code += f'{key.literal(proto_name)} = {value.literal(proto_name)};\n'
        code += f'{proto_name}_instance->{proto_name}_select = *{proto_name}_select;\n'
        code += f'{proto_name}_instance->{proto_name}_data = {proto_name}_data;\n'
        code += f'{proto_name}_instance->state = ?;\n'
        code += f'{proto_name}_instance->rec_ptr = timer_update(\
            &{proto_name}_list, {proto_name}_instance, NULL, now);\n'
        code += f'init_buf_list(&{proto_name}_instance->bufs);\n'
        code += f'hash = {proto_name}_hash({proto_name}_select);\n'
        code += f'tommy_hashdyn_insert(&{proto_name}_hashtable, \
            &{proto_name}_instance->node, {proto_name}_instance, hash);\n'
        self.ecode = code
        return code        

    def __str__(self):
        return (
            'Create @ ' + str(self.identifier) + ': ' + 
            str_dict(self.initial_map)
        )


class Contain(Expr):
    def __init__(self, identifier):
        self.identifier = identifier

    def literal(proto_name):
        return f'{proto_name}_instance = tommy_hashdyn_search(&{proto_name}_hashtable, \
            {proto_name}_compare, {proto_name}_select, {self.identifier.literal(proto_name)})'

    def __str__(self):
        return 'CONTAIN ' + str(self.identifier)


class Delete(Stat):
    def __str__(self):
        return 'DELETE'

    def literal(proto_name):
        # TODO: connection type should be specified
        code = f"\tfree_buf_list({proto_name}_instance->bufs);\n"
        code += f"\ttommy_hashdyn_remove_existing(&{proto_name} \
            _hashtable, &{proto_name}_instance->node);\n"
        code += f"\tif({proto_name}_instance->time_record_leader) deregister_timer(&\
            {proto_name}_list, {proto_name}_instance->rec_ptr);\n"
        # TODO: I should whether this layer has perm data
        # code += "\tfree({proto_name}_instance->{proto_name}_data);\n"
        code += f"\tfree({distinction}_instance->is_active_part);\n"
        code += f"\tfree({distinction}_instance);\n"

class Constant(Expr):
    def __init__(self, value):
        self.value = value

    def literal(proto_name):
        return str(self.value)

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