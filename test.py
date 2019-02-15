import math as m

e = m.e
pi = m.pi

func_list = ['sin','cos','tan','csc','sec','cot','log_','sqrt']
const_list = ['e','pi']
variable_list = ['x','y','z']

def tokenizer(A):

	A = A.strip()

	if len(A) == 0: return 'empty input'

	single = ['+','-','*','/','(',')','|','^','x','y','z','e']
	# x,y,z are the only letters for variable 
	num = ['0','1','2','3','4','5','6','7','8','9']
	word_2 = ['pi']
	word_3 = ['sin','cos','tan','csc','sec','cot']
	word_4 = ['sqrt', 'log_']

	tokens = []
	loc = 0

	l = len(A)

	while(loc < l):
		if A[0:4] in word_4:
			tokens.append((A[0:4], loc))
			loc += 4
			A = A[4:]
		elif A[0:3] in word_3:
			tokens.append((A[0:3], loc))
			loc += 3
			A = A[3:]
		elif A[0:2] in word_2:
			tokens.append((A[0:2], loc))
			loc += 2
			A = A[2:]
		elif A[0] in single:
			tokens.append((A[0], loc))
			loc += 1
			A = A[1:]
		elif A[0] in num:				 # possible: 012, 012.34(start with zero), 12.(end with decimal point) // impossible: .12 (start with decimal point)
			temp = 1
			while(A[temp:temp+1] in num):
				temp += 1
			if A[temp:temp+1] == '.':
				temp += 1
				while (A[temp:temp+1] in num):
					temp += 1
			tokens.append((A[0:temp], loc))
			loc += temp
			A = A[temp:]
		elif A[0] == ' ':
			loc += 1
			A = A[1:]
		else:
			return 'improper letter at index {}'.format(loc)  # current loc has the location which raise the tokenizing error.

	tokens.append(('EOL', loc))

	return tokens

class Tree:
	def __init__(self):
		pass
	def differential(self):
		pass
	def canonical(self):
		pass
	def evaluate(self, x, y, z):
		temp = []
		for i in range(len(self.operand)):
			temp.append(self.operand[i].evaluate(x,y,z))
		self.operand = temp
		return self

	


class AddTree(Tree):
	def __init__(self):
		self.operand = []

	def __str__(self):
		output = ''
		if len(self.operand) > 1:
			output += '('+str(self.operand[0])+')'
			for i in self.operand[1:]:
				output += '+'
				output += '('+str(i)+')'
			return output
		else:
			return str(self.operand[0])

	def push(self, operand):
		if type(operand) == list:
			for i in operand:
				self.operand.append(i)
		else:
			self.operand.append(operand)
	def canonical(self):
		add_tree = AddTree()
		for operand in self.operand:
			add_tree.push(operand.canonical())

		for i in range(len(add_tree.operand)):
			if isinstance(add_tree.operand[i], AddTree):
				temp = add_tree.operand.pop(i).operand
				add_tree.push(temp)
				return add_tree.canonical()

		temp_dict = {'&': 0}		
		for i in add_tree.operand:
			if not isinstance(i, NumUnit):

				coeff_tree = MulTree()
				coeff_tree.push(NumUnit(1))
				coeff_tree.push(i)
				coeff_tree = coeff_tree.canonical()
				#print('coeff_op: {}'.format(coeff_tree.operand))

				if len(coeff_tree.operand[1:]) > 1:
					term_tree= MulTree()
					term_tree.push(coeff_tree.operand[1:])
				else:
					term_tree = coeff_tree.operand[1]
				#print('term_tr.{}'.format(term_tree))

				if str(term_tree) not in temp_dict.keys():
					temp_dict[str(term_tree)] = (term_tree, coeff_tree.operand[0])
				else:
					add_exp = AddTree()
					add_exp.push(temp_dict[str(term_tree)][1])
					add_exp.push(coeff_tree.operand[0])
					add_exp = add_exp.canonical()
					temp_dict[str(term_tree)] = (term_tree, add_exp)
			
			else:
				temp_dict['&'] += i.value

		#print('addtree_dict: {}'.format(temp_dict))

		sorting = list(temp_dict.keys())
		sorting.sort()

		for i in sorting[1:]:
			#print(temp_dict[i][1].value)
			if isinstance(temp_dict[i][1], NumUnit):
				if temp_dict[i][1].value == 0:
					temp_dict.pop(i)

		#print(temp_dict)

		if len(temp_dict) == 1:
			return NumUnit(temp_dict['&'])
		else:
			if temp_dict['&'] == 0:
				temp_dict.pop('&')
			add_tree.operand = []
			sorting = list(temp_dict.keys())
			sorting.sort()
			#print(sorting)
			for i in sorting:
				if i == '&':
					add_tree.push(NumUnit(temp_dict[i]))
				# elif isinstance(temp_dict[i][1], NumUnit) & temp_dict[i][1].value == 1:
				# 	mul_tree.push(temp_dict[i][0])
				else:
					mul_tree = MulTree()
					mul_tree.push(temp_dict[i][1])
					mul_tree.push(temp_dict[i][0])
					add_tree.push(mul_tree)#.canonical())

			return add_tree#.canonical()

	def diff(self, var):
		temp = []
		for i in range(len(self.operand)):
			temp.append(self.operand[i].diff(var))
		add_tree = AddTree()
		add_tree.push(temp)
		return add_tree



