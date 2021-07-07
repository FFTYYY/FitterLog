import {make_column_title , title_process} from "../scripts/title_list_process.js"
import {isnull , ID_COLUMN} from "../scripts/utils.js"

export function make_columns(titlelist){
	/*将titlelist转成可以直接用于naiveui.table的columns的格式*/
	let full_titlelist = [[ID_COLUMN , []]]
	if(!isnull(titlelist))
		full_titlelist = full_titlelist.concat(titlelist)

	return title_process(full_titlelist , [] , {
		title: (titlename , fatherlist) => titlename == ID_COLUMN ? "id" : titlename , 
		key  :  make_column_title , 
	})
}

export function make_datas(datadict){
	/*将datadict转成可以直接用于naiveui.table的columns的格式

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
		data_item[make_column_title(ID_COLUMN,[])] = key // ID栏
		data_item["key"] 	 = key // vue的key
		ret.push(data_item)
	}


	return ret
}
