import os
from YTools.client.cui import CUI
from YTools.universe.beautiful_str import merge_str
from YTools.network.server.client import Requester
from fitterlog.interface.restore import load_noun_number
from base64 import b64encode , b64decode

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

def processer_ask_val(ui , cmd):
	noun_id = int(cmd[1])
	pred_name = (" ".join(cmd[2:])).encode("utf-8")
	pred_name = str( b64encode(  pred_name ) , encoding = "utf-8")
	val = ui.req.request("ask_val/{noun_id}/{pred_name}".format(noun_id = noun_id , pred_name = pred_name))
	ui.output(val)

def processer_ask_all(ui , cmd):
	noun_id = int(cmd[1])
	pred_name = (" ".join(cmd[2:])).encode("utf-8")
	pred_name = str( b64encode(  pred_name ) , encoding = "utf-8")
	val = ui.req.request("ask_all/{noun_id}/{pred_name}".format(noun_id = noun_id , pred_name = pred_name))
	ui.output(val)


def main():
	ui = CUI()
	ui.add_processor("conn" 	  , processer_connect   , "[ip:str , port: int] give ip & port")
	ui.add_processor("noun_cnt"   , processer_noun_cnt  , "[] ask number of nouns")
	ui.add_processor("syntax" , processer_ask_syntax    , "[noun_id: int] ask syntax of specific noun")
	ui.add_processor("askval" , processer_ask_val       , "[noun_id: int, pred_name: str] ask a certain value")
	ui.add_processor("askall" , processer_ask_all       , "[noun_id: int, pred_name: str] ask all values")
	ui.fake_input("conn 127.0.0.1 7898")
	ui.fake_input("noun_cnt")
	ui.fake_input("syntax 346")
	ui.fake_input("askval 346 test loss")
	ui.run() 

if __name__ == "__main__":
	main()