class MulTree(Tree):
	def __init__(self):
		self.operand = []
		#self.coeff = NumUnit(1)
	def __str__(self):
		output = ''
		if len(self.operand) > 1:
			output += '('+str(self.operand[0])+')'
			for i in self.operand[1:]:
				output += '*'
				output += '('+str(i)+')'
			return output
		else:
			return str(self.operand[0])
		
	def push(self, operand):
		if type(operand) == list:
			for i in operand:
				self.operand.append(i)
		else:
			self.operand.append(operand)
	def canonical(self):
		mul_tree = MulTree()
		for operand in self.operand:
			mul_tree.push(operand.canonical())

		for i in range(len(mul_tree.operand)):
			if isinstance(mul_tree.operand[i], MulTree):
				temp = mul_tree.operand.pop(i).operand
				mul_tree.push(temp)
				return mul_tree.canonical()
		
		for i in range(len(mul_tree.operand)):
			if isinstance(mul_tree.operand[i], AddTree):
				expand_tree = AddTree()
				add_operand = mul_tree.operand.pop(i).operand
				for i in add_operand:
					temp = MulTree()
					temp.push(i)
					temp.push(mul_tree.operand)
					temp = temp.canonical()
					expand_tree.push(temp)
				return expand_tree.canonical()
		

		temp_dict = {'&': 1}      					# '&' == 'NumUnit'
		for i in mul_tree.operand:
			if isinstance(i, PowerTree):
				if str(i.base) not in temp_dict.keys():
					temp_dict[str(i.base)] = (i.base, i.exponent)
				else:
					add_exp = AddTree()
					add_exp.push(temp_dict[str(i.base)][1])
					add_exp.push(i.exponent)
					add_exp = add_exp.canonical()
					temp_dict[str(i.base)] = (i.base, add_exp)
			elif isinstance(i, Term):
				if str(i) not in temp_dict.keys():
					temp_dict[str(i)] = (i, NumUnit(1))
				else:
					add_exp = AddTree()
					add_exp.push(temp_dict[str(i)][1])
					add_exp.push(NumUnit(1))
					add_exp = add_exp.canonical()
					temp_dict[str(i)] = (i, add_exp)
			else:
				temp_dict['&'] *= i.value
		#print('multree_dict: {}'.format(temp_dict))

		sorting = list(temp_dict.keys())
		sorting.sort()
		# print(sorting)
		sorting.pop(0)
		# print(sorting)
		for i in sorting:
			if isinstance(temp_dict[i][1], NumUnit):
				if temp_dict[i][1].value == 0:
					temp_dict.pop(i)


		if temp_dict['&'] == 0:
			return NumUnit(0)
		elif len(temp_dict) == 1:
			return NumUnit(temp_dict['&'])
		else:
			mul_tree.operand = []
			sorting = list(temp_dict.keys())
			sorting.sort()
			for i in sorting:
				if i == '&':
					mul_tree.push(NumUnit(temp_dict[i]))
				# elif isinstance(temp_dict[i][1], NumUnit) & temp_dict[i][1].value == 1:
				# 	mul_tree.push(temp_dict[i][0])
				else:
					mul_tree.push(PowerTree(temp_dict[i][0], temp_dict[i][1]).canonical())#.canonical())
			
			return mul_tree#.canonical()

	def diff(self, var):
		add_tree = AddTree()
		for i in range(len(self.operand)):
			mul_tree = MulTree()
			for j in range(len(self.operand)):
				if j == i:
					mul_tree.push(self.operand[j].diff(var))
				else:
					mul_tree.push(self.operand[j])
			add_tree.push(mul_tree)
			
		return add_tree


			

