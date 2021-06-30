export function maketitle(title_name){
	// 根据title的名称生成title的key

	return `fitter-title:${title_name}`
}
 
export function make_columns(titlelist){
	/*根据远端发送的title信息生成可以直接用于vue组件的title变量。
	
	参数：
	titlelist：形如 [  ["loss" , [ ["train"] , ["test"] ]]  , ["acc"] ]

	返回值：形如[
		{
			key: "fitter-title:loss",
			title: "loss",
			children:[
				{
					key: "fitter-title:train",
					title: "train",
				},
				{
					key: "fitter-title:test",
					title: "test",
				},
			]
		},				
		{
			key: "fitter-title:acc",
			title: "acc",
		},
	]

	*/

	let ret = []
	for(let t of titlelist)
	{
		let title_name = t[0]
		let cur = {
			"title": title_name , 
			"key":  maketitle(title_name), 
		}
		if(t.length > 1){
			cur["children"] = make_columns(t[1])
		}
		ret.push(cur)
	}
	return ret
}

export function make_datas(datadict){
	/*根据远端发送的data信息生成可以直接用于vue组件的data变量。

	参数：
	datadict：形如 {
		23: {
			"loss" : 0.5,
			"acc"  : 1.0,
		},
		24:{
			"loss" : 0.7,
			"acc"  : 0.9,
		},
	}

	返回值：形如[
		{
			key: 23,
			"fitter-title:loss": 0.5,
			"fitter-title:acc" : 1.0,
		},
		{
			key: 24,
			"fitter-title:loss": 0.7,
			"fitter-title:acc" : 0.9,
		},
	]

	*/

	let ret = []
	for(let key in datadict)
	{
		let data_item_old = datadict[key]
		let data_item = {}
		for (let title_name in data_item_old)
			data_item[maketitle(title_name)] = data_item_old[title_name]
		data_item["key"] = key
		ret.push(data_item)
	}
	return ret
}
