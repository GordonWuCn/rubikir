#temp method

import sys
sys.path.append("C:\\Users\\Gordon Wu\\Documents\\GitHub\\rubik-frontend")
import ip

class header_gen:
	def __init__(self, parser, pname):
		self.parser = parser
		self.hcode = ""
		self.dcode = ""
		self.ecode = ""
		self.pname = pname

	def gen(self):
		generator = getattr(self, "gen_" + self.parser.__class__.__name__)
		generator(self.parser)

	def gen_SeqLayout(self, layouts):
		for layout in layouts.layout_list:
			generator = getattr(self, "gen_" + layout.__class__.__name__)
			generator(layout)

	def gen_StructLayout(self, layout):
		self.gen_assignment(layout)

	def gen_IfElseLayout(self, layout):
		self.ecode += f"if({layout.guard.literal(self.pname)}){{\n"
		generator = getattr(self, "gen_" + layout.true.__class__.__name__)
		generator(layout.true)
		self.ecode += '}\nelse{\n'
		generator = getattr(self, "gen_" + layout.false.__class__.__name__)
		generator(layout.false)
		self.ecode += '}\n'

	def gen_WhileAnyLayout(self, layout):
		self.ecode += f"while({layout.guard.literal(self.pname)}){{\n"
		for l in layout.choice_list:
			ph, v = list(l.iter_field())[0]
			self.ecode += f"if((struct {self.pname}_{l.layout_type.__name__}_t *)(payload + cur_pos)" \
						  f"{v.name} == {str(v.const)}){{\n"
			generator = getattr(self, "gen_" + l.__class__.__name__)
			generator(l)
			self.ecode += "}\nelse "
		self.ecode += "{}\n}\n"

	def gen_assignment(self, header):
		header_name = f'{self.pname}_{header.layout_type.__name__}'
		self.ecode += f'{self.pname}_header_bitmap->{self.pname}_{header_name} = 1;\n'
		self.ecode += f'{header_name} = (struct {header_name}*)(payload + cur_pos);\n'
		self.ecode += 'cur_pos = cur_pos '
		for name, field in header.iter_field():
			if isinstance(field.length, int):
				self.ecode += '+ ' + str(field.length)
			else:
				self.ecode += '+ ' + field.length.literal(self.pname)
				# There will be two cases. The first one is a field in layout
				# The another one will be a Op class.
		self.ecode += ';\n'
a = header_gen(ip.ip_parser().header, "ip")
a.gen()
print(a.ecode)