class NonTree:
	def __init__(self, term):
		self.term = term
	def evaluate(self, x, y, z):
		self.term = self.term.evaluate(x,y,z)
		return self.canonical()




class MinusSignTree(NonTree):
	def __str__(self):
		return '-({})'.format(self.term)                          #dont wrap outside                       
	def canonical(self):
		_term = self.term
		mul_tree = MulTree()
		mul_tree.push(NumUnit(-1))
		mul_tree.push(_term)
		return mul_tree.canonical()
	def diff(self, var):
		self.term = self.term.diff(var)
		return self.canonical()

class Unit:
	pass

class Term(Unit):
	pass

class ReciprocalTree(Term, NonTree):
	def __str__(self):
		return '1/({})'.format(self.term)
	def canonical(self):
		_denominator = self.term.canonical()
		if isinstance(_denominator, NumUnit):
			return NumUnit(1/float(_denominator.value))
		else:
			return ReciprocalTree(_denominator)
	def diff(self, var):
		temp = self.term.diff(var)
		denom = ReciprocalTree(PowerTree(self.term, NumUnit(2)).canonical())
		mul_tree = MulTree()
		mul_tree.push(NumUnit(-1))
		mul_tree.push(temp)
		mul_tree.push(denom)
		return mul_tree.canonical()


class SinTree(Term, NonTree):
	def __str__(self):
		return 'sin({})'.format(self.term)
	def canonical(self):
		_sin_value = self.term.canonical()
		if isinstance(_sin_value, NumUnit):
			return NumUnit(m.sin(_sin_value.value))
		else:
			return  SinTree(_sin_value)
	def diff(self, var):
		temp = self.term.diff(var)
		cos_tree = CosTree(self.term)
		mul_tree = MulTree()
		mul_tree.push(cos_tree)
		mul_tree.push(temp)
		return mul_tree.canonical()

class CosTree(Term, NonTree):
	def __str__(self):
		return 'cos({})'.format(self.term)
	def canonical(self):
		_cos_value = self.term.canonical()
		if isinstance(_cos_value, NumUnit):
			return NumUnit(m.cos(_cos_value.value))
		else:
			return CosTree(_cos_value)
	def diff(self, var):
		temp = self.term.diff(var)
		sin_tree = SinTree(self.term)
		mul_tree = MulTree()
		mul_tree.push(NumUnit(-1))
		mul_tree.push(sin_tree)
		mul_tree.push(temp)
		return mul_tree.canonical()

class TanTree(Term, NonTree):
	def __str__(self):
		return 'tan({})'.format(self.term)
	def canonical(self):
		_tan_value = self.term.canonical()
		if isinstance(_tan_value, NumUnit):
			return NumUnit(m.tan(_tan_value.value))
		else:
			return TanTree(_tan_value)
	def diff(self, var):
		temp = self.term.diff(var)
		sec_tree = PowerTree(SecTree(self.term), NumUnit(2)).canonical()
		mul_tree = MulTree()		
		mul_tree.push(sec_tree)
		mul_tree.push(temp)
		return mul_tree.canonical()

