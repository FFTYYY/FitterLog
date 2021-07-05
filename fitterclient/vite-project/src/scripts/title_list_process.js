import {CLAUSE_ROOT_NAME , CLAUSE_CONCAT , COLUMN_PREFIX , FILTER_PREFIX} from "./utils.js"
import {isnull} from "./utils.js"

function get_real_name(title_name , father_list){
	/*对于给定的father_list和直接名title_name，生成一个真实名。
	*/
	if(!isnull(father_list))
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
	在filter中不添加前缀，直接用真实名，因为是要去筛选的。
	*/
	return get_real_name(title_name , father_list)
}
