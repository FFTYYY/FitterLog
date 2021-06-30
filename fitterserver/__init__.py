from YTools.network.server.server import start_server
from fitterlog.interface.restore import load_noun_number , load_syntax , load_last , load_all
from fitterlog.core.morphology import Noun , Predicate
from base64 import b64encode , b64decode

def noun_cnt(request):
	return load_noun_number()

def ask_syntax(request , noun_id):
	the_noun = Noun(noun_id)
	return load_syntax(the_noun)

def ask_val(request , noun_id , pred_name):
	the_noun = Noun(noun_id)
	the_pred = Predicate(str(b64decode(pred_name) , encoding = "utf-8"))
	return load_last(the_noun , the_pred , False)

def ask_all(request , noun_id , pred_name):
	the_noun = Noun(noun_id)
	the_pred = Predicate(str(b64decode(pred_name) , encoding = "utf-8"))
	return load_all(the_noun , the_pred , False)

if __name__ == "__main__":
	from table_page import ask_titles , ask_datas

	start_server(ip = "127.0.0.1" , port = "7899" , responsers = {
		"noun_cnt" : noun_cnt , 
		"ask_syntax/<int:noun_id>" : ask_syntax , 
		"ask_all/<int:noun_id>/<str:pred_name>" : ask_all , 
		"ask_val/<int:noun_id>/<str:pred_name>" : ask_val , 
		"ask_titles" : ask_titles , 
		"ask_datas"  : ask_datas , 
	} , encode = "json" , cross_domain = True)