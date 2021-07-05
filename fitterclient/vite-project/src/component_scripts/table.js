import {make_column_title} from "../scripts/title_list_process.js"
import {isnull , ID_COLUMN} from "../scripts/utils.js"

export function make_columns(titlelist , father_list = []){
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

	if ( isnull(titlelist) )
		return []

	let ret = []
	if(father_list.length == 0){ // 当他是根的时候，添加一个id栏
		ret.push({
			title: "id" , 
			key  : ID_COLUMN,
		})
	}
	
	for(let [title_name , sons] of titlelist){
		let cur = {
			title: title_name , // 对于显示，直接用直接名。
			key  : make_column_title(title_name , father_list), // 对于key，转换成真实名，并附加title格式。
		}
		if(sons.length > 0){ //有后代节点
			cur["children"] = make_columns(sons , father_list.concat([title_name]))
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
	注意，datadict中传过来的key应该是真实名。

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
	if ( isnull(datadict) )
		return []

	let ret = []
	for(let key in datadict)
	{
		let data_item_old = datadict[key]
		let data_item = {}
		for (let title_name in data_item_old){
			// 按照约定，title_name已经是真实名了，因此无需转换
			data_item[make_column_title(title_name , undefined)] = data_item_old[title_name]
		}
		data_item[ID_COLUMN] = key // ID栏
		data_item["key"] 	 = key // vue的key
		ret.push(data_item)
	}


	return ret
}
