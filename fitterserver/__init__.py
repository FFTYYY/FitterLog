from YTools.network.server.server import start_server
from fitterlog.interface.restore import load_noun_number , load_syntax , load_last
from fitterlog.core.morphology import Noun , Predicate

def noun_cnt(request):
	return load_noun_number()
def ask_syntax(request , noun_id):
	the_noun = Noun(noun_id)
	return load_syntax(the_noun)

start_server(ip = "127.0.0.1" , port = "7899" , responsers = {
	"noun_cnt" : noun_cnt , 
	"ask_syntax/<int:noun_id>" : ask_syntax , 
})