class CscTree(Term, NonTree):
	def __str__(self):
		return 'csc({})'.format(self.term)
	def canonical(self):
		_csc_value = self.term.canonical()
		if isinstance(_csc_value, NumUnit):
			return NumUnit(1/m.sin(_csc_value.value))
		else:
			return CscTree(_csc_value)
	def diff(self, var):
		temp = self.term.diff(var)
		cot_tree = CotTree(self.term)
		mul_tree = MulTree()
		mul_tree.push(NumUnit(-1))
		mul_tree.push(self)
		mul_tree.push(cot_tree)
		mul_tree.push(temp)
		return mul_tree.canonical()

class SecTree(Term, NonTree):
	def __str__(self):
		return 'sec({})'.format(self.term)
	def canonical(self):
		_sec_value = self.term.canonical()
		if isinstance(_sec_value, NumUnit):
			return NumUnit(1/m.cos(_sec_value.value))
		else:
			return SecTree(_sec_value)
	def diff(self, var):
		temp = self.term.diff(var)
		tan_tree = TanTree(self.term)
		mul_tree = MulTree()
		mul_tree.push(self)
		mul_tree.push(tan_tree)
		mul_tree.push(temp)
		return mul_tree.canonical()

class CotTree(Term, NonTree):
	def __str__(self):
		return 'cot({})'.format(self.term)
	def canonical(self):
		_cot_value = self.term.canonical()
		if isinstance(_cot_value, NumUnit):
			return NumUnit(1/m.tan(_cot_value.value))
		else:
			return CotTree(_cot_value)
	def diff(self, var):
		temp = self.term.diff(var)
		csc_tree = PowerTree(CscTree(self.term), NumUnit(2)).canonical()
		mul_tree = MulTree()
		mul_tree.push(NumUnit(-1))		
		mul_tree.push(csc_tree)
		mul_tree.push(temp)
		return mul_tree.canonical()

class LnTree(Term, NonTree):
	def __str__(self):
		return 'log({})'.format(self.term)		
	def canonical(self):
		_log_value = self.term.canonical()
		if isinstance(_log_value, NumUnit):
			return NumUnit(m.log(_log_value.value))
		else:
			return LnTree(_log_value)
	def diff(self, var):
		temp = self.term.diff(var)
		denom = ReciprocalTree(self.term)
		mul_tree = MulTree()
		mul_tree.push(temp)
		mul_tree.push(denom)
		return mul_tree.canonical()

