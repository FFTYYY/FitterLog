class FitterType:

	def __init__(self , name , func):
		self.name = name
		self.func = func

	def __call__(self , *pargs , **kwargs):

		return self.func(*pargs , **kwargs)

	def __str__(self):
		return self.name


Int 	= FitterType("Int" 		, int)
Float 	= FitterType("Float" 	, lambda x: round(float(x) , 6))
String 	= FitterType("String" 	, str)
Bool 	= FitterType("Bool" 	, lambda x: x == "True" or x == "1" or x == "true")