CONNECTION_ORIENTED = 0
CONNECTIONLESS = 1

class static_code_gen:
	def __init__(self, proto_name, ctype):
		self.proto_name = proto_name
		self.type = ctype
		self.hcode = ""
		self.dcode = ""
	def generate(self):
		pass

	def globals_gen(self):
		# TODO: if the buf operation is used define AVL shreshold
		if self.type = CONNECTION_ORIENTED:
	        code += f"struct{self.proto_name}_instance_t* {self.proto_name}_instance_reverse;\n"
	        code += f"struct{self.proto_name}_select_t* {self.proto_name}_select_reverse;\n"
	        code += f"struct{self.proto_name}_instance_t* {self.proto_name}_fake_instance_reverse;\n"
		code += f"struct{self.proto_name}_instance_t* {self.proto_name}_instance;\n"
        code += f"struct{self.proto_name}_select_t* {self.proto_name}_select;\n"
        code += f"struct{self.proto_name}_instance_t* {self.proto_name}_fake_instance;\n"
        code += f"tommy_hashdyn {self.proto_name}_hashtable;\n"
        code += f"struct timer {self.proto_name}_list;\n"
        code += f"struct timeval {self.proto_name}_gap;\n"
        # TODO dump all protocol headers
		# TODO if there is perm data, define it
		code += f"char {self.distinction}_has_buf = 0;\n"
        code += f"u_char* {self.distinction}_buf;\n"
        code += f"int {self.distinction}_buf_length;\n"
        code += f"u_char* {self.distinction}_payload;\n"
        code += f"int {self.distinction}_payload_length;\n"
        code += f"struct {self.distinction}_rubik_bitmap_t* {
                self.distinction}_rubik_bitmap;\n"
        code += f"struct {self.distinction}_transition_bitmap_t* {
                self.distinction}_transition_bitmap;\n"
        return code

    def init_gen(self):
    		# TODO if define timeout init the gap
    # if root.timeout:
    #     code += "\t" + root.distinction + \
    #         "_gap.tv_sec = " + str(root.timeout) + ";\n"
    # else:
    #     code += "\t" + root.distinction + \
    #         "_gap.tv_sec = 10;\n"
    	code = "\
void {0}_init(){\
    tommy_hashdyn_init(&{0}_hashtable);\
    {0}_gap.tv_usec = 0;\
    {0}_list.head = NULL;\
    {0}_list.tail = NULL;\
    {0}_instance = NULL;\
    {0}_fake_instance = malloc(sizeof(struct " + \
            root.distinction + "_instance_t));\
    {0}_fake_instance->is_active_part = malloc(sizeof(char));\
    *({0}_fake_instance->is_active_part) = 1;\
    {0}_fake_instance->stand = 0;\
    {0}_select = malloc(sizeof(struct {0}_select_t));\
    memset({0}_select, 0, sizeof(struct {0}_select_t));\
    {0}_rubik_bitmap = malloc(sizeof(struct {0}_rubik_bitmap_t));\
    {0}_transition_bitmap = malloc(sizeof(struct {0}_transition_bitmap_t));\
    memset({0}_rubik_bitmap, 0, sizeof(struct {0}_rubik_bitmap_t));\
    memset({0}_transition_bitmap, 0, sizeof(struct {0}_transition_bitmap_t));".format(self.proto_name)
    # check what is this? 
    # for malloc in malloc_list:
    #         code += "\t" + malloc + \
    #             " = malloc(sizeof(struct " + malloc + "_t));"
	    if self.type = CONNECTION_ORIENTED:
	    	code += '{0}_fake_instance_reverse = malloc(sizeof(struct {0}_instance_t));\
	    	{0}_fake_instance_reverse->is_active_part = {0}_fake_instance->is_active_part;\
	    	{0}_fake_instance_reverse->stand = 1;\
	    	memset({0}_select_reverse, 0, sizeof(struct {0}_select_t));\
	    	{0}_select_reverse = malloc(sizeof(struct {0}_select_t));'.format(self.proto_name)

	    code += "}\n"
	    return code

	def hash_func_gen(self):
		code = "\
uint32_t {0}_hash(void * obj){\n\
	uint64_t size = sizeof(struct {0}_select_t);\n\
	return tommy_hash_u32(0, obj, size);\n\
}\n".format(self.proto_name)
		# TODO consider introduce variable length field into hash function