#At this point, we dont know whether it is PolyTree(natural exp, should expand), FloatPolyTree or ExpTree
class PowerTree:
	def __init__(self, base, exponent):
		self.base = base
		self.exponent = exponent
	def __str__(self):
		return '({})^({})'.format(self.base, self.exponent)
	def canonical(self):
		_base = self.base.canonical()
		_exp = self.exponent.canonical()

		if isinstance(_base, NumUnit) & isinstance(_exp, NumUnit):
			return NumUnit(_base.value**_exp.value)

		if isinstance(_base, PowerTree):
			if isinstance(_exp, NumUnit):
				if _exp.value-int(_exp.value):
					return FloatPolyTree(_base, _exp)
			if isinstance(_base, FloatPolyTree) & isinstance(_exp, NumUnit):
				if (_exp.value == int(_exp.value)) & (_exp.value>1):
					return PolyTree(_base, _exp)
			mul_tree = MulTree()
			mul_tree.push(_base.exponent)
			mul_tree.push(_exp)
			return PowerTree(_base.base, mul_tree).canonical()


		if isinstance(_base, MulTree):
			mul_tree = MulTree()
			for operand in _base.operand:
				mul_tree.push(PowerTree(operand, _exp).canonical())
			return mul_tree.canonical()

		if isinstance(_base, NumUnit):
			if _base.value == 0:
				return NumUnit(0)

		if isinstance(_exp, NumUnit):
			if _exp.value == 1:
				return _base
			elif _exp.value == 0:
				return NumUnit(1)
			elif _exp.value < 0:
				return ReciprocalTree(PowerTree(_base, NumUnit(_exp.value*(-1))).canonical())   ############

		if isinstance(_exp, NumUnit):
			if (_exp.value > 1) & (_exp.value == int(_exp.value)):
				if isinstance(_base, AddTree):
					mul_tree = MulTree()
					for i in range(int(_exp.value)):
						mul_tree.push(_base)
					return mul_tree.canonical()

		if isinstance(_exp, NumUnit):
			if _exp.value != int(_exp.value):
				return FloatPolyTree(_base, _exp)
			else:
				return PolyTree(_base, _exp)
		else:
			mul_tree = MulTree()
			mul_tree.push(_exp)
			mul_tree.push(LnTree(_base))
			return ExpTree(NumUnit(e), mul_tree.canonical())
		
	def evaluate(self, x, y, z):
		_base = self.base.evaluate(x,y,z)
		_exp = self.exponent.evaluate(x,y,z)
		return PowerTree(_base, _exp).canonical()


class FloatPolyTree(PowerTree):   #(except NumUnit, MulTree)^float(>0)
	def diff(self, var):
		temp = self.base.diff(var)
		_exp = NumUnit(self.exponent.value-1)
		power = PowerTree(self.base, _exp).canonical()
		mul_tree = MulTree()
		mul_tree.push(self.exponent)
		mul_tree.push(power)
		mul_tree.push(temp)
		return mul_tree.canonical()

class PolyTree(FloatPolyTree): #(VarUnit or FloatPoly or Term)^integer(>1)
	pass

class ExpTree(PowerTree):
	
	def diff(self, var):
		term = self.exponent.diff(var)
		mul_tree = MulTree()
		mul_tree.push(term)
		mul_tree.push(self)
		return mul_tree.canonical()



class NumUnit(Unit):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return '{}'.format(self.value)
	def canonical(self):
		return self
	def evaluate(self, x, y, z):
		return self
	def diff(self, var):
		return NumUnit(0)

class Variable:
	def __init__(self):
		pass
	def canonical(self):
		return self
	def diff(self, var):     ######################
		if str(self) == var:
			return NumUnit(1)
		else:
			return NumUnit(0)



class VarUnit_x(Term, Variable):
	def __str__(self):
		return 'x'
	def evaluate(self, x, y, z):
		return NumUnit(x)
	

class VarUnit_y(Term, Variable):
	def __str__(self):
		return 'y'
	def evaluate(self, x, y, z):
		return NumUnit(y)


class VarUnit_z(Term, Variable):
	def __str__(self):
		return 'z'
	def evaluate(self, x, y, z):
		return NumUnit(z)


##################returned class from canonical function should be re-defined as a canonical-class? (ex. NumUnit->CanNumUnit)##################

def parser(tokens):
	tree = takeAddTree(tokens)
	takeIt(tokens, ['EOL'])
	return tree

def takeAddTree(tokens):
	mul_tree = takeMulTree(tokens)
	if tokens[0][0] in ['+','-']:
		add_tree = AddTree()
		add_tree.push(mul_tree)
		while(tokens[0][0] in ['+','-']):
			op = takeIt(tokens, ['+','-'])
			mul_tree = takeMulTree(tokens)
			if op == '+':
				add_tree.push(mul_tree)
			else:
				add_tree.push(MinusSignTree(mul_tree))
		return add_tree
	else:
		return mul_tree

