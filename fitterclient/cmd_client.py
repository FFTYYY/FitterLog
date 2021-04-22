import os
from YTools.client.cui import CUI
from YTools.universe.beautiful_str import merge_str
from YTools.network.server.client import Requester
from fitterlog.interface.restore import load_noun_number

def noun_cnt(request):
	return load_noun_number()

def processer_connect(ui , cmd):
	inp = ui.interpret_cmd(cmd[1:] , names = ["ip" , "port"] , update_env = True)
	ui.req = Requester(ip = inp["ip"] , port = inp["port"])

def processer_noun_cnt(ui , cmd):
	# import pdb;pdb.set_trace()
	noun_cnt = ui.req.request("noun_cnt")
	ui.output(noun_cnt)
	ui.env["noun cnt"] = noun_cnt

def processer_ask_syntax(ui , cmd):
	noun_id = ui.interpret_cmd(cmd[1:] , names = ["noun_id"] , types = [int])["noun_id"]
	syntax = ui.req.request("ask_syntax/{noun_id}".format(noun_id = noun_id))
	ui.output(syntax.linearize())

def main():
	ui = CUI()
	ui.add_processor("conn" 	  , processer_connect   , "[ip:str , port: int] give ip & port")
	ui.add_processor("noun_cnt"   , processer_noun_cnt  , "[] ask number of nouns")
	ui.add_processor("syntax" , processer_ask_syntax  , "[noun_id: int] ask syntax of specific noun")
	ui.fake_input("conn 127.0.0.1 7899")
	ui.fake_input("noun_cnt")
	ui.fake_input("syntax 346")
	ui.run() 

if __name__ == "__main__":
	main()
