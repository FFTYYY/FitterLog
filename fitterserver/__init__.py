from YTools.network.server.server import start_server


if __name__ == "__main__":
	from table_page import ask_datas

	start_server(ip = "127.0.0.1" , port = "7899" , responsers = {
		"ask_datas"  : ask_datas , 
	} , encode = "json" , cross_domain = True)