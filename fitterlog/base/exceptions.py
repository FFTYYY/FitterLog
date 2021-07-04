class ArgumentError(Exception):
	'''函数的参数不符合要求'''
	def __init__(self, func_name , var_name = None , var_val = None , class_name = None , note_str = None):
		''' 
		参数：
			func_name： 字符串。抛出异常的位置
			var_name： str，抛出异常的变量名
			var_val： object，抛出异常的变量值
			in_class： 如果不是None，就是某个class
		'''

		if class_name is not None:
			func_name = "{class_name}.{func_name}".format(class_name = class_name , func_name = func_name)

		if note_str is None:
			note_str = "Invalid argument value"
		
		var_str = ""
		if var_name is not None:
			var_str = ": {var_name} can not be {var_val}".format(var_name = var_name , var_val = var_val)
		
		self.args = ["{func_name}: {note_str}{var_str}".format(
			func_name = func_name , note_str = note_str , var_str = var_str
		)]

