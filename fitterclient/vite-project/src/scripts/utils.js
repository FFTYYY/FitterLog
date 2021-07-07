export var CLAUSE_ROOT_NAME  = "_fitterlog_root"    // 从句的默认名
export var CLAUSE_CONCAT 	 = "-fitterlog-concat-" // 在clause的真实名中连接父名和子名的字符串
export var COLUMN_PREFIX 	 = "fitter-column" 		// colum的title前缀
export var SELECTOR_PREFIX 	 = "fitter-selector" 		// colum的title前缀

export var FILTER_PREFIX 	 = "fitter-filter" 		// filter的title前缀
export var ID_COLUMN 	 	 = "fitter-id" // filter的title前缀

export function isnull(o){
	return o == null || o == undefined 
}
