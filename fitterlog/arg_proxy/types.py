class FitterType:

	def __init__(self , func , name):
		self.name = name
		self.func = func

	def __call__(self , *pargs , **kwargs):

		return self.func(*pargs , **kwargs)

	def __str__(self):
		return self.name


Int 	= FitterType(int 												, "Int"   )
Float 	= FitterType(lambda x: round(float(x) , 6) 						, "Float" )
String 	= FitterType(str 												, "String")
Bool 	= FitterType(lambda x: x == "True" or x == "1" or x == "true" 	, "Bool"  )

# 特殊类型，表示在前端放一根分隔线
FITTER_SPLITTER = FitterType(lambda x: print("You should not see this."), "_FITTER_SPLITTER")