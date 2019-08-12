class InsertMeta(Stat):
    def __init__(self, offset, length):
        self.offset = offset
        self.length = length

    def literal(proto_name):
        retrx = ''
        overlap = ''
        retrx_handle = ''
        overlap_handle = ''
        callback_code = ''
        code = ''
        code += 
        # global var current_node should be declared.
        code += "\
                    {0}_current_node = NULL;\n\
                    {0}_bufs = {0}_instance->bufs;\n\
					if({0}_bufs->is_tree || {0}_bufs->packet_count > {0}_THRESHOLD){{\n\
						struct buffer_node * node;\n\
						struct avl_node * dup = NULL;\n\
						node = malloc(sizeof(struct buffer_node));\n\
						//node->buf.buf = malloc({0}_payload_length);\n\
						//memcpy(node->buf.buf,{0}_payload, {0}_payload_length);\n\
                        {0}_current_node = node->buf;\n\
						node->buf.len = {7};\n\
						node->buf.meta = {1};// meta assignment\n\
						struct avl_node **link = &({0}_bufs->root->node); \n\
						struct avl_node *parent = NULL; \n\
						int hr = 1; \n\
						while (link[0]) {{ \n\
							parent = link[0]; \n\
							{0}_buf_length = ((struct buffer_node*)parent)->buf.len;\n\
							uint64_t meta = ((struct buffer_node*)parent)->buf.meta;\n\
							hr = COMPARE_ASC((struct avl_node *)node, parent); \n\
							{2}\n\
							{3}\n\
							if (hr == -1) {{ dup = parent; break; }} \n\
							else if (hr == 1) {{ link = &(parent->left); }} \n\
							else if (hr == 2) {{ \n\
								{4}\n\
								dup = parent; break;\n\
							}}\n\
							else if (hr == 3) {{ \n\
								{5}\n\
								dup = parent; break;\n\
							}}\n\
							else {{ link = &(parent->right); }} \n\
						}} \n\
						if (dup == NULL) {{ \n\
						{6}\n\
							if(!{0}_bufs->root->node) {0}_bufs->root->head = (struct avl_node *)node; \n\
							else if(COMPARE_ASC((struct avl_node *)node, {0}_bufs->root->head) == 1) {0}_bufs->root->head = (struct avl_node *)node; \n\
							avl_node_link((struct avl_node *)node, parent, link); \n\
							avl_node_post_insert((struct avl_node *)node, {0}_bufs->root); \n\
						}} \n\
						if(!dup){{\n\
							{0}_bufs->packet_count++;\n\
							{0}_bufs->buf_len += {7};\n\n\
						}}\n\
						else{{\n\
							free(node->buf.buf);\n\
							free(node);\n\
						}}\n\
					}}\n\
					else{{\n\
						if({0}_bufs->head->next == NULL) {{\n\
							{6}\n\
							{0}_bufs->head->next = malloc(sizeof(struct buf_list));\n\
                            {0}_current_node = {0}_bufs->head->next->buf;\
							{0}_bufs->head->next->buf.meta = {1};//meta_data_assignment here\n\
							//{0}_bufs->head->next->buf.buf = malloc({0}_payload_length);\n\
							{0}_bufs->head->next->next = NULL;\n\
							//memcpy({0}_bufs->head->next->buf.buf, {0}_payload, {0}_payload_length);\n\
							{0}_bufs->head->next->buf.len = {7};\n\
							{0}_bufs->buf_len = {7};\n\
							{0}_bufs->packet_count++;\n\
						}}\n\
						else{{\n\
							if({0}_bufs->packet_count >= {0}_THRESHOLD) {{\n\
								struct buf_list * pre_buf;\n\
								struct buf_list * cur_buf = {0}_bufs->head->next;\n\
								struct buffer_node * node;\n\
								struct avl_node * dup = NULL;\n\
								while(cur_buf != NULL) {{\n\
									dup = NULL;\n\
									node = malloc(sizeof(struct buffer_node));\n\
									node->buf = cur_buf->buf;\n\
									struct avl_node **link = &({0}_bufs->root->node); \n\
									struct avl_node *parent = NULL; \n\
									int hr = 1; \n\
									while (link[0]) {{ \n\
										parent = link[0]; \n\
										{0}_buf_length = ((struct buffer_node*)parent)->buf.len;\n\
										uint64_t meta = ((struct buffer_node*)parent)->buf.meta;\n\
										hr = COMPARE_ASC((struct avl_node *)node, parent); \n\
										{2}\n\
										{3}\n\
										if (hr == -1) {{ dup = parent; break; }} \n\
										else if (hr == 1) {{ link = &(parent->left); }} \n\
										else if (hr == 2) {{ \n\
											{4}\n\
											dup = parent; break;\n\
										}}\n\
										else if (hr == 3) {{ \n\
											{5}\n\
											dup = parent; break;\n\
										}}\n\
										else {{ link = &(parent->right); }} \n\
									}} \n\
									if (dup == NULL) {{ \n\
										if(!{0}_bufs->root->node) {0}_bufs->root->head = (struct avl_node *)node; \n\
										else if(COMPARE_ASC((struct avl_node *)node, {0}_bufs->root->head) == 1) {0}_bufs->root->head = (struct avl_node *)node; \n\
										avl_node_link((struct avl_node *)node, parent, link); \n\
										avl_node_post_insert((struct avl_node *)node, {0}_bufs->root); \n\
									}} \n\
									pre_buf = cur_buf;\n\
									cur_buf = cur_buf->next;\n\
									free(pre_buf);\n\
								}}\n\
								{0}_bufs->head->next = NULL;\n\
								node = malloc(sizeof(struct buffer_node));\n\
                                {0}_current_node = node->buf;\n\
								//node->buf.buf = malloc({0}_payload_length);\n\
								//memcpy(node->buf.buf,{0}_payload, {0}_payload_length);\n\
								node->buf.len = {7};\n\
								node->buf.meta = {1};//meta_data assignment here\n\
								struct avl_node **link = &({0}_bufs->root->node); \n\
								struct avl_node *parent = NULL; \n\
								int hr = 1; \n\
								dup = NULL; \n\
								while (link[0]) {{ \n\
									parent = link[0]; \n\
									{0}_buf_length = ((struct buffer_node*)parent)->buf.len;\n\
									uint64_t meta = ((struct buffer_node*)parent)->buf.meta;\n\
									hr = COMPARE_ASC((struct avl_node *)node, parent); \n\
									{2}\
									{3}\
									if (hr == -1) {{ dup = parent; break; }} \n\
									else if (hr == 1) {{ link = &(parent->left); }} \n\
									else if (hr == 2) {{ \n\
										{4}\
										dup = parent; break;\n\
									}}\n\
									else if (hr == 3) {{ \n\
										{5}\
										dup = parent; break;\n\
									}}\n\
									else {{ link = &(parent->right); }} \n\
								}} \n\
								if (dup == NULL) {{ \n\
									{6}\n\
									if(!{0}_bufs->root->node) {0}_bufs->root->head = (struct avl_node *)node; \n\
									else if(COMPARE_ASC((struct avl_node *)node, {0}_bufs->root->head) == 1) {0}_bufs->root->head = (struct avl_node *)node; \n\
									avl_node_link((struct avl_node *)node, parent, link); \n\
									avl_node_post_insert((struct avl_node *)node, {0}_bufs->root); \n\
								}} \n\
								if(!dup){{\n\
									{0}_bufs->packet_count++;\n\
									{0}_bufs->buf_len += {7};\n\n\
								}}\n\
								else{{\n\
									free(node);\n\
								}}\n\
								{0}_bufs->is_tree = 1;\n\
							}}\n\
							else {{\n\
								struct buf_list * pre_buf = {0}_bufs->head;\n\
								struct buf_list * cur_buf = {0}_bufs->head->next;\n\
								char inserted = 0;\n\
								while(cur_buf != NULL) {{\n\
									int hr = LIST_COMPARE_ASC(cur_buf->buf.meta, {1});\n\
									{0}_buf_length = cur_buf->buf.len;\n\
									uint64_t meta = cur_buf->buf.meta;\n\
									{2}\
									{3}\
									if(hr == 1) {{\n\
										{6}\n\
										pre_buf->next = malloc(sizeof(struct buf_list));\n\
										{0}_current_node = pre_buf->next->buf;\n\
                                        //pre_buf->next->buf.buf = malloc({0}_payload_length);\n\
										pre_buf->next->buf.len = {7};\n\
										//memcpy(pre_buf->next->buf.buf, {0}_payload, {0}_payload_length);\n\
										pre_buf->next->buf.meta = {1};//meta_data assignment here\n\
										pre_buf->next->next = cur_buf;\n\
										{0}_bufs->buf_len += {7};\n\
										{0}_bufs->packet_count++;\n\
										inserted = 1;\n\
										break;\n\
									}}\n\
									else if(hr == -1){{\n\
										inserted = 1;\n\
										break;\n\
									}}\n\
									else if(hr == 2){{\n\
										{4}\n\
										inserted = 1;\n\
										break;\n\
									}}\n\
									else if(hr == 3){{\n\
										{5}\n\
										inserted = 1;\n\
										break;\n\
									}}\n\
									else{{\n\
										pre_buf = cur_buf;\n\
										cur_buf = cur_buf->next;\n\
									}}\n\
								}}\n\
								if(!inserted) {{\n\
									{6}\n\
									pre_buf->next = malloc(sizeof(struct buf_list));\n\
                                    {0}_current_node = pre_buf->next->buf;\n\
									//pre_buf->next->buf.buf = malloc({0}_payload_length);\n\
									pre_buf->next->buf.len = {7};\n\
									//memcpy(pre_buf->next->buf.buf, {0}_payload, {0}_payload_length);\n\
									pre_buf->next->next = NULL;\n\
									pre_buf->next->buf.meta = {1};//meta_data assignment here\n\
									{0}_bufs->buf_len += {7};\n\
									{0}_bufs->packet_count++;\n\
								}}\n\
							}}\n\
						}}\n\
					}}".format(proto_name, self.offset.literal(proto_name),
                            retrx, overlap, retrx_handle, overlap_handle, callback_code, self.length.literal(proto_name))
    def __str__(self):
        return 'INSERT @' + str(self.offset) + ', len: ' + str(self.length)


