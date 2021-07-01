export function titlelist2options(titlelist){
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
	for(let t of titlelist)
	{
		let title_name = t[0]
		ret.push({
			"value": title_name , 
			"label": title_name, 
		})
		ret = ret.concat(titlelist2options(t[1]))
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