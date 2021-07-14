import {CLAUSE_ROOT_NAME , CLAUSE_CONCAT , COLUMN_PREFIX , FILTER_PREFIX , SELECTOR_PREFIX} from "./utils.js"
import {isnull_str , isnull_list , isnull_obj} from "./utils.js"

function get_real_name(predname , fatherlist){
	/*对于给定的fatherlist和直接名predname，生成一个真实名。
	*/
	if(!isnull_list(fatherlist))
		return ["" , CLAUSE_ROOT_NAME].concat(fatherlist).concat(predname).join(CLAUSE_CONCAT)
	return predname
}

export function make_column_key(predname , fatherlist){
	/*对于给定的fatherlist和直接名predname，生成一个真实名。并转换成predlist的格式为column的格式。
	*/

	return `${COLUMN_PREFIX}:${get_real_name(predname , fatherlist)}`
}

export function make_filter_key(predname , fatherlist){
	/*对于给定的fatherlist和直接名predname，生成一个真实名。并转换成predlist的格式为filter的格式。
	在filter中不添加前缀，直接用真实名，因为是要传给后端去筛选的。
	*/
	return get_real_name(predname , fatherlist)
}
export function make_selector_key(predname , fatherlist){
	/*对于给定的fatherlist和直接名predname，生成一个真实名。并转换成predlist的格式为selector的格式。
	*/

	return `${SELECTOR_PREFIX}:${get_real_name(predname , fatherlist)}`
}



export function predlist_process(
	predlist , 
	fatherlist   = [] , 
	key_and_funcs = {} , 
	sons_key 	  = undefined , 
	leaf_extra    = {} , 
){
	/*根据远端发送的predlist信息生成可以直接用于vue组件的predlist变量。
	key_and_funcs的键是生成的结果中的键，值是一个函数，接受predname和一个fatherlist，并将他们处理成结果

	参数：
	predlist：形如 [  ["loss" , [ ["train" , []] , ["test" , []] ]]  , ["acc" , []] ]

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
	if ( isnull_list(predlist) )
		return []

	let ret = []
	
	for(let [predname , sons] of predlist){
		let cur = {}

		for(let key in key_and_funcs){
			let func = key_and_funcs[key]
			cur[key] = func(predname , fatherlist)
		}
				

		// 为叶子添加额外属性
		if((isnull_list(sons) || sons.length <= 0) && (!isnull_obj(leaf_extra))){
			for(let key in leaf_extra){
				let func = leaf_extra[key]
				cur[key] = func(predname , fatherlist)
			}
		}

		if(isnull_str(sons_key)) //拉成平面
		{
			ret = ret.concat(predlist_process(
					sons , fatherlist.concat([predname]) , key_and_funcs , sons_key , leaf_extra
			))
		}
		else{
			if((!isnull_list(sons)) && sons.length > 0){ //有后代节点
				cur[sons_key] = predlist_process(
					sons , fatherlist.concat([predname]) , key_and_funcs , sons_key , leaf_extra
				)
			}
		}

		ret.push(cur)
	}
	return ret
}
