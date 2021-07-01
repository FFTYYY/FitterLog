import axios from "axios"

function isnull(o){
	return o == null || o == undefined || o == ""
}

export function make_filter(filter_items){
	let filter = {}
	for(let item of filter_items){
		if(item.pred == null) continue

		if(item.opr == "fitter-opt:exists")
		{
			filter[item.pred] = {
				"type" : "exists",
			}
		}
		if(item.opr == "fitter-opt:regular")
		{
			filter[item.pred] = {
				"type" : "regular",
				"cond" : isnull(item.content1) ? "" : item.content1, // null转成匹配全部
			}
		}
		if(item.opr == "fitter-opt:interval")
		{
			filter[item.pred] = {
				"type" : "interval",
				"cond" : [
					isnull(item.content1) ? "-inf" : item.content1, // null转成inf
					isnull(item.content2) ? "inf"  : item.content2,
				], 
			}
		}
	}
	return filter
}

export async function get_data(v , filter){

	/*这是个异步函数，从远端获取数据并更新给定对象的data.columns和data.datas两厢*/
	let title_resp = await axios.post("http://127.0.0.1:7899/ask_titles" , {from:19 , to:40 , filter: filter})
	let data_resp  = await axios.post("http://127.0.0.1:7899/ask_datas"  , {from:19 , to:40 , filter: filter})

	v.$data.title_list = title_resp.data
	v.$data.data_dict  = data_resp .data
}
