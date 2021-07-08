import {CLAUSE_ROOT_NAME , CLAUSE_CONCAT , COLUMN_PREFIX , FILTER_PREFIX , SELECTOR_PREFIX} from "./utils.js"
import {isnull_str , isnull_list , isnull_obj} from "./utils.js"

function get_real_name(title_name , father_list){
	/*对于给定的father_list和直接名title_name，生成一个真实名。
	*/
	if(!isnull_list(father_list))
		return ["" , CLAUSE_ROOT_NAME].concat(father_list).concat(title_name).join(CLAUSE_CONCAT)
	return title_name
}

export function make_column_title(title_name , father_list){
	/*对于给定的father_list和直接名title_name，生成一个真实名。并转换成title的格式为column的格式。
	*/

	return `${COLUMN_PREFIX}:${get_real_name(title_name , father_list)}`
}

export function make_filter_title(title_name , father_list){
	/*对于给定的father_list和直接名title_name，生成一个真实名。并转换成title的格式为filter的格式。
	在filter中不添加前缀，直接用真实名，因为是要传给后端去筛选的。
	*/
	return get_real_name(title_name , father_list)
}
export function make_filter_title_user(title_name , father_list){
	/*生成适合用户的filter-title
	*/
	return father_list.concat([title_name]).join("-")
}

export function make_selector_title(title_name , father_list){
	/*对于给定的father_list和直接名title_name，生成一个真实名。并转换成title的格式为selector的格式。
	*/

	return `${SELECTOR_PREFIX}:${get_real_name(title_name , father_list)}`
}



export function title_process(
	title_list , 
	father_list   = [] , 
	key_and_funcs = {} , 
	sons_key 	  = undefined , 
	leaf_extra    = {} , 
){
	/*根据远端发送的title信息生成可以直接用于vue组件的title变量。
	key_and_funcs的键是生成的结果中的键，值是一个函数，接受title_name和一个father_list，并将他们处理成结果

	参数：
	titlelist：形如 [  ["loss" , [ ["train" , []] , ["test" , []] ]]  , ["acc" , []] ]

	返回值：形如[
		{
			key_1: key_and_funcs["key_1"]("loss" , []),
			key_2: key_and_funcs["key_2"]("loss" , []),
			children:[
				{
					key_1: key_and_funcs["key_1"]("dev" , ["loss"]),
					key_2: key_and_funcs["key_2"]("dev" , ["loss"]),
				},
				{
					key_1: key_and_funcs["key_1"]("test" , ["loss"]),
					key_2: key_and_funcs["key_2"]("test" , ["loss"]),
				},
			]
		},				
		{
			key_1: key_and_funcs["key_1"]("acc" , []),
			key_2: key_and_funcs["key_2"]("acc" , []),
		},
	]

	*/
	if ( isnull_list(title_list) )
		return []

	let ret = []
	
	for(let [title_name , sons] of title_list){
		let cur = {}

		for(let key in key_and_funcs){
			let func = key_and_funcs[key]
			cur[key] = func(title_name , father_list)
		}
				

		// 为叶子添加额外属性
		if((isnull_list(sons) || sons.length <= 0) && (!isnull_obj(leaf_extra))){
			for(let key in leaf_extra){
				let func = leaf_extra[key]
				cur[key] = func(title_name , father_list)
			}
		}

		if(isnull_str(sons_key)) //拉成平面
		{
			ret = ret.concat(title_process(
					sons , father_list.concat([title_name]) , key_and_funcs , sons_key , leaf_extra
			))
		}
		else{
			if((!isnull_list(sons)) && sons.length > 0){ //有后代节点
				cur[sons_key] = title_process(
					sons , father_list.concat([title_name]) , key_and_funcs , sons_key , leaf_extra
				)
			}
		}

		ret.push(cur)
	}
	return ret
}
