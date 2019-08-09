class Op(Expr):
	self.op_dict = {'add': '+',
		'equal': '=='}

    def __init__(self, type, operand_list):
        self.type = type
        self.operand_list = operand_list
        self.hcode = ''
        self.dcode = ''
        self.ecode = ''
    def literal(proto_name):
    	if self.type not in self.op_dict.keys():
    		handler = getattr(self, "handle_" + self.type)
    	else:
    		handler = self.op_trans
    	return handler(proto_name)

    def handle_hash(proto_name):
    	#To use hash, the presumption is every protocol will only hash their keys once.
    	#cannot deduct the length of key
    	self.hcode = f'{proto_name}_select_t{{\n'
    	for operand in self.operand_list:
    		#uint32_t is pure makeup
    		self.hcode += f'\tuint32_t {operand.literal(proto_name, literal)};\n'
    	self.hcode += "};\n"

    	# self.dcode = f'struct {proto_name}_select_t* {proto_name}_select;\n'

    	self.ecode = f"{proto_name}_hash({proto_name}_select)\n"

    	return self.ecode

    def op_trans(proto_name):
    	return self.operand_list[0].literal() + self.op_dict[self.type] + self.operand_list[1].literal()

    def __str__(self):
        return (
            'OP:' + self.type + '(' + 
            str_list([str(operand) for operand in self.operand_list]) +
            ')'
        )