class InsertData(Stat):
    def __init__(self, offset, length, payload):
        self.payload = payload

    def literal(proto_name):
        code = f"{proto_name}_current_node.buf = malloc({proto_name}_current_node.len);\n"
        code += f'memcpy({proto_name}_current_node.buf, {self.payload.literal(proto_name)}, {proto_name}_current_node.len);\n'


    def __str__(self):
        return (
            'INSERTDATA @ ' + str(self.offset) + ', len: ' + str(self.length) +
            ', payload: ' + str(self.payload)
        )


class Assemble(Stat):
    def __str__(self):
        return 'ASSEMBLE'
    def literal(proto_name):
    	code = "\
					{0}_bufs = {0}_instance->bufs;\n\
					if({0}_bufs->is_tree || {0}_bufs->packet_count > {0}_THRESHOLD){{\n\
						{0}_buf = malloc({0}_bufs->buf_len);\n\
						{0}_buf_length = {0}_bufs->buf_len;\n\
						int offset = 0;\n\
						struct avl_node * stack[{0}_bufs->packet_count];\n\
						int stack_ptr = 0;\n\
						struct avl_node * cur_ptr = {0}_bufs->root->node;\n\
						struct avl_node * tmp;\n\
						while({0}_bufs->packet_count > 0) {{\n\
							if(cur_ptr) {{\n\
								stack[stack_ptr++] = cur_ptr;\n\
								cur_ptr = cur_ptr->left;\n\
							}}\n\
							else{{\n\
								cur_ptr = stack[--stack_ptr];\n\
								memcpy({0}_buf + offset, ((struct buffer_node*)cur_ptr)->buf.buf,\n\
										((struct buffer_node*)cur_ptr)->buf.len);\n\
								offset += ((struct buffer_node*)cur_ptr)->buf.len;\n\
								free(((struct buffer_node*)cur_ptr)->buf.buf);\n\
								tmp = cur_ptr;\n\
								cur_ptr = cur_ptr->right;\n\
								free(tmp);\n\
								{0}_bufs->packet_count--;\n\
							}}\n\
						}}\n\
						{0}_bufs->buf_len = 0;\n\
						{0}_bufs->is_tree = 0;\n\
						{0}_bufs->root->node = NULL;\n\
						{0}_bufs->root->head = NULL;\n\
						{0}_has_buf = 1;\n\
					}}\n\
					else{{\n\
						{0}_buf = malloc({0}_bufs->buf_len);\n\
						{0}_buf_length = {0}_bufs->buf_len;\n\
						int offset = 0;\n\
						struct buf_list* cur_buf;\n\
						struct buf_list* pre_buf;\n\
						for(cur_buf = {0}_bufs->head->next; cur_buf != NULL;) {{\n\
							memcpy({0}_buf + offset, cur_buf->buf.buf, cur_buf->buf.len);\n\
							offset += cur_buf->buf.len;\n\
							pre_buf = cur_buf;\n\
							cur_buf = cur_buf->next;\n\
							free(pre_buf->buf.buf);\n\
							free(pre_buf);\n\
						}}\n\
						{0}_bufs->buf_len = 0;\n\
						{0}_bufs->packet_count = 0;\n\
						{0}_bufs->head->next = NULL;\n\
						{0}_has_buf = 1;\n\
						}}\n".format(proto_name)

class External(Stat):
    def __init__(self, dep_list, data=False):
        self.dep_list = dep_list
        self.data = data

    def __str__(self):
        ext = 'EXTERNAL ' + str_list(self.dep_list)
        if self.data:
            ext += ' AND DATA'
        return ext
