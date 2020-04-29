from fitterlog.arg_proxy import ArgProxy
import math as M
import random

arg_proxy = ArgProxy()
arg_proxy.add_argument("n" , type = lambda x: M.sqrt(int(x)) , default = 10)
arg_proxy.add_argument("info" , type = str , default = "haha")
arg_proxy.add_argument("lr" , type = float , default = 0.1)
arg_proxy.add_argument("batch size" , type = int , default = 32)
arg_proxy.add_argument("num_steps" , type = float , default = 1000)
arg_proxy.add_argument("yyy" , type = float , default = 0.23333)
arg_proxy.add_argument("num_layers" , type = int , default = 6)
arg_proxy.add_argument("num_head" , type = int , default = 6)
arg_proxy.add_argument("ui" , type = float , default = 0.23333)
arg_proxy.add_argument("a rand val" , type = int , default = random.random())

__all__ = [
	arg_proxy , 
]