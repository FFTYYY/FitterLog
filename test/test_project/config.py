from fitterlog.arg_proxy import ArgProxy
import math as M

arg_proxy = ArgProxy()
arg_proxy.add_argument("n" , type = lambda x: M.sqrt(int(x)) , default = 10)
arg_proxy.add_argument("info" , type = str , default = "haha")
arg_proxy.add_argument("lr" , type = float , default = 0.1)

__all__ = [
	arg_proxy , 
]