import {make_filter_title} from "../scripts/title_list_process.js"

export function titlelist2options(titlelist , father_list = []){
	/*根据远端发送的title信息生成可以直接用于options的变量
	
	参数：
	titlelist：形如 [  ["loss" , [ ["train" , []] , ["test" , []] ]]  , ["acc" , []] ]

	返回值：形如[
		{
			"label": "loss",
			"value": "loss",
		},
		{
			"label": "train",
			"value": "test",
		},
		...
	]

	*/

	if(titlelist == undefined || titlelist == []){
		return []
	}


	let ret = []
	for(let [title_name , sons] of titlelist)
	{
		ret.push({
			"label": title_name , //TODO：搞成 father-son这种形式
			"value": make_filter_title(title_name , father_list), 
		})
		ret = ret.concat(titlelist2options(sons , father_list.concat(title_name)))
	}
	return ret
}

export function get_opr_options(){
	return [
		{
			value: "fitter-opt:exists",
			label: "存在",
		},
		{
			value: "fitter-opt:interval",
			label: "范围",
		},
		{
			value: "fitter-opt:regular",
			label: "正则",
		},

	]
}