def takeMulTree(tokens):
	func_tree = takeFuncTree(tokens)
	if tokens[0][0] in ['*','/']:
		mul_tree = MulTree()
		mul_tree.push(func_tree)
		while(tokens[0][0] in ['*','/']):
			op = takeIt(tokens, ['*','/'])
			func_tree = takeFuncTree(tokens)
			if op == '*':
				mul_tree.push(func_tree)
			else:
				mul_tree.push(ReciprocalTree(func_tree))
		return mul_tree
	else:
		return func_tree



def takeFuncTree(tokens):
	if tokens[0][0] == '-':
		takeIt(tokens, ['-'])
		return MinusSignTree(takeFuncTree(tokens))
	elif tokens[0][0] in func_list:
		func = takeIt(tokens, func_list)
		if func == 'sin':
			return SinTree(takeFuncTree(tokens))
		elif func == 'cos':
			return CosTree(takeFuncTree(tokens))
		elif func == 'tan':
			return TanTree(takeFuncTree(tokens))
		elif func == 'csc':
			return CscTree(takeFuncTree(tokens))
		elif func == 'sec':
			return SecTree(takeFuncTree(tokens))
		elif func == 'cot':
			return CotTree(takeFuncTree(tokens))
		elif func == 'log_':
			base = takeFuncTree(tokens)
			log_value = takeFuncTree(tokens)
			mul_tree = MulTree()
			mul_tree.push(LnTree(log_value))
			mul_tree.push(ReciprocalTree(LnTree(base)))
			return mul_tree
		elif func == 'sqrt':
			return PowerTree(takeFuncTree(tokens), NumUnit(0.5))
	else:
		return takeUnitTree(tokens)                				           

var_dic = {'x': VarUnit_x(), 'y': VarUnit_y(), 'z': VarUnit_z()}
const_dic = {'e':e, 'pi':pi}

def takeUnitTree(tokens):
	if tokens[0][0] == '(':
		takeIt(tokens, ['('])
		base = takeAddTree(tokens)                                         
		takeIt(tokens, [')'])
	elif tokens[0][0] == '|':
		takeIt(tokens, ['|'])
		base = PowerTree(PowerTree(takeAddTree(tokens), NumUnit(2)), NumUnit(0.5))
		takeIt(tokens, ['|'])
	elif tokens[0][0] in variable_list:
		var = takeIt(tokens, variable_list)
		base = var_dic[var]
	elif tokens[0][0] in const_list:
		base = NumUnit(const_dic[takeIt(tokens, const_list)])
	else:
		base = NumUnit(takeIt(tokens, 'isNumber'))


	if tokens[0][0] == '^':
		takeIt(tokens, ['^'])
		exponent = takeFuncTree(tokens)
		return PowerTree(base, exponent)
	else:
		return base

def takeIt(tokens, token_type):
	temp = tokens.pop(0)
	if token_type == 'isNumber':
		if float(temp[0])-int(float(temp[0])):
			return float(temp[0])
		else:
			return int(float(temp[0]))
	else:
		if temp[0] in token_type:
			return temp[0]
		else:
			e = MyException(temp, token_type)
			raise e


class MyException(Exception):
	def __init__(self,token_0,tokentype):
		self.token_0 = token_0
		self.tokentype = tokentype

