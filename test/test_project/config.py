from fitterlog.arg_proxy import ArgProxy
import math as M
import random

def get_arg_proxy():
	arg_proxy = ArgProxy()
	arg_proxy.add_argument("n" , type = lambda x: M.sqrt(int(x)) , default = 10)
	arg_proxy.add_argument("info" , type = str , default = "" , editable = True)
	arg_proxy.add_argument("lr" , type = float , default = 0.1)
	arg_proxy.add_argument("batch size" , type = int , default = 32)
	arg_proxy.add_argument("num_steps" , type = float , default = 1000)
	arg_proxy.add_argument("yyy" , type = float , default = 0.23333)
	arg_proxy.add_argument("num_layers" , type = int , default = 6)
	arg_proxy.add_argument("num_head" , type = int , default = 6)
	arg_proxy.add_argument("ui" , type = float , default = 0.23333)
	arg_proxy.add_argument("a rand val" , type = int , default = random.random())
	arg_proxy.add_store_true("use_kernel")
	arg_proxy.add_store_true("a variable with very very long variable name hahahahha dsfjdsfljfjfljdsfjfjsdflflf")
	arg_proxy.add_store_true("another variable with very very long variable name hahahahha dsfjdsfljfjfljdsfjfjsdflflf")
	arg_proxy.add_store_true("use_core")

	return arg_proxy

__all__ = [
	get_arg_proxy , 
]