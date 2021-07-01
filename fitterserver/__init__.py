from YTools.network.server.server import start_server
from fitterlog.interface.restore import load_noun_number , load_syntax , load_last , load_all
from fitterlog.core.morphology import Noun , Predicate
from base64 import b64encode , b64decode
import django


if __name__ == "__main__":
	from table_page import ask_datas

	start_server(ip = "127.0.0.1" , port = "7899" , responsers = {
		"ask_datas"  : ask_datas , 
	} , encode = "json" , cross_domain = True)