def execute(strings, s1, s2, s3):
	try:
		tokens = tokenizer(strings)
	except:
		return ('Invalid Letters', 'Invalid Letters', '.', '.', '.', '.', '.', '.')

	try:
		expr = parser(tokens)
	except:
		return ('Invalid Equation', 'Invalid Equation', '.', '.', '.', '.', '.', '.')

	p = str(expr)

	try:	
		cano_expr = expr.canonical()
		for_diffx = expr.canonical()
		for_diffy = expr.canonical()
		for_diffz = expr.canonical()
	except:
		return ('CanonicalError', p, 'CanonicalError', '.', '.', '.', '.', '.')

	try:
		fx = for_diffx.diff('x').canonical()
		fy = for_diffy.diff('y').canonical()
		fz = for_diffz.diff('z').canonical()
	except:
		return ('DiffError', p, 'DiffError', '.', '.', '.', '.', '.')

	a = str(cano_expr)
	b = str(fx)
	c = str(fy)
	d = str(fz)

	try:
		x = parser(tokenizer(s1)).canonical().value
		y = parser(tokenizer(s2)).canonical().value
		z = parser(tokenizer(s3)).canonical().value
	except:
		return (a, p, b, c, d, 'Type proper value for variables', '.', '.')

	try:
		func_val = cano_expr.evaluate(x,y,z)
		func_val = func_val.canonical()
	except:
		return (a, p, b, c, d, 'ValueError', 'No', 'No')

	e = str(func_val)

	try:
		temp = fx.evaluate(x,y,z).canonical()
		temp = fy.evaluate(x,y,z).canonical()
		temp = fz.evaluate(x,y,z).canonical()
	except:
		return (a, p, b, c, d, e, 'Yes', 'No')

	return (a, p, b, c, d, e, 'Yes', 'Yes')



# def canonicalTree(strings):
# 	return str(parser(tokenizer(strings)).canonical())

def plot_eval(strings, x, y, z):
	try:
		temp = parser(tokenizer(strings)).canonical()
		temp2 = temp.evaluate(x,y,z)
		return temp2.canonical().value
	except:
		return 1

# def differ(strings, var):
# 	temp = parser(tokenizer(strings)).canonical()
# 	return str(temp.diff(var).canonical())

# def continuity(strings, s1, s2, s3):
# 	if 	evaluation(strings, s1, s2, s3) == 'NoValue':
# 		return 'No'
# 	else:
# 		return 'Yes'

# def differentiability(strings, s1, s2, s3):
# 	temp1 = parser(tokenizer(strings)).canonical().diff('x').canonical()
# 	temp2 = parser(tokenizer(strings)).canonical().diff('y').canonical()
# 	temp3 = parser(tokenizer(strings)).canonical().diff('z').canonical()
# 	if (evaluation(str(temp1), s1, s2, s3)=='NoValue') or (evaluation(str(temp2), s1, s2, s3)=='NoValue') or (evaluation(str(temp3), s1, s2, s3)=='NoValue'):
# 		return 'No'
# 	else:
# 		return 'Yes'


# while(1):

# 	line = raw_input('Type a equation: ')
# 	tokens = tokenizer(line)
# 	print('\ntokens: {}\n'.format(tokens))

# 	s1 = raw_input('Type a number for x (If there is no variable x, type any number): ')
# 	s2 = raw_input('Type a number for y (If there is no variable y, type any number): ')
# 	s3 = raw_input('Type a number for z (If there is no variable z, type any number): ')

# 	# x = parser(tokenizer(s1)).canonical().value
# 	# y = parser(tokenizer(s2)).canonical().value
# 	# z = parser(tokenizer(s3)).canonical().value
# 	print(execute(line, s1, s2, s3))




# 	# if isinstance(tokens, list):
# 	# 	print('\ntokens: {}\n'.format(tokens))
# 	# 	expr = parser(tokens)
# 	# 	print('Parsing completed\n')

# 	# 	print('<Parsed Tree>')
# 	# 	print(expr)

# 	# 	print('<Canonicalized Tree>')
# 	# 	print(canonicalTree(line))


# 	# 	print('<Evaluation>')
# 	# 	# expr2 = expr.evaluate(x, y, z)
# 	# 	print(evaluation(line, s1, s2, s3))

# 	# 	print('<Differentiated Tree>')
# 	# 	# expr_x = a.diff('x')
# 	# 	print('f_x: {}'.format(differ(line, 'x')))
# 	# 	# expr_y = a.diff('y')
# 	# 	print('f_y: {}'.format(differ(line, 'y')))
# 	# 	# expr_z = a.diff('z')
# 	# 	print('f_z: {}'.format(differ(line, 'z')))
		
# 	# else:
# 	# 	print(tokens)

# 	print('------------------------------------------')
