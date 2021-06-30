import axios from "axios"


export default async function get_data(v){

	/*这是个异步函数，从远端获取数据并更新给定对象的data.columns和data.datas两厢*/
	let title_resp = await axios.post("http://127.0.0.1:7899/ask_titles" , {from:19 , to:40})
	let data_resp  = await axios.post("http://127.0.0.1:7899/ask_datas"  , {from:19 , to:40})

	v.$data.title_list = title_resp.data
	v.$data.data_dict  = data_resp